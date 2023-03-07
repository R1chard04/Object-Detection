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
    xin = pipeline.create(dai.node.XLinkIn)
    xin.setStreamName("control")
    xin.out.link(camRgb.inputControl)
    camRgb.isp.link(xout.input)
    return pipeline

def clamp(num, v0, v1):
    return max(v0, min(num, v1))

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
        self.station = station
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
        self.errDir = params["errDir"]
        
    def paramSetup(self, device):
        q = device.getOutputQueue(name="out")
        qControl = device.getInputQueue(name="control")
        
        while True:
            frame = q.get().getCvFrame()
            frame = cv.pyrDown(frame)
            frame = cv.pyrDown(frame)
            cv.imshow(self.station, frame)
            
            key = cv.waitKey(1)
            
            # focal length adjustment
            if key in [ord(','), ord('.')]:
                if key == ord(','):
                    self.lensPos -= 2
                elif key == ord('.'):
                    self.lensPos += 2
                self.lensPos = clamp(self.lensPos, 0, 255)
                print("Setting manual focus, lens position: ", self.lensPos)
                ctrl = dai.CameraControl()
                ctrl.setManualFocus(self.lensPos)
                qControl.send(ctrl)
            # brightness adjustment
            elif key in [ord('k'), ord('l')]:
                if key == ord('k'):
                    self.brightness -= 1
                elif key == ord('l'):
                    self.brightness += 1
                self.brightness = clamp(self.brightness, -10, 10)
                print("Brightness:", self.brightness)
                ctrl = dai.CameraControl()
                ctrl.setBrightness(self.brightness)
                qControl.send(ctrl) 
            
            if key == ord('q'):
                # update britness and lesPos to json file
                return self.brightness, self.lensPos
    
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
                
    def upDateParams(self, station):
        # this method read all the parameters from the json again
        with open (r'main/params.json', 'r') as f:
              partList = json.load(f)
              
        # select which station to use here
        params = partList[station]
        self.brightness = params["brightness"]
        self.lensPos = params["lensPos"]

    def updateJson(self, station, new_brightness, new_lensPos):
        # this function set all the values in the json
        with open(r'main/params.json', 'r') as f:
            partList = json.load(f)
        
        # change the settings in json
        
        partList[station]["brightness"] = new_brightness
        partList[station]["lensPos"] = new_lensPos

        with open('main/params.json', 'w') as f:
            json.dump(partList, f, indent=4)

        print(f"Update values of the brightness and focal length")
       
    def errorSetup(self, device):
        q = device.getOutputQueue(name="out")
        startTime = time.time()
        while ((time.time()-startTime) < 3):
            imgFrame = q.get()  
        
        input("press any key to start setting up error:")
        for i in range(10):
            imgFrame = q.get().getCvFrame()
            cv.imwrite(self.colPaths[i], imgFrame)
        pass
    
    def controlSetup(self, device):
        q = device.getOutputQueue(name="out")
        i = 0           
        while i < len(self.parts):
            print("load" + self.parts[i] + "part.")
            startTime = time.time()
            while ((time.time()-startTime) < 3):
                imgFrame = q.get()
            imgSil = imgFrame.getCvFrame()
            cv.imwrite(self.refPaths[i], imgSil)
        pass
    
    
    # this function should be called when the camera get turned on
    # it will adjust the camera to the brightness and lensPos 
    def adjustCamera(self, device):
        
        q = device.getOutputQueue(name="out")
        qControl = device.getInputQueue(name="control")
        
        print("Setting manual focus, lens position: ", self.lensPos)
        ctrl = dai.CameraControl()
        ctrl.setManualFocus(self.lensPos)
        qControl.send(ctrl)
        
        print("Brightness:", self.brightness)
        ctrl = dai.CameraControl()
        ctrl.setBrightness(self.brightness)
        qControl.send(ctrl)
        
        startTime = time.time()
        while ((time.time()-startTime) < 10):
            imgFrame = q.get().getCvFrame()
            imgFrame = cv.pyrDown(imgFrame)
            imgFrame = cv.pyrDown(imgFrame)
            cv.imshow("it'shere", imgFrame)
            cv.waitKey(1)
        
        # auto white balance lock
        print("auto white balance lock")
        ctrl = dai.CameraControl()
        ctrl.setAutoWhiteBalanceLock(True)
        qControl.send(ctrl)

        # auto exposure lock
        print("auto exposure lock")
        ctrl = dai.CameraControl()
        ctrl.setAutoExposureLock(True)
        qControl.send(ctrl)
        
        # while True:
        #     imgFrame = q.get().getCvFrame()
        #     imgFrame = cv.pyrDown(imgFrame)
        #     imgFrame = cv.pyrDown(imgFrame)
        #     cv.imshow("results", imgFrame)
        #     key = cv.waitKey(1)
        #     if key == ord('q'):
        #         break
        return
        
    # this function capture an image and return it    
    def capture(self, device):
        q = device.getOutputQueue(name="out")
        imgFrame = q.get().getCvFrame()
        return imgFrame

    def pressKeyCapture(self, device):
        pass