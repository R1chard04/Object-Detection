import cv2 as cv
import time
import depthai as dai
from imageProcessingClasses import imageProcessing
from imagePredictionClass import MSEStabilization
from calibrations import Recalibration, createPipeline
import time
import cv2 as cv
import depthai as dai

camera = Recalibration("station10")
processingObject = imageProcessing("station10")

device_info = dai.DeviceInfo(camera.IP)

with dai.Device(createPipeline(), device_info) as device:
    camera.adjustCamera(device)
    
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