import cv2 as cv
import depthai as dai
from imageProcessingClasses import imageProcessing
from imagePredictionClass import MSEStabilization
from imageCalibrationClass import Recalibration, createPipeline
from pylogix import PLC
from PLCUpdate import writePLC
from imageTimingClasses import timeLog
from PLCUpdate import writePLC, readPLC
import time
from passref import create_pass_ref


camera = Recalibration("station120")
device_info = dai.DeviceInfo(camera.IP)



# create_pass_ref(camera=camera, device_info=device_info)
input("here: ")
time.sleep(10)
with dai.Device(createPipeline(), device_info) as device:
    camera.adjustCamera(device)
    processingObject = imageProcessing("station120")
    timeObject = timeLog(camera.station, camera.parts)

    while True:         
        print("started loop")
        img = camera.capture(device)
        processingObject.setTestImg(img)
        error = processingObject.compareImage()
        frame = processingObject.displayResultPosition()     
        prediction = MSEStabilization(error, camera.passref, len(camera.parts)) 

        print(error)
        result = prediction.result()
        print(result)
        
        clampClosed = False
        # clampClosed = readPLC("Program:Sta120.Station.Cycle.Step.Bit[10]")

        recorded = timeObject.log(result, clampClosed)

        # write PLC value to the HMI
        # writePLC("Camera_Output.5", result)

        # print(arr)
        # print(final)

        # transferToPLC("OP100", result)
        cv.waitKey(1)
        frame = cv.pyrDown(frame)
        cv.imshow(camera.IP, frame)

        # if recorded is True:
        #     while readPLC("Sta120_OK_To_Enter") is False:
        #         pass
        #     timeObject = timeLog(camera.station, camera.parts)
                