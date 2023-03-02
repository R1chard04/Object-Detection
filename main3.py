import cv2 as cv
import time
import depthai as dai
from cameraInitialisationClass import initialise
from imageProcessingClasses import imageProcessing
from imageCaptureClasses import imageCapture
from imageMaskGeneration import createMask
from imagePredictionClass import MSEStabilization, getPassRef
import time
import os
import json
import pdb

photosPath = "Photos\Init"

IP = dai.DeviceInfo("169.254.1.203")

initialisationObject = initialise(photosPath)
print("here1")
photoDirectoryName, pipeline, camRgb, xoutRgb, xin, videoEnc, xoutStill = initialisationObject.initialise()

for device in dai.Device.getAllAvailableDevices():
    print(f"{device.getMxId()} {device.state}")
# print(IP)
device_info = dai.DeviceInfo(IP)
device_info.state = dai.XLinkDeviceState.X_LINK_BOOTLOADER
device_info.protocol = dai.XLinkProtocol.X_LINK_TCP_IP
    

#----------------------Camera Capture Initialisation---------------------#
#This needs to be setup for multiple cameras
    
with dai.Device(pipeline, device_info) as device:
    captureObject = imageCapture(device.getOutputQueue(name="rgb", maxSize=30, blocking=False), 
                                device.getOutputQueue(name="still", maxSize=30, blocking=True), 
                                device.getInputQueue(name="control"))
    # brightness, lensPos = paramsSetup(selected, captureObject, recalibrate, IP)
    brightness = -1
    lensPos = 108
    print(IP)

# python main1.py& python main2.py& python main3.py&