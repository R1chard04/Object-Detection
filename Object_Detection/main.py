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
photoDirectoryName, pipeline, camRgb, xoutRgb, xin, videoEnc, xoutStill = initialisationObject.initialise()

# Multiple cameras set up
device_info = dai.DeviceInfo("1944301051766E1300")
device_info.state = dai.XLinkDeviceState.X_LINK_BOOTLOADER
device_info.protocol = dai.XLinkProtocol.X_LINK_TCP_IP

with dai.Device(pipeline, device_info) as device:
    captureObject = imageCapture(device.getOutputQueue(name="rgb", maxSize=30, blocking=False), 
                                 device.getOutputQueue(name="still", maxSize=30, blocking=True), 
                                 device.getInputQueue(name="control"),
                                 photoDirectoryName)
   
    
    for i in range(5):                   
        initialTestImg, initialTestImgPath = captureObject.capture()
        cv.imshow("test", initialTestImg)
        
        cv.waitKey(0)
    initialTestImg, initialTestImgPath = captureObject.capture()
        
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
