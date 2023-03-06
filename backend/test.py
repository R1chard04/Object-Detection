from main.calibrations import Recalibration, createPipeline
import cv2 as cv
import depthai as dai
camera = Recalibration("station10")

device_info = dai.DeviceInfo(camera.IP)
with dai.Device(createPipeline(), device_info) as device:
    camera.paramSetup(device)
