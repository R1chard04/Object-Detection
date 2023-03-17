import cv2 as cv
import time
import depthai as dai
from imageProcessingClasses import imageProcessing
from imagePredictionClass import MSEStabilization
from imageCalibrationClass import Recalibration, createPipeline
from imageTimingClasses import imageTiming
from imageAverageClasses import imageAverage
import time
import cv2 as cv
import depthai as dai
import pdb
import pylogix 
from pylogix import PLC
from PLCUpdate import writePLC, readPLC
from timeLog import timeLog

db_config = {
     "hostname": "localhost",
     "database": "imageTiming",
     "username": "postgres",
     "pwd": "W1nter@2023Hydro",
     "port_id": 5432
 }

# Clamp at work for station#100
clampSt100 = readPLC("Program:Sta100.Station.Cycle.Step.Bit[7]")
# clear to enter station#100
clrSt100 = readPLC("Sta100_OK_To_Enter")

        

camera = Recalibration("station100")

device_info = dai.DeviceInfo(camera.IP)

with dai.Device(createPipeline(), device_info) as device:
    camera.adjustCamera(device)
    camera.pressKeyCapture(device, camera.standardPath)
    camera.errorSetup(device)
    print("final error:")
    print(camera.passref)
    camera.updateJson(camera.station)
    processingObject = imageProcessing("station100")
    
    print("start")
    
    #ask user to name each occurance in array
    new_partLists100 = ['TopPart', 'LeftPart', 'BottomPart', 'RightPart']
    print(new_partLists100)

    timing = imageTiming(new_partLists100, db_config)

    # arr = [0, 0, 0, 0]
    timeObject = timeLog(camera.station, camera.parts)
    
    while True:     
        
        img = camera.capture(device)
        processingObject.setTestImg(img)
        error = processingObject.compareImage()
        frame = processingObject.displayResultPosition()     
        prediction = MSEStabilization(error, camera.passref, len(camera.parts)) 
        # pdb.set_trace()
        result = prediction.result()

        # response = timing.record(result)
        # calculation = imageAverage(db_config)
        # final = calculation.average()

        # clampClosed = readPLC("Program:Sta100.Station.Cycle.Step.Bit[10]")
        clampClosed = False

        recorded = timeObject.log(result, clampClosed)

        
        #  # write PLC value to the HMI
        # writePLC("Camera_Output.1", result)
        print(result)

        # transferToPLC("OP100", result)
        cv.waitKey(1)
        frame = cv.pyrDown(frame)
        cv.imshow(camera.IP, frame)

        if recorded is True:
            while readPLC("Sta100_OK_To_Enter") is False:
                pass
            timeObject = timeLog(camera.station, camera.parts)