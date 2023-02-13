#main.py

import cv2 as cv
import time
import depthai as dai
from cameraInitialisationClass import initialise
from imageProcessingClasses import imageProcessing
from imageCaptureClasses import imageCapture
from imageMaskGeneration import recalibrate
from imageCalibration import imageCalibration
from imageStitchingClasses import imageStitching
import time
import os
from pylogix import PLC
from PLCUpdate import transferToPLC

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
with dai.Device(pipeline) as device:
    
    captureObject = imageCapture(device.getOutputQueue(name="rgb", maxSize=30, blocking=False), 
                                device.getOutputQueue(name="still", maxSize=30, blocking=True), 
                                device.getInputQueue(name="control"))

    

     #Set Brightness, Focal
    brightness, lensPos = captureObject.setParameters()

#----------------------Inputs for station100, hardcoded for now---------------------#

    maskObject = recalibrate()

    maskDir = "Object_Detection\Photos\Masks"
    masks = ["top.jpg", "left.jpg", "bottom.jpg", "right.jpg"]

    refDir = "Object_Detection\Photos\Refs"
    refs = ["top.jpg", "left.jpg", "bottom.jpg", "right.jpg"]

    colDir = "Object_Detection\Photos\Col"
    cols = ["top.jpg", "left.jpg", "bottom.jpg", "right.jpg"]

    for i in range(len(refs)):
        refPath = os.path.join(refDir, refs[i])
        colPath = os.path.join(colDir, cols[i])
        maskPath = os.path.join(maskDir, masks[i])

        print("Load " + masks[i])
        cv.waitKey(0)
        refs[i] = captureObject.captureImage(refPath)
        print("Change to colour")
        cv.waitKey(0)
        cols[i] = captureObject.captureImage(colPath)

        mask = recalibrate.createMask(refs[i], cols[i], maskPath)
        masks[i] = mask
        
    station100ProcessingObject = imageProcessing(masks, refs, ref,"station100")
    
    #-------------------------------------------------------------------------------------------#
    
    while True:
        captureObject.autoCapture("Test.jpg", photoDirectoryName, station100ProcessingObject) 
        capturedImages = captureObject.autoCapture("Test.jpg", photoDirectoryName, station100ProcessingObject) 
        transferToPLC("OP100", capturedImages)
        
        # # for i in range(len(result)):
        # for object in station100ProcessingObjectArray:
        #     object.setTestImg()
        #     error, diffImg = object.compareImage()
        #     print("Image " + i+ ": " +error)
        #     # if error < tolerance:
        #     #     resultArray[i] = 1
        # # updatePLC(errorArray)
        