#main.py#

import cv2 as cv
import time
import depthai as dai
from imageProcessingClasses import imageProcessing
from imageCaptureClasses import initialise, imageCapture
from imageCalibration import imageCalibration
from imageStitchingClasses import imageStitching

#-----------------------------------------Importing folders, images-----------------------------------------#
#Photos Path
photosPath = "Object_Detection\photos\Input"

#-----------------------------------------Main Loop-----------------------------------------#
needCalibrate = False

initialisationObject = initialise(photosPath)
photoDirectoryName, pipeline, camRgb, xoutRgb, xin, videoEnc, xoutStill, pipeline_1 = initialisationObject.initialise()

for device in dai.Device.getAllAvailableDevices():
    print(f"{device.getMxId()} {device.state}")

#device_info = dai.DeviceBootloader(dai.DeviceInfo("1944301051766E1300"), allowFlashingBootloader = True)
device_info = dai.DeviceInfo("1944301051766E1300")
device_info.state = dai.XLinkDeviceState.X_LINK_BOOTLOADER
device_info.protocol = dai.XLinkProtocol.X_LINK_TCP_IP

device_info_1 = dai.DeviceInfo("19443010613C6E1300")
device_info_1.state = dai.XLinkDeviceState.X_LINK_BOOTLOADER
device_info_1.protocol = dai.XLinkProtocol.X_LINK_TCP_IP

total_device_info = [device_info]
total_pipeline = [pipeline]

for myDevice, myPipeline in total_device_info, total_pipeline:
    with dai.Device(myDevice, myDevice) as device:
        captureObject = imageCapture(device.getOutputQueue(name="rgb", maxSize=30, blocking=False), 
                                    device.getOutputQueue(name="still", maxSize=30, blocking=True), 
                                    device.getInputQueue(name="control"),
                                    photoDirectoryName)
    
        captureObject.maskCapture()    
        # for i in range(5):                   
        #     initialTestImg, initialTestImgPath = captureObject.autoCapture()
        #     cv.imshow("test", initialTestImg)
            
        #     cv.waitKey(0)
        # initialTestImg, initialTestImgPath = captureObject.autoCapture()
            
        # processingObject = imageProcessing(maskImg, refImg, initialTestImg, initialTestImgPath)

        # while needCalibrate == False:
        #     testImg, testImgPath = captureObject.capture()

        #     cv.imshow("test",testImg)
        #     # set up and calibrate the images from both cameras
        #     myImageCalibration = imageCalibration(testImgPath)
        #     myImageCalibration.imageCalibration() # -> return void and calibrate both images

        #     # stitch the images together
        #     myImageStitching = imageStitching(testImgPath)
        #     myImageStitching.stitchImgs() # -> return void and stitch both images into 1 image

        #     # start process the images
        #     processingObject.setTestImg(testImg,testImgPath)
        #     response = processingObject.compareImage()
            
        #     time.sleep(1)

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