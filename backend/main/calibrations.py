import json
import depthai as dai
import cv2 as cv
import time
from main.imageMaskGeneration import createMask
import pdb

def createPipeline():
    pipeline = dai.Pipeline()
    # This might improve reducing the latency on some systems
    pipeline.setXLinkChunkSize(0)

    # Define source and output
    camRgb = pipeline.create(dai.node.ColorCamera)
    camRgb.setFps(3)
    camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
    camRgb.setPreviewSize(1920, 1080)

    xout = pipeline.create(dai.node.XLinkOut)
    xout.setStreamName("out")
    camRgb.isp.link(xout.input)
    return pipeline

# def cameraSetup(station):
#     stationCamera = Recalibration(station)
#     device_info = dai.DeviceInfo(stationCamera.IP)
#     with dai.Device(createPipeline(), device_info) as device:
#         # stationCamera.paramSetup()
#         # render website?
#         stationCamera.maskSetup()
#         # render website?
#     return

# set up the mask, control and errors
class Recalibration:
    def __init__(self, station) -> None:
        with open (r'main/params.json') as f:
              partList = json.load(f)
              
        # select which station to use here
        params = partList[station]
        self.brightness = params["brightness"]
        self.lensPos = params["lensPos"]
        self.parts = params["parts"]
        self.IP = params["IP"]
        self.maskPaths = params["masks"]
        self.refPaths = params["refs"]
        self.colPaths = params ["cols"]
        self.standardPath = params["standard"]
        self.testPath = params["test"]
    def paramSetup(self):
        pass
    
    def maskSetup(self, device):
        q = device.getOutputQueue(name="out")
        i = 0           
        while i < len(self.parts):
            print("load" + self.parts[i] + "part.")
            startTime = time.time()
            while ((time.time()-startTime) < 3):
                imgFrame = q.get()
            imgSil = imgFrame.getCvFrame()
            cv.imwrite(self.refPaths[i], imgSil)
            
            input("load"+ self.parts[i] + "colour part.")
            startTime = time.time()
            while ((time.time()-startTime) < 3):
                imgFrame = q.get()
            imgFrame = q.get()
            imgCol = imgFrame.getCvFrame()
            
            cv.imwrite(self.colPaths[i], imgCol)
            
            print("Creating a mask, this may take a minute")
            if createMask(imgSil, imgCol, self.maskPaths[i]):
                i += 1
                print("Mask generated")
            else:
                print(f"Mask is redoing!")
        
        print("all masks are done")
        return
                
    def upDate(self, station):
        # this method read all the parameters from the json again
        with open (r'params.json') as f:
              partList = json.load(f)
              
        # select which station to use here
        params = partList[station]
        self.brightness = params["brightness"]
        self.lensPos = params["lensPos"]
        self.parts = params["parts"]
        self.IP = params["IP"]
        self.maskPaths = params["masks"]
        self.refPaths = params["refs"]
        self.colPaths = params ["cols"]
        self.standardPath = params["standard"]
        self.testPath = params["test"]
    
    def errorSetup(self):
        pass
    
    def controlSetup(self):
        pass
    
        
