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
# from pylogix import PLC
# from PLCUpdate import updatePLC

#-----------------------------------------Importing folders, images-----------------------------------------#
#Photos Path
photosPath = "Object_Detection\Photos\Masking\INIT"

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
    # capture the image 
    captureObject = imageCapture(device.getOutputQueue(name="rgb", maxSize=30, blocking=False), 
                                device.getOutputQueue(name="still", maxSize=30, blocking=True), 
                                device.getInputQueue(name="control"))

    

     #Set Brightness, Focal
    brightness, lensPos = captureObject.setParameters()
    # myCalibration = imageCalibration(initImgPath)
    # myCalibration.imageCalibration()

    

#----------------------Inputs for station100, hardcoded for now---------------------#

    topMask = cv.cvtColor(cv.imread("Photos\MASKS\\topPartM.jpg"), cv.COLOR_BGR2GRAY)
    bottomMask = cv.cvtColor(cv.imread("Photos\MASKS\\bottomPartM.jpg"), cv.COLOR_BGR2GRAY)
    rightMask = cv.cvtColor(cv.imread("Photos\MASKS\\rightPartM.jpg"), cv.COLOR_BGR2GRAY)
    leftMask = cv.cvtColor(cv.imread("Photos\MASKS\leftPartM.jpg"), cv.COLOR_BGR2GRAY)

    topRef =cv.imread("Photos\STD\\topPart.jpg")
    leftRef =cv.imread("Photos\STD\leftPart.jpg")
    bottomRef =cv.imread("Photos\STD\\bottomPart.jpg")
    rightRef =cv.imread("Photos\STD\\rightPart.jpg")

    masks=[topMask,leftMask, bottomMask, rightMask]
    ref = cv.imread("Photos\STD\STD.jpg")
    refs =[topRef, leftRef, bottomRef,rightRef]

    # for i in range(4):
    #     object = imageProcessing(masks[i], refs[i], initImg)
    #     station100ProcessingObjectArray.append(object)
        
    station100ProcessingObject = imageProcessing(masks, refs, ref,"station100")
    
    #-----------------------------------------Calibrate-----------------------------------------#
  
    maskObject = recalibrate(captureObject, station100ProcessingObject, brightness, lensPos)

    # #gen mask
    # maskObject.setStandards()
    # maskObject.setNones()
    # maskObject.createMask()
    #-------------------------------------------------------------------------------------------#
    
    while True:
        captureObject.autoCapture("Test.jpg", photoDirectoryName, station100ProcessingObject) 
        # updatePLC(errorArray)
        capturedImages = captureObject.autoCapture("Test.jpg", photoDirectoryName, station100ProcessingObject) 
        
        # # for i in range(len(result)):
        # for object in station100ProcessingObjectArray:
        #     object.setTestImg()
        #     error, diffImg = object.compareImage()
        #     print("Image " + i+ ": " +error)
        #     # if error < tolerance:
        #     #     resultArray[i] = 1
        # # updatePLC(errorArray)
        
        

    # capture = time.time()
    # while True:
        

    # with dai.Device(pipeline_1, device_info_1) as device1:
    #     captureObject1 = imageCapture(device1.getOutputQueue(name="rgb", maxSize=30, blocking=False), 
    #                                 device1.getOutputQueue(name="still", maxSize=30, blocking=True), 
    #                                 device1.getInputQueue(name="control"),
    #                                 photoDirectoryName)
    
        
    #     for i in range(5):                   
    #         initialTestImg1, initialTestImgPath1 = captureObject1.capture()
    #         cv.imshow("test", initialTestImg1)
            
    #         cv.waitKey(0)
    #     initialTestImg1, initialTestImgPath1 = captureObject1.capture()
