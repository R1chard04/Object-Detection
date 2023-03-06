import cv2 as cv
import time
import depthai as dai
from cameraInitialisationClass import initialise
from imageProcessingClasses import imageProcessing
from imageCaptureClasses import imageCapture
from imageMaskGeneration import createMask
from imagePredictionClass import MSEStabilization, getPassRef
import time
import os
import json
import pdb

# time.sleep(5)
# from pylogix import PLC
# from PLCUpdate import transferToPLC

#-----------------------------------------Directories-----------------------------------------#
#Photos Path
photosPath = "Photos\Init" #This is where all the images are being saved

#MSE Initialisation Photos Path
errDir = "Photos\Err" #This is whered the difference images can be saved; they are not currently

#Mask Paths
refDir = "Photos\Refs" #This is where the reference photos for each part at one station are being saved
colDir = "Photos\Col" #This is where the alternate colour reference photos for each part at one station are being saved
maskDir = "Photos\Masks" #This is where the generated masks are being saved

#Part List
with open(r'params.json') as f:
  partList = json.load(f)

# select which station to use here
params = partList["station100"]

brightness = params["brightness"]
lensPos = params["lensPos"]
parts = params["parts"]
passref = params["passref"]
IP = params["IP"]
maskPaths = params["masks"]
refPaths = params["refs"]
colPaths = params ["cols"]
standardPath = params["standard"]
testPath = params["test"]

# for n in maskPaths:
#     print(n)
# print(refPaths[0])
# img = cv.imread(maskPaths[0])
# cv.imshow('hi',img)
# cv.waitKey(0)

# Create pipeline
pipeline = dai.Pipeline()
# This might improve reducing the latency on some systems
pipeline.setXLinkChunkSize(0)

# Define source and output
camRgb = pipeline.create(dai.node.ColorCamera)
camRgb.setFps(3)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
camRgb.setPreviewSize(1920, 1080)

xout = pipeline.create(dai.node.XLinkOut)
xout.setStreamName("out")
camRgb.isp.link(xout.input)
device_info = dai.DeviceInfo(IP)

with dai.Device(pipeline, device_info) as device:
    q = device.getOutputQueue(name="out")
    print("done params")

    # masks = maskSetup(selected, captureObject, recalibrate, brightness, lensPos, IP)
    masks = []
    for path in maskPaths:
        masks.append(cv.imread(path, 0))
    print("done masks")
    # tempRef = controlSetup(selected, captureObject, recalibrate, brightness, lensPos)
    tempRef = cv.imread(standardPath)
    # pdb.set_trace()
    processingObject = imageProcessing(masks, tempRef, tempRef, parts) #Initialisation of the processing object
    print("processing object initialized")

    # ref, passref = errorSetup(selected, captureObject, processingObject, recalibrate, brightness, lensPos)
    # print("errorsetup")
    # processingObject.setRefImg(tempRef)
    # print("refsetup")

#-------------------------------------------------------------------------------------------#   
    while True:
        
        imgFrame = q.get()
        print(IP)
        # capture a test image
        # img = captureObject.captureOne(testPath, brightness, lensPos)
        img = imgFrame.getCvFrame()
        processingObject.setTestImg(img)  
        # display the result on the frame
        frame = processingObject.displayResultPosition()
        # get the mse error
        error = processingObject.compareImage() 
        #Generates PASS/FAIL array
        prediction = MSEStabilization(error, passref, len(parts)) 

        result = prediction.result()
        # print(result)

        # transferToPLC("OP100", result)
        cv.waitKey(1)
        frame = cv.pyrDown(frame)
        frame = cv.pyrDown(frame)
        cv.imshow(IP, frame)