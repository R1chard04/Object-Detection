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

db_config = {
    "hostname": "localhost",
    "database": "imageTiming",
    "username": "postgres",
    "pwd": "W1nter@2023Hydro",
    "port_id": 5432
}

camera = Recalibration("station100")
processingObject = imageProcessing("station100")

device_info = dai.DeviceInfo(camera.IP)

with dai.Device(createPipeline(), device_info) as device:
    camera.adjustCamera(device)
    
    print("start")
    
    # ask user to name each occurance in array
    assigned_names = [1, 2, 3, 4]
    print(assigned_names)

    timing = imageTiming(assigned_names, db_config)

    arr = [0, 0, 0, 0]
    
    while True:     
        
        img = camera.capture(device)
        processingObject.setTestImg(img)
        frame = processingObject.displayResultPosition()
        error = processingObject.compareImage()
        prediction = MSEStabilization(error, camera.passref, len(camera.parts)) 

        result = prediction.result()
        response = timing.record(result)
        calculation = imageAverage(db_config)
        final = calculation.average()
        
        
        print(result)

        # transferToPLC("OP100", result)
        cv.waitKey(1)
        frame = cv.pyrDown(frame)
        frame = cv.pyrDown(frame)
        cv.imshow(camera.IP, frame)