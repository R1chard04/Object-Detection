import cv2 as cv
import datetime
import depthai as dai
import os

def clamp(num, v0, v1):
    return max(v0, min(num, v1))

class imageCapture:
    def __init__(self, qRgb, qStill, qControl) -> None:
        self.qRgb = qRgb
        self.qStill = qStill
        self.qControl = qControl

    def setParameters(self):
        lensPos = 150
        brightness = 0
        BRIGHT_STEP = 1
        LENS_STEP = 3

        while True:
            inRgb = self.qRgb.tryGet() 

            if inRgb is not None:
                img = inRgb.getCvFrame()
                img = cv.pyrDown(img)
                img = cv.pyrDown(img)
                cv.imshow("rgb", img)

            key = cv.waitKey(1)
            # focal length adjestment
            if key in [ord(','), ord('.')]:
                if key == ord(','):
                    lensPos -= LENS_STEP
                if key == ord('.'):
                    lensPos += LENS_STEP
                lensPos = clamp(lensPos, 0, 255)
                print("Setting manual focus, lens position: ", lensPos)
                ctrl = dai.CameraControl()
                ctrl.setManualFocus(lensPos)
                self.qControl.send(ctrl)
            
            # brightness adjestment
            if key in [ord('k'), ord('l')]:
                if key == ord('k'):
                    brightness -= BRIGHT_STEP
                if key == ord('l'):
                    brightness += BRIGHT_STEP
                brightness = clamp(brightness, -10, 10)
                print("Brightness:", brightness)
                ctrl = dai.CameraControl()
                ctrl.setBrightness(brightness)
                self.qControl.send(ctrl)
            
            if key == ord('ENTER'):
                return brightness, lensPos
            
            ctrl = dai.CameraControl()
            ctrl.setManualFocus(lensPos)
            ctrl.setBrightness(brightness)
            ctrl.setCaptureStill(True)
            self.qControl.send(ctrl)

    def autoCapture(self, imgPath, directoryName, brightness, focalLength):
        
        lensPos = clamp(focalLength, 0, 255)
        brightness = clamp(brightness, -10, 10)
    
        while True:
            img = 1  #instantiates img
            imgUpdated = False #img updated condition

            inRgb = self.qRgb.tryGet() 
            
            if imgPath == "Test":
                imgPath = round(float(((str(datetime.datetime.now()).replace("-","")).replace(" ","")).replace(":","")))
            
            imgPath = os.path.join(directoryName,imgPath)

            if inRgb is not None:
                img = inRgb.getCvFrame()
                img = cv.pyrDown(img)
                img = cv.pyrDown(img)
                
                cv.imshow("rgb", img)

            if self.qStill.has():
                with open(imgPath, "wb") as f:
                    f.write(self.qStill.get().getData())
                    print('Image saved to', imgPath)
                    imgUpdated = True

            ctrl = dai.CameraControl()
            ctrl.setManualFocus(lensPos)
            ctrl.setBrightness(brightness)
            ctrl.setCaptureStill(True)

            self.qControl.send(ctrl)
            print("Sent 'still' event to the camera!")
            
            if imgUpdated == True:
                return img, imgPath