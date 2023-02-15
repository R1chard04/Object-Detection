#main.py

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

    top = cv.imread("Object_Detection\Photos\Masks/top.jpg", 0)
    left = cv.imread("Object_Detection\Photos\Masks/left.jpg", 0)
    bottom = cv.imread("Object_Detection\Photos\Masks/bottom.jpg", 0)
    right = cv.imread("Object_Detection\Photos\Masks/right.jpg", 0)
    
    masks = [top,left,bottom,right]    

    #----------------------Error Algorithm and Image Processing Initialisation---------------------#
    tempRef = captureObject.captureImage(os.path.join(refDir, "STD.jpg")) #Creating a stand-in initialisation picture
    processingObject = imageProcessing(masks, tempRef, tempRef, partList) #Initialisation of the processing object

    print("Load all parts then press any key")
    cv.waitKey(0)

    #After loading all parts, camera begins capturing reference photos
    for i in range(25):
        captureObject.captureOne("Test", errDir, processingObject)

    # Taking a standard image
    ref = captureObject.captureOne(os.path.join(refDir, "STD.jpg"))
    processingObject.setRefImg(ref)

    #Post-processing of captured images for MSE threshold creation

    for image in os.listdir(errDir):
        path = os.path.join(errDir, image)
        img = cv.imread(path)

        processingObject.setTestImg(img)   
        error = processingObject.compareImage()
        passref = getPassRef(error, passRef)
        print(error, passref)
    

    #-------------------------------------------------------------------------------------------#

    while True:
        img = cv.imread(captureObject.autoCapture("Test", photoDirectoryName, processingObject))
        

        prediction = MSEStabilization(error, passref) #Generates PASS/FAIL array
        print(prediction.result())




        
    #     transferToPLC("OP100", RESULTARRAYTBD)
        
        # # for i in range(len(result)):
        # for object in station100ProcessingObjectArray:
        #     object.setTestImg()
        #     error, diffImg = object.compareImage()
        #     print("Image " + i+ ": " +error)
        #     # if error < tolerance:
        #     #     resultArray[i] = 1
        # # updatePLC(errorArray)
        