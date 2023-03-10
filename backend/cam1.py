import cv2 as cv
import time
import depthai as dai
from imageProcessingClasses import imageProcessing
from imagePredictionClass import MSEStabilization
from calibrations import Recalibration, createPipeline
from imageRenamingClasses import BinaryNameAssigner
from imageTimingClasses import imageTiming
from imageAverageClasses import imageAverage
import time
import cv2 as cv
import depthai as dai
import pdb
import pylogix 
from pylogix import PLC
from PLCUpdate import writePLC


db_config = {
    "hostname": "localhost",
    "database": "imageTiming",
    "username": "postgres",
    "pwd": "W1nter@2023Hydro",
    "port_id": 5432
}

camera = Recalibration("station120")
processingObject = imageProcessing("station120")

device_info = dai.DeviceInfo(camera.IP)

with dai.Device(createPipeline(), device_info) as device:
    camera.adjustCamera(device)
    camera.pressKeyCapture(device, camera.standardPath)
    
    print("start")
    
    array = [0, 0, 0, 0]
    bna = BinaryNameAssigner(array)
    assigned_names = bna.assign()
    
    while True:     
        
        img = camera.capture(device)
        processingObject.setTestImg(img)
        frame = processingObject.displayResultPosition()
        error = processingObject.compareImage()
        prediction = MSEStabilization(error, camera.passref, len(camera.parts)) 

        result = prediction.result()
        timing = imageTiming(assigned_names, db_config)
        response = timing.record(result)
        calculation = imageAverage(db_config)
        calculation.average(result)

        # write PLC value to the HMI
        writePLC("Camera_Output.5", result)
        
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