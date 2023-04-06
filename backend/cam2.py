#THis is cam1.py except it has a try except
import cv2 as cv
import time
import depthai as dai
from imageProcessingClasses import imageProcessing
from imagePredictionClass import MSEStabilization
from imageCalibrationClass import Recalibration, createPipeline
from pylogix import PLC
from PLCUpdate import writePLC, readPLC
from imageTimingClasses import timeLog
import cProfile

camera = Recalibration("station100")
device_info = dai.DeviceInfo(camera.IP)

while True:
    try:  
        with dai.Device(createPipeline(), device_info) as device:
            camera.adjustCamera(device)
            # camera.pressKeyCapture(device, camera.standardPath)
            # camera.errorSetup(device)
            # print("final error:")
            # print(camera.passref)
            # camera.updateJson(camera.station)
            processingObject = imageProcessing("station100")
            timeObject = timeLog(camera.station, camera.parts)
            
            while True:     
                
                img = camera.capture(device)
                processingObject.setTestImg(img)
                error = processingObject.compareImage()
                frame = processingObject.displayResultPosition()     
                prediction = MSEStabilization(error, camera.passref, len(camera.parts)) 
                result = prediction.result()

                print("Check clamp start")
                start = time.time()
                clampClosed = readPLC("Program:Sta100.Station.Cycle.Step.Bit[10]")
                print("check clamp done")
                print(time.time() - start)

                start = time.time()
                recorded = timeObject.log(result, clampClosed)
                print("done")
                print(time.time()-start)
                
                recorded = True
                
                # write PLC value to the HMI
                print("transfer to PLC start")
                start = time.time()
                writePLC("Camera_Output.1", result)
                print("write to PLC done")
                print(time.time()-start)

                print(result)
                # transferToPLC("OP100", result)
                
                cv.waitKey(1)
                frame = cv.pyrDown(frame)
                cv.imshow(camera.IP, frame)

                if recorded is True:
                    while readPLC("Sta100_OK_To_Enter") is False:
                        pass
                    timeObject = timeLog(camera.station, camera.parts)
    except:
        print(f"Retrying to reconnect to the device with {device_info}!")
        pass