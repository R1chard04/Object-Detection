import cv2 as cv
import time
import depthai as dai
from cameraInitialisationClass import initialise
from imageProcessingClasses import imageProcessing
from imageCaptureClasses import imageCapture
from imageMaskGeneration import recalibrate
from imagePredictionClass import MSEStabilization, getPassRef
import time
import os
import pdb
# from pylogix import PLC
# from PLCUpdate import transferToPLC

#-----------------------------------------Importing folders, images-----------------------------------------#
#Photos Path
photosPath = "Object_Detection\Photos\Init" #This is where all the images are being saved

#Mask Paths
refDir = "Object_Detection\Photos\Refs" #This is where the reference photos for each part at one station are being saved
colDir = "Object_Detection\Photos\Col" #This is where the alternate colour reference photos for each part at one station are being saved
maskDir = "Object_Detection\Photos\Masks" #This is where the generated masks are being saved

#MSE Initialisation Photos Path
errDir = "Object_Detection\Photos\Err"

#Part List
partList = ["Top", "Left", "Bottom", "Right"]

#-----------------------------------------Camera Initialisation-----------------------------------------#
initialisationObject = initialise(photosPath)
photoDirectoryName, pipeline, camRgb, xoutRgb, xin, videoEnc, xoutStill, pipeline_1 = initialisationObject.initialise()

for device in dai.Device.getAllAvailableDevices():
    print(f"{device.getMxId()} {device.state}")

device_info = dai.DeviceInfo("19443010A137DE1200")
device_info.state = dai.XLinkDeviceState.X_LINK_BOOTLOADER
device_info.protocol = dai.XLinkProtocol.X_LINK_TCP_IP

#----------------------Camera Capture Initialisation---------------------#
with dai.Device(pipeline) as device:
    
    captureObject = imageCapture(device.getOutputQueue(name="rgb", maxSize=30, blocking=False), 
                                device.getOutputQueue(name="still", maxSize=30, blocking=True), 
                                device.getInputQueue(name="control"))

    #Camera frame and brightness setup window
    brightness, lensPos = captureObject.setParameters()
    cv.destroyAllWindows()

#----------------------Mask Initialisation---------------------#

    # maskObject = recalibrate() #Instantiation of the mask object
    # refs, cols, masks = ["top.jpg", "left.jpg", "bottom.jpg", "right.jpg"]  

    # for i in range(len(refs)):
    #     refPath = os.path.join(refDir, refs[i])
    #     colPath = os.path.join(colDir, cols[i])
    #     maskPath = os.path.join(maskDir, masks[i])

    #     print("Load " + partList[i])
    #     cv.waitKey(0)
    #     refs[i] = captureObject.captureImage(refPath)
    #     cv.destroyAllWindows()
        
    #     print("Change to colour")
    #     cv.waitKey(0)
    #     cols[i] = captureObject.captureImage(colPath)
    #     cv.destroyAllWindows()

    #     print("creating a mask, this may take a couple minutes.")
    #     mask = recalibrate.createMask(refs[i], cols[i], maskPath)
    #     print("Mask generated")
    #     masks[i] = mask


    # print("Load " + "right")
    # refPath = "Object_Detection\Photos\Refs\\right1.jpg"
    # cv.waitKey(0)
    # ref = captureObject.captureImage(refPath)
    # cv.destroyAllWindows()
    
    # print("Change to colour")
    # cv.waitKey(0)
    # colPath = "Object_Detection\Photos\Col\\right1.jpg"
    # col = captureObject.captureImage(colPath)
    # cv.destroyAllWindows()

    # print("creating a mask, this may take a couple minutes.")
    # maskPath = "Object_Detection\Photos\Masks\\right1.jpg"
    # mask = recalibrate.createMask(ref, col, maskPath)
    # print("Mask generated")

    top = cv.imread("Object_Detection\Photos\Masks/top.jpg", 0)
    left = cv.imread("Object_Detection\Photos\Masks/left1.jpg", 0)
    bottom = cv.imread("Object_Detection\Photos\Masks/bottom.jpg", 0)
    right = cv.imread("Object_Detection\Photos\Masks/right1.jpg", 0)
    
    masks = [top,left,bottom,right]    

    #----------------------Error Algorithm and Image Processing Initialisation---------------------#
    tempRef = captureObject.captureImage(os.path.join(refDir, "STD.jpg")) #Creating a stand-in initialisation picture
    processingObject = imageProcessing(masks, tempRef, tempRef, partList) #Initialisation of the processing object

    print("Load all parts then press any key")
    cv.waitKey(0)

    #After loading all parts, camera begins capturing reference photos
    for i in range(3):
        # captureObject.autoCapture("Test", errDir, processingObject)
        testImg = captureObject.captureOne(os.path.join(errDir, "Test " + str(i) + ".jpg"), brightness, lensPos)
        time.sleep(0.5)

    # Taking a standard image
    ref = captureObject.captureOne(os.path.join(refDir, "STD.jpg"), brightness, lensPos)
    processingObject.setRefImg(ref)

    #Post-processing of captured images for MSE threshold creation
    passRef = [0,0,0,0] #for now

    for image in os.listdir(errDir):
        path = os.path.join(errDir, image)
        img = cv.imread(path)

        processingObject.setTestImg(img)   
        error = processingObject.compareImage()
        passref = getPassRef(error, passRef)
        print(error, passref)
    
    cv.destroyAllWindows()
    

    #-------------------------------------------------------------------------------------------#

    while True:
        img = cv.imread(captureObject.autoCapture("Test.jpg", photoDirectoryName, processingObject, brightness, lensPos))
        
        processingObject.setTestImg(img)  
        frame = processingObject.displayResultPosition()
        error = processingObject.compareImage() # compare w all the parts
        
        prediction = MSEStabilization(error, passref, 4) #Generates PASS/FAIL array

        # if top is there, compare w tlr or tlbr
        # if top is not there, compare w lbr or lr
        result = prediction.result()
        print(result)

        frame = cv.pyrDown(frame)
        frame = cv.pyrDown(frame)
        cv.imshow("errors", frame)
        cv.waitKey(1)
        
        




        
    #     transferToPLC("OP100", RESULTARRAYTBD)
        
        # # for i in range(len(result)):
        # for object in station100ProcessingObjectArray:
        #     object.setTestImg()
        #     error, diffImg = object.compareImage()
        #     print("Image " + i+ ": " +error)
        #     # if error < tolerance:
        #     #     resultArray[i] = 1
        # # updatePLC(errorArray)
        