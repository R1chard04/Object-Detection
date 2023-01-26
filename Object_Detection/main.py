import cv2 as cv
import time
import depthai as dai
from imageProcessingClasses import imageProcessing
from imageCaptureClasses import initialise, imageCapture
from imageCalibration import imageCalibration
from imageStitchingClasses import imageStitching

#-----------------------------------------Importing folders, images-----------------------------------------#
#Standard
refImg = cv.imread('Object-Detection\photos\Test\Reference\STANDARD.jpg')

#Photos Path
photosPath = "Object-Detection\photos\Input"

#-----------------------------------------Main Loop-----------------------------------------#
needCalibrate = True

initialiseObject = initialise(photosPath)
photoDirectoryName, pipeline, camRgb, xoutRgb, xin, videoEnc, xoutStill = initialiseObject.initialise()

with dai.Device(pipeline) as device:
    captureObject = imageCapture(device.getOutputQueue(name="rgb", maxSize=30, blocking=False), 
                                 device.getOutputQueue(name="still", maxSize=30, blocking=True), 
                                 device.getInputQueue(name="control"),
                                 photoDirectoryName)

    # calibrate()                            
    initialTestImg, initialTestImgPath = captureObject.capture()
    processingObject = imageProcessing(maskImg, refImg, initialTestImg, initialTestImgPath)

    while needCalibrate == False:
        testImg, testImgPath = captureObject.capture()
        # set up and calibrate the images from both cameras
        myImageCalibration = imageCalibration(testImgPath)
        myImageCalibration.imageCalibration() # -> return void and calibrate both images

        # stitch the images together
        myImageStitching = imageStitching(testImgPath)
        myImageStitching.stitchImgs() # -> return void and stitch both images into 1 image

        # start process the images
        processingObject.setTestImg(testImg,testImgPath)
        response = processingObject.compareImage()
        
        time.sleep(1)
