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
photosPath = "Object_Detection\Photos\Init"

#-----------------------------------------Main Loop-----------------------------------------#
needCalibrate = False

initialisationObject = initialise(photosPath)
photoDirectoryName, pipeline, camRgb, xoutRgb, xin, videoEnc, xoutStill, pipeline_1 = initialisationObject.initialise()

for device in dai.Device.getAllAvailableDevices():
    print(f"{device.getMxId()} {device.state}")

#device_info = dai.DeviceBootloader(dai.DeviceInfo("1944301051766E1300"), allowFlashingBootloader = True)
device_info = dai.DeviceInfo("19443010A137DE1200")
device_info.state = dai.XLinkDeviceState.X_LINK_BOOTLOADER
device_info.protocol = dai.XLinkProtocol.X_LINK_TCP_IP

# device_info_1 = dai.DeviceInfo("19443010613C6E1300")
# device_info_1.state = dai.XLinkDeviceState.X_LINK_BOOTLOADER
# device_info_1.protocol = dai.XLinkProtocol.X_LINK_TCP_IP

# total_device_info = [device_info]
# total_pipeline = [pipeline]

# for myDevice, myPipeline in total_device_info, total_pipeline:

#----------------------Capture Init---------------------#
with dai.Device(pipeline) as device:
    
    captureObject = imageCapture(device.getOutputQueue(name="rgb", maxSize=30, blocking=False), 
                                device.getOutputQueue(name="still", maxSize=30, blocking=True), 
                                device.getInputQueue(name="control"))

    #Set Brightness, Focal
    brightness, lensPos = captureObject.setParameters()
    cv.destroyAllWindows()

#----------------------Mask Init---------------------#

    # maskObject = recalibrate()

    # maskDir = "Object_Detection\Photos\Masks"
    # masks = ["top.jpg", "left.jpg", "bottom.jpg", "right.jpg"]

    # refDir = "Object_Detection\Photos\Refs"
    # refs = ["top.jpg", "left.jpg", "bottom.jpg", "right.jpg"]

    # colDir = "Object_Detection\Photos\Col"
    # cols = ["top.jpg", "left.jpg", "bottom.jpg", "right.jpg"]

    # for i in range(len(refs)):
    #     refPath = os.path.join(refDir, refs[i])
    #     colPath = os.path.join(colDir, cols[i])
    #     maskPath = os.path.join(maskDir, masks[i])

    #     print("Load " + masks[i])
    #     cv.waitKey(0)
    #     refs[i] = captureObject.captureImage(refPath)

    #     cv.destroyAllWindows()
        
    #     print("Change to colour")
    #     cv.waitKey(0)

    #     # pdb.set_trace()
    #     cols[i] = captureObject.captureImage(colPath)

    #     cv.destroyAllWindows()

    #     cv.imshow("ref", refs[i])
    #     cv.waitKey(0)
    #     cv.destroyAllWindows()

    #     mask = recalibrate.createMask(refs[i], cols[i], maskPath)
    #     cv.imshow("mask", mask)
    #     cv.waitKey(0)
    #     masks[i] = mask

    top = cv.imread("Object_Detection\Photos\Masks/top.jpg", 0)
    left = cv.imread("Object_Detection\Photos\Masks/left.jpg", 0)
    bottom = cv.imread("Object_Detection\Photos\Masks/bottom.jpg", 0)
    right = cv.imread("Object_Detection\Photos\Masks/right.jpg", 0)
    
    masks = [top,left,bottom,right]    

    # masks = [cv.imread("Object_Detection\Photos\Masks\\top.jpg",0), cv.imread("Object_Detection\Photos\Masks\left.jpg",0),cv.imread("Object_Detection\Photos\Masks\\bottom.jpg",0), cv.imread("Object_Detection\Photos\Masks\\right.jpg",0)]
    #-------------------------------------------------------------------------------------------#

    tempRef = captureObject.captureImage(os.path.join(photosPath, "STD.jpg"))
    partList = ["Top", "Left", "Bottom", "Right"]
    processingObject = imageProcessing(masks, tempRef, tempRef, partList)

    errDir = "Object_Detection\Photos\Err"

    print("Load all parts")
    cv.waitKey(0)

    while captureObject.autoCapture("Test", errDir, processingObject):
        pass
        
    print("here")
    ref = captureObject.captureImage(os.path.join(photosPath, "STD.jpg"))
    processingObject.setRefImg(ref)

    passRef = [0,0,0,0] #for now

    for image in os.listdir(errDir):
        print("here1")
        path = os.path.join(errDir, image)
        img = cv.imread(path)

        processingObject.setTestImg(img)   
        error = processingObject.compareImage()
        passref = getPassRef(error, passRef)
        print(passref)
    

    #-------------------------------------------------------------------------------------------#

    while True:
        img = cv.imread(captureObject.autoCapture("Test", photoDirectoryName, processingObject))
        processingObject.setTestImg(img)   
        error = processingObject.compareImage()
        prediction = MSEStabilization(error, passref)
        
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
        