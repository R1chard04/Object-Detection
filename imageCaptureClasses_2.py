import cv2 as cv
import datetime
import depthai as dai
import os
import time
from imageProcessingClasses import imageProcessing

# A function to ensure lens and brightness adjestment does not go out of range
def clamp(num, v0, v1):
    return max(v0, min(num, v1))

class imageCapture:
    def __init__(self, qRgb, qStill, qControl) -> None:
        self.qRgb = qRgb
        self.qStill = qStill
        self.qControl = qControl
        self.MSEresults = 0

    # Camera calibration
    def setParameters(self, name):
        lensPos = 108
        brightness = -1
        BRIGHT_STEP = 1
        LENS_STEP = 3
        awb_lock = False
        ae_lock = False
        
        while True:
    
            inRgb = self.qRgb.tryGet() 

            # streaming the frame
            if inRgb is not None:
                frame = inRgb.getCvFrame()
                frame = cv.pyrDown(frame)
                frame = cv.pyrDown(frame)
                cv.imshow(name, frame)

            key = cv.waitKey(1)
            
            # focal length adjestment
            if key in [ord(','), ord('.')]:
                if key == ord(','):
                    lensPos -= LENS_STEP
                elif key == ord('.'):
                    lensPos += LENS_STEP
                lensPos = clamp(lensPos, 0, 255)
                print("Setting manual focus, lens position: ", lensPos)
                ctrl = dai.CameraControl()
                ctrl.setManualFocus(lensPos)
                self.qControl.send(ctrl)
            
            # brightness adjestment
            elif key in [ord('k'), ord('l')]:
                if key == ord('k'):
                    brightness -= BRIGHT_STEP
                elif key == ord('l'):
                    brightness += BRIGHT_STEP
                brightness = clamp(brightness, -10, 10)
                print("Brightness:", brightness)
                ctrl = dai.CameraControl()
                ctrl.setBrightness(brightness)
                self.qControl.send(ctrl) 
                
            # lock/unlock auto white balance
            elif key == ord('1'):
                awb_lock = not awb_lock
                print("Auto white balance lock:", awb_lock)
                ctrl = dai.CameraControl()
                ctrl.setAutoWhiteBalanceLock(awb_lock)
                self.qControl.send(ctrl) 
                
            # lock/unlock auto exposure
            elif key == ord('2'):
                ae_lock = not ae_lock
                print("Auto exposure lock:", ae_lock)
                ctrl = dai.CameraControl()
                ctrl.setAutoExposureLock(ae_lock)
                self.qControl.send(ctrl) 
            
            if key == ord("q"):
                return brightness, lensPos
                
    def autoCapture(self, imgName, directoryName):
        capture = time.time()
        imgCaptured = False #img updated condition

        while not imgCaptured:
            
            if imgName == "Test":
                imgName = str(round(float(((str(datetime.datetime.now()).replace("-","")).replace(" ","")).replace(":",""))))+".jpg"
            
            path = os.path.join(directoryName,imgName)
                
            if self.qStill.has():
                with open(path, "wb") as img:
                    img.write(self.qStill.get().getData())
                
                    img = cv.imread(path)
                    return path
                    
            key = cv.waitKey(1)

            if (time.time() - capture) > 0.3:
                capture = time.time()
                ctrl = dai.CameraControl()
                ctrl.setCaptureStill(True)
                self.qControl.send(ctrl)
        
    def captureImage(self, path):
    
        imgUpdated = False
        img = 1

        while not imgUpdated:
            # inRgb = self.qRgb.tryGet() 
            
            # if inRgb is not None:
            #     frame = inRgb.getCvFrame()
            #     frame = cv.pyrDown(frame)
            #     frame = cv.pyrDown(frame)
            #     cv.imshow("captured", frame)     
            

            if self.qStill.has():
                with open(path, "wb") as f:
                    f.write(self.qStill.get().getData())
                    imgUpdated = True

                    img = cv.imread(path)
                    return img

            key = cv.waitKey(1)  
            if key == ord('c'):
                ctrl = dai.CameraControl()
                ctrl.setCaptureStill(True)
                self.qControl.send(ctrl)

    def captureOne(self, path, brightness, lensPos, IP):
    
        imgUpdated = False
        img = 1

        while not imgUpdated:
            inRgb = self.qRgb.tryGet() 
            
            # if inRgb is not None:
            #     frame = inRgb.getCvFrame()
            #     frame = cv.pyrDown(frame)
            #     frame = cv.pyrDown(frame)
            #     cv.imshow(IP, frame)     
            

            if self.qStill.has():

                ctrl = dai.CameraControl()
                ctrl.setBrightness(brightness)
                self.qControl.send(ctrl) 

                ctrl = dai.CameraControl()
                ctrl.setManualFocus(lensPos)
                self.qControl.send(ctrl)
                
                with open(path, "wb") as f:
                    f.write(self.qStill.get().getData())
                    imgUpdated = True

            cv.waitKey(1)  
            ctrl = dai.CameraControl()
            ctrl.setCaptureStill(True)
            self.qControl.send(ctrl)
    
        img = cv.imread(path)
        return img
        
                