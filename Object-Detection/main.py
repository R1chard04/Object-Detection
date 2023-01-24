import cv2 as cv
import time
import depthai as dai
from imageProcessingClasses import imageProcessing
from imageCaptureClasses import initialise, imageCapture

#-----------------------------------------Importing folders, images, report-----------------------------------------#
#Mask
maskImg = cv.imread('Object-Detection\photos\Test\mask.jpg')  #No tolerance around piece, 1-4 is increasing in tolerance

#Standard
refImg = cv.imread('Object-Detection\photos\Test\Reference\STANDARD.jpg')

#Report and Photos Path
reportPath = "Object-Detection\Report.txt"
photosPath = "Object-Detection\photos\Input"

#-----------------------------------------Main Loop-----------------------------------------#
initialiseObject = initialise(reportPath, photosPath)
photoDirectoryName, pipeline, camRgb, xoutRgb, xin, videoEnc, xoutStill = initialiseObject.initialise()

with dai.Device(pipeline) as device:
    #calibrate
    captureObject = imageCapture(device.getOutputQueue(name="rgb", maxSize=30, blocking=False), 
                                 device.getOutputQueue(name="still", maxSize=30, blocking=True), 
                                 device.getInputQueue(name="control"),
                                 photoDirectoryName)

    initialTestImg, initialTestImgPath = imageCapture.capture()
    processingObject = imageProcessing(maskImg, refImg, initialTestImg, reportPath, initialTestImgPath)

    while True:
        testImg, testImgPath = imageCapture.capture()
        processingObject.setTestImg(testImg,testImgPath)
        response = processingObject.compareImage()
        time.sleep(1)
