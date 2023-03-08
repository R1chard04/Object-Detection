from calibrations import Recalibration, createPipeline
import cv2 as cv
import depthai as dai
camera = Recalibration("station10")

device_info = dai.DeviceInfo(camera.IP)

with dai.Device(createPipeline(), device_info) as device:
    camera.adjustCamera(device)
    print("press c to capture a standard picture")
    camera.pressKeyCapture(device, camera.standardPath)
    print("press c to start setting errors")
    camera.errorSetup(device)
    camera.updateJson(camera.station)
