import cv2 as cv
import time
import depthai as dai
from imageProcessingClasses import imageProcessing
from imagePredictionClass import MSEStabilization
from imageCalibrationClass import Recalibration, createPipeline
from imageTimingClasses import imageTiming
# from imageAverageClasses import imageAverage
import time
import cv2 as cv
import depthai as dai
import pdb
import pylogix 
from pylogix import PLC
from PLCUpdate import writePLC

camera = Recalibration("station120")
device_info = dai.DeviceInfo(camera.IP)

with dai.Device(createPipeline(), device_info) as device:
    camera.adjustCamera(device)
    camera.maskSetup(device)
    # processingObject = imageProcessing("station100")
