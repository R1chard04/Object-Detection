#main.py#

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
    initImgArry = ["", "", "", ""]
    processingObject = imageProcessing(initImgArray[0], initImgArray[0], initImgArray[0])


    topMask = cv.imread("Object_Detection\Photos\MASKS\topPart.png")
    bottomMask = cv.imread("Object_Detection\Photos\MASKS\bottomPart.png")
    rightMask = cv.imread("Object_Detection\Photos\MASKS\rightPart.png")
    leftMask = cv.imread("Object_Detection\Photos\MASKS\leftPart.png")

    topRef =cv.imread("Quadrant 3.jpg")
    leftRef =cv.imread("Quadrant 1.jpg")
    bottomRef =cv.imread("Quadrant 4.jpg")
    rightRef =cv.imread("Quadrant 2.jpg")

    processingObjectArray = []

    masks=[topMask,leftMask, bottomMask, rightMask]
    refs =[topRef, leftRef, bottomRef,rightRef]

    for i in range(4):
        object = imageProcessing(masks[i], refs[i], initImg)
        processingObjectArray.append(object)

    #-----------------------------------------Calibrate-----------------------------------------#
  

    maskObject = recalibrate(captureObject, processingObject, brightness, lensPos)

    # #gen mask
    # maskObject.setStandards()
    # maskObject.setNones()
    # maskObject.createMask()
    #-------------------------------------------------------------------------------------------#
    
    while True:
        captureObject.autoCapture("Test.jpg", photoDirectoryName, processingObjectArray) 
        # updatePLC(errorArray)
        capturedImages = captureObject.autoCapture("Test.jpg", photoDirectoryName, processingObject) 
        
        # # for i in range(len(result)):
        # for object in processingObjectArray:
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
