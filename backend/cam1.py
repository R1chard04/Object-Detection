import cv2 as cv
import depthai as dai
from imageProcessingClasses import imageProcessing
from imagePredictionClass import MSEStabilization
from imageCalibrationClass import Recalibration, createPipeline
from pylogix import PLC
from PLCUpdate import writePLC
from imageTimingClasses import timeLog
from PLCUpdate import writePLC, readPLC, transferToPLC
import time
import json
import requests
from passref import create_pass_ref

#Establishing conection to the camera
camera = Recalibration("station120")
device_info = dai.DeviceInfo(camera.name)

print(device_info)

#After establishing the connection, enter the main program
with dai.Device(createPipeline(), device_info) as device:
    camera.adjustCamera(device) #adjusting camera fram to brightness and FOV
    processingObject = imageProcessing("station120") #init for processing
    timeObject = timeLog(camera.station, camera.parts) #init for timing

    while True:         #main loop
        print("started loop")
        img = camera.capture(device)
        processingObject.setTestImg(img) #capture and set the testing frame
        error = processingObject.compareImage() #acquiring the error/diff of the test relative to the ref image
        frame = processingObject.displayResultPosition()    #frame gen 
        prediction = MSEStabilization(error, camera.passref, len(camera.parts)) #producing a pass prediction of boolean values

        print("error is", error)
        result = prediction.result()  #grabbing the result of the pass/fail
        print("result is", result)
        
        #The code below checks if the clamp is closed at the station from the PLC. Lots of the PLC code makes the code run really slow
        # clampClosed = readPLC("Program:Sta120.Station.Cycle.Step.Bit[10]")
        clampClosed = False

        recorded, record = timeObject.log(result, clampClosed) #takes the result and finds the time it takes for each part to appear

        # write PLC value to the HMI
        # writePLC("Camera_Output.5", result)

        # # print(arr)
        # # print(final)

        # transferToPLC("OP100", result) #sending results to PLC
        cv.waitKey(1)

        # send the POST request contains the errors, result and the timing to the server
        url = 'http://127.0.0.1:5000/bt1xx/post-result/120/'

        # request_headers = {
        #     'Content-Type' : 'application/json'
        # }

        # request_body = {
        #     'message' : 'Sending error, pass/fail rates and timing to the server!',
        #     'station_number' : '120',
        #     'passref' : camera.passref,
        #     'error' : error,
        #     'result' : result,
        #     'timing' : record
        # }

        # request_json = json.dumps(request_body)

        # response = requests.post(url, headers=request_headers, data=request_json)

        frame = cv.pyrDown(frame)
        cv.imshow(camera.name, frame)

        #Code below is commented out for testing. During main implementation, this code will stall while the station is not
        #safe to enter. Once it is, it will reset the timing and proceed.
        
        # if recorded is True:
        #     while readPLC("Sta120_OK_To_Enter") is False:
        #         pass
        #     timeObject = timeLog(camera.station, camera.parts)
                