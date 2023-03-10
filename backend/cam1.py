import cv2 as cv
import time
import depthai as dai
from imageProcessingClasses import imageProcessing
from imagePredictionClass import MSEStabilization
from calibrations import Recalibration, createPipeline
import time
import cv2 as cv
import depthai as dai
import pdb

camera = Recalibration("station120")
processingObject = imageProcessing("station120")

device_info = dai.DeviceInfo(camera.IP)

with dai.Device(createPipeline(), device_info) as device:
    camera.adjustCamera(device)
    camera.pressKeyCapture(device, camera.standardPath)
    
    print("start")
    while True:     
        
        img = camera.capture(device)
        processingObject.setTestImg(img)
        frame = processingObject.displayResultPosition()
        error = processingObject.compareImage()
        prediction = MSEStabilization(error, camera.passref, len(camera.parts)) 

        result = prediction.result()
        print(result)

        # transferToPLC("OP100", result)
        cv.waitKey(1)
        frame = cv.pyrDown(frame)
        frame = cv.pyrDown(frame)
        cv.imshow(camera.IP, frame)
        
    # print("press c to capture a standard picture")
    # camera.pressKeyCapture(device, camera.standardPath)
    # print("press c to start setting errors")
    # camera.errorSetup(device)
    # camera.updateJson(camera.station)