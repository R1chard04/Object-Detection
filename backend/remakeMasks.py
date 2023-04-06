#Manual mask making that was used in testing a lot.
import cv2 as cv
import time
import depthai as dai
from imageProcessingClasses import imageProcessing
from imagePredictionClass import MSEStabilization
from imageCalibrationClass import Recalibration, createPipeline
# from imageTimingClasses import imageTiming
# from imageAverageClasses import imageAverage
import time
import cv2 as cv
import depthai as dai
import pdb
# import pylogix 
from pylogix import PLC
from PLCUpdate import writePLC
from imageMaskGeneration import createMask

camera = Recalibration("station120")
device_info = dai.DeviceInfo(camera.IP)

# with dai.Device(createPipeline(), device_info) as device:
#     # camera.paramSetup(device)
#     # camera.updateJson(camera.station)
#     camera.adjustCamera(device)
#     camera.maskSetup(device)
#     # processingObject = imageProcessing("station100")

# cv.imshow("this", imgSil)
# cv.waitKey(0)

for i in range(len(camera.parts)):
    print(camera.parts[i])
    imgSil = cv.imread(camera.refPaths[i])
    imgCol = cv.imread(camera.colPaths[i])
    print(camera.maskPaths[i])
    createMask(imgSil, imgCol, camera.maskPaths[i])
