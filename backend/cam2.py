#THis is cam1.py except it has a try except
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
import json
import requests
from passref import create_pass_ref


camera = Recalibration("station100")
device_info = dai.DeviceInfo(camera.IP)



# create_pass_ref(camera=camera, device_info=device_info)
input("enter")
with dai.Device(createPipeline(), device_info) as device:
    camera.adjustCamera(device)
    processingObject = imageProcessing("station100")
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
        # clampClosed = readPLC("Program:Sta100.Station.Cycle.Step.Bit[10]")

        recorded, record = timeObject.log(result, clampClosed)

        # write PLC value to the HMI
        # writePLC("Camera_Output.5", result)

        # print(arr)
        # print(final)

        # transferToPLC("OP100", result)
        cv.waitKey(1)

        # # send the POST request contains the errors, result and timing to the server
        # url = 'http://127.0.0.1:5000/bt1xx/post-result/100/'

        # request_headers = {
        #     'Content-Type' : 'application/json'
        # }

        # request_body = {
        #     'message' : 'Sending error, pass/fail rate and timing to the server!',
        #     'station_number' : '100',
        #     'passref' : camera.passref,
        #     'error' : error,
        #     'result' : result,
        #     'timing' : record
        # }

        # request_json = json.dumps(request_body)

        # response = requests.post(url, headers=request_headers, data=request_json)

        frame = cv.pyrDown(frame)
        cv.imshow(camera.IP, frame)

        # if recorded is True:
        #     while readPLC("Sta100_OK_To_Enter") is False:
        #         pass
        #     timeObject = timeLog(camera.station, camera.parts)