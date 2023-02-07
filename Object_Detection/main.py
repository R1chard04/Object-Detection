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

# device_info_1 = dai.DeviceInfo("19443010613C6E1300")
# device_info_1.state = dai.XLinkDeviceState.X_LINK_BOOTLOADER
# device_info_1.protocol = dai.XLinkProtocol.X_LINK_TCP_IP

total_device_info = [device_info]
total_pipeline = [pipeline]

# for myDevice, myPipeline in total_device_info, total_pipeline:
with dai.Device(pipeline) as device:
    # Calibrate the camera using 10 images of the chessboards in order to get rid of the lens distortion
    # myImageCalibration = imageCalibration()
    # myImageCalibration.imageCalibration("calibrationImages/*.png")

    # Start capture the images after the len is distorted
    captureObject = imageCapture(device.getOutputQueue(name="rgb", maxSize=30, blocking=False), 
                                device.getOutputQueue(name="still", maxSize=30, blocking=True), 
                                device.getInputQueue(name="control"))


#-----------------------------------------Setup-----------------------------------------#
     #Set Brightness, Focal
    brightness, lensPos = captureObject.setParameters()
    print(brightness , " ", lensPos)

    initImg, initImgPath = captureObject.autoCapture("INIT.jpg", photoDirectoryName, brightness, lensPos)
    print(initImgPath)
    # myCalibration = imageCalibration("..\Photos\Masking\INIT")
    # myCalibration.imageCalibration()

    processingObject = imageProcessing(initImg, initImg, initImg)

#-----------------------------------------Calibrate-----------------------------------------#

    maskObject = recalibrate(captureObject, processingObject, brightness, lensPos)

    #gen mask
    # std = maskObject.setStandards()
    std = cv.imread("Object_Detection\Photos\STD\STD1.jpg")
    # cv.waitKey(0)
    # none = maskObject.setNones()
    mask = maskObject.createMask()

    processingObject.setMaskImg(mask)
    processingObject.setRefImg(std)

    print(mask.shape)
    print(std.shape)

    report = open("report.txt", "w")
    #-------------------------------------------------------------------------------------------#

    while True:
        testImg, testImgPath = captureObject.autoCapture("Test", photosPath, brightness, lensPos)
        processingObject.setTestImg(testImg)

        error, diffImg = processingObject.compareImage()

        path = os.path.join(diffPath, testImgPath)
        cv.imwrite(path, diffImg)
        print(error)
        report.write(testImgPath + " %s"%error + " \n")

        time.sleep(3)
    
