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
from imageSlicing import imageSlicing
import time
import os

#-----------------------------------------Importing folders, images-----------------------------------------#
#Photos Path
photosPath = "Object_Detection\Photos\INIT"
diffPath = "Object_Detection\Photos\DIFF"

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


with dai.Device(pipeline) as device:
    # Start capture the images after the len is distorted
    captureObject = imageCapture(device.getOutputQueue(name="rgb", maxSize=30, blocking=False), 
                                device.getOutputQueue(name="still", maxSize=30, blocking=True), 
                                device.getInputQueue(name="control"))


#-----------------------------------------Setup-----------------------------------------#
    #Set Brightness, Focal
    captureObject.setParameters()
    # brightness = -1
    # lensPos = 108
    # print(brightness , " ", lensPos)

    # initImg, initImgPath = captureObject.autoCapture("INIT.jpg", photoDirectoryName, brightness, lensPos)

    initImg = cv.imread("Object_Detection\Photos\INIT\INIT.jpg")
    processingObject = imageProcessing(initImg, initImg, initImg)

#-----------------------------------------Calibrate-----------------------------------------#

    # maskObject = recalibrate(captureObject, processingObject, brightness, lensPos)

    
    #gen mask
    # std = maskObject.setStandards()
    std = cv.imread("Object_Detection\Photos\STD\STD.jpg")
    mask = cv.imread("Object_Detection\Photos\mask.jpg", cv.IMREAD_GRAYSCALE)
    mask = cv.resize(mask, None, fx=1.875, fy=1.875, interpolation = cv.INTER_LINEAR)
    mask[mask != 0 ] = 255

    processingObject.setMaskImg(mask)
    processingObject.setRefImg(std)

    print(mask.shape)
    print(std.shape)

    report = open("report.txt", "w")
    
    #-------------------------------------------------------------------------------------------#

    
    captureObject.autoCapture("Test.jpg", photoDirectoryName, processingObject)

    # capture = time.time()
    # while True:
        
    #     path = "Object_Detection\Photos\INIT"
    #     result = "Object_Detection\Photos\DIFF"
    
    #     testImg, testImgPath = captureObject.autoCapture("Test", photosPath, brightness, lensPos)
    #     testImg = cv.imread(os.path.join(path, testImgPath))
    #     processingObject.setTestImg(testImg)
    #     cv.imshow("test",  cv.resize(testImg,(0,0), fx = 0.2, fy = 0.2))
    #     # cv.waitKey(1)

    #     error, diffImg = processingObject.compareImage()

    #     # dirname = os.path.dirname(result)
    #     # if not os.path.exists(dirname):
    #     #     os.makedirs(dirname)

    #     diffPath = os.path.join(result, testImgPath)
    #     cv.imwrite(diffPath, diffImg)
    #     print(error)
    #     report.write(testImgPath + " %s"%error + " \n")

    #     # time.sleep(3)

