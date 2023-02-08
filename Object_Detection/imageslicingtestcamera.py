import cv2 as cv
import time
import numpy
import depthai as dai
from cameraInitialisationClass import initialise
from imageProcessingClasses import imageProcessing
from imageCaptureClasses import imageCapture
from imageMaskGeneration import recalibrate
from imageCalibration import imageCalibration
from imageStitchingClasses import imageStitching
from imageSlicing import imageSlicing

photosPath = "Object_Detection\Photos\Masking\INIT"

needCalibrate = False

initialisationObject = initialise(photosPath)
photoDirectoryName, pipeline, camRgb, xoutRgb, xin, videoEnc, xoutStill, pipeline_1 = initialisationObject.initialise()

for device in dai.Device.getAllAvailableDevices():
    print(f"{device.getMxId()} {device.state}")
    
device_info = dai.DeviceInfo("19443010A137DE1200")
device_info.state = dai.XLinkDeviceState.X_LINK_BOOTLOADER
device_info.protocol = dai.XLinkProtocol.X_LINK_TCP_IP

total_device_info = [device_info]
total_pipeline = [pipeline]

with dai.Device(pipeline) as device:
    captureObject = imageCapture(device.getOutputQueue(name="rgb", maxSize=30, blocking=False), 
                                device.getOutputQueue(name="still", maxSize=30, blocking=True), 
                                device.getInputQueue(name="control"))
    while True:
        testImg, testImgPath = captureObject.autoCapture("Test", photosPath, brightness, lensPos)
        img_slicer = imageSlicing(testImg)
        result = img_slicer.imageSlicing()
        for i, res in enumerate(result):
                window_height = int(res.shape[0] * 0.7)
                window_width = int(res.shape[1] * 0.7)
                cv.namedWindow(f"Quadrant {i+1}", cv.WINDOW_NORMAL)
                cv.resizeWindow(f"Quadrant {i+1}", window_width, window_height)
                cv.imshow(f"Quadrant {i+1}", res)


