import cv2 as cv
import time
import depthai as dai
from cameraInitialisationClass import initialise
from imageProcessingClasses import imageProcessing
from imageCaptureClasses import imageCapture
from imageMaskGeneration import createMask
from imagePredictionClass import MSEStabilization, getPassRef
from calibrations import Recalibration, createPipeline
import time
import os
import json
import pdb

# from pylogix import PLC
# from PLCUpdate import transferToPLC

#-----------------------------------------Camera Initialisation-----------------------------------------#

station = Recalibration("station10")
device_info = dai.DeviceInfo(station.IP)

with dai.Device(createPipeline(), device_info) as device:
    q = device.getOutputQueue(name="out")
    print("done params")

    # masks = maskSetup(selected, captureObject, recalibrate, brightness, lensPos, IP)
    masks = []
    for path in station.maskPaths:
        masks.append(cv.imread(path, 0))
    print("done masks")
    # tempRef = controlSetup(selected, captureObject, recalibrate, brightness, lensPos)
    tempRef = cv.imread(station.standardPath)
    processingObject = imageProcessing(masks, tempRef, tempRef, station.parts) #Initialisation of the processing object
    print("processing object initialized")

#-------------------------------------------------------------------------------------------#   
    while True:
        
        print(station.IP)
        # capture a test image
        # img = captureObject.captureOne(testPath, brightness, lensPos)
        processingObject.setTestImg(station.capture())  
        # display the result on the frame
        frame = processingObject.displayResultPosition()
        # get the mse error
        error = processingObject.compareImage() 
        #Generates PASS/FAIL array
        prediction = MSEStabilization(error, station.passref, len(station.parts)) 

        result = prediction.result()
        # print(result)

        # transferToPLC("OP100", result)
        cv.waitKey(1)
        frame = cv.pyrDown(frame)
        frame = cv.pyrDown(frame)
        cv.imshow(station.IP, frame)
        
# python cam1.py& python cam2.py& python cam3.py&