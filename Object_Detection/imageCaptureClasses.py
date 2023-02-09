import cv2 as cv
import datetime
import depthai as dai
import os
import time
from imageProcessingClasses import imageProcessing
from imageSlicing import imageSlicing

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
        img = 1
        imgUpdated = False
        
        while True:
    
            inRgb = self.qRgb.tryGet() 

            if inRgb is not None:
                frame = inRgb.getCvFrame()
                cv.imshow("rgb", cv.resize(frame,(0,0), fx = 0.2, fy = 0.2))

            if self.qStill.has():
                dirName = "Object_Detection\Photos\MASKS"
                fName = f"{dirName}/{int(time.time() * 1000)}.jpg"
                with open(fName, "wb") as f:
                    f.write(self.qStill.get().getData())
                    print('Image saved to', fName)

                    imgUpdated = True
                    img = cv.imread(fName)

                    if imgUpdated is True:
                        cv.destroyAllWindows()
                        return brightness, lensPos, img

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
            
            if key == ord("q"):
                
                ctrl = dai.CameraControl()
                ctrl.setCaptureStill(True)
                self.qControl.send(ctrl)
                print("Sent 'still' event to the camera!")
                

    def autoCapture(self, imgPath, directoryName, processingObject):
        capture = time.time()

        errorAcheived = False #img updated condition
        error = 0
        tolerance = 0
        resultArray = []

        while not errorAcheived:
            inRgb = self.qRgb.tryGet() 
            
            if imgPath == "Test":
                imgPath = str(round(float(((str(datetime.datetime.now()).replace("-","")).replace(" ","")).replace(":",""))))+".jpg"
            
            path = os.path.join(directoryName,imgPath)
            diffPath = os.path.join("Object_Detection\Photos\DIFF", imgPath)

            if inRgb is not None:
                frame = inRgb.getCvFrame()
                frame = cv.pyrDown(frame)
                frame = cv.pyrDown(frame)
                cv.imshow("captured", frame)
                
            if self.qStill.has():
                fName = path
                with open(fName, "wb") as f:
                    f.write(self.qStill.get().getData())

                    # img_slicer = imageSlicing(cv.imread(path))
                    # result = img_slicer.imageSlicing()

                    # for i in range(len(result)):
                    processingObject.setTestImg(cv.imread(fName))
                    error, diffImg = processingObject.compareImage()
                    cv.imwrite(diffPath,diffImg)
                    print(error)

                        # if error < tolerance:
                        #     resultArray[i] = 1

            key = cv.waitKey(1)
            if (time.time() - capture) > 0.3:
                capture = time.time()
                ctrl = dai.CameraControl()
                ctrl.setCaptureStill(True)
                self.qControl.send(ctrl)
        
        return resultArray

    def captureImage(self, path):
    
        imgUpdated = False
        img = 1

        while not imgUpdated:
            inRgb = self.qRgb.tryGet() 
            
            if inRgb is not None:
                frame = inRgb.getCvFrame()
                frame = cv.pyrDown(frame)
                frame = cv.pyrDown(frame)
                cv.imshow("captured", frame)     

            if self.qStill.has():
                fName = path
                with open(fName, "wb") as f:
                    f.write(self.qStill.get().getData())
                    imgUpdated = True
                    
                    return
    
    def getFrame(self, name="rgb"):
        if name == "rgb":
            return self.qRgb.get()
        else:
            raise ValueError("Invalid name")