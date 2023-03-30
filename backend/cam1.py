import cv2 as cv
import depthai as dai
from imageProcessingClasses import imageProcessing
from imagePredictionClass import MSEStabilization
from imageCalibrationClass import Recalibration, createPipeline
import pdb
import pylogix 
from pylogix import PLC
from PLCUpdate import writePLC
from imageTimingClasses import timeLog
    
from PLCUpdate import writePLC, readPLC

# db_config = {
#      "hostname": "localhost",
#      "database": "imageTiming",
#      "username": "postgres",
#      "pwd": "W1nter@2023Hydro",
#      "port_id": 5432
#  }

camera = Recalibration("station120")
device_info = dai.DeviceInfo(camera.IP)

with dai.Device(createPipeline(), device_info) as device:
    camera.adjustCamera(device)
    camera.pressKeyCapture(device, camera.standardPath)
    camera.errorSetup(device)
    print("final error:")
    print(camera.passref)
    camera.updateJson(camera.station)
    processingObject = imageProcessing("station120")
    
    # print("start")
    
    # ask user to name each occurance in array
    # new_partLists120 = ['TopRightPart', 'TopLeftPart', 'LeftPart', 'BottomLeftPart', 'BottomRightPart', 'RightPart']
    # print(new_partLists120)

    # timing = imageTiming(assigned_names, db_config)

    # arr = [0, 0, 0, 0]
    timeObject = timeLog(camera.station, camera.parts)

    while True:         
        
        img = camera.capture(device)
        processingObject.setTestImg(img)
        error = processingObject.compareImage()
        frame = processingObject.displayResultPosition()     
        prediction = MSEStabilization(error, camera.passref, len(camera.parts)) 
        # pdb.set_trace()
        print(error)
        result = prediction.result()

        clampClosed = readPLC("Program:Sta120.Station.Cycle.Step.Bit[10]")

        recorded = timeObject.log(result, clampClosed)

        # response = timing.record(result)
        # calculation = imageAverage(db_config)
        # final = calculation.average()
        #  # write PLC value to the HMI
        writePLC("Camera_Output.5", result)

        # print(arr)
        # print(final)

        # transferToPLC("OP100", result)
        cv.waitKey(1)
        frame = cv.pyrDown(frame)
        cv.imshow(camera.IP, frame)

        if recorded is True:
            while readPLC("Sta120_OK_To_Enter") is False:
                pass
            timeObject = timeLog(camera.station, camera.parts)
                