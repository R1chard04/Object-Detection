import cv2 as cv
import datetime
import depthai as dai
import os
import time
from imageProcessingClasses import imageProcessing

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
        # i = 0
        while True:
            # i+=1
            # print(i)
            inRgb = self.qRgb.tryGet() 

            if inRgb is not None:
                frame = inRgb.getCvFrame()
                cv.imshow("rgb", cv.resize(frame,(0,0), fx = 0.2, fy = 0.2))

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
                cv.destroyAllWindows()
                return
                # return brightness, lensPos
            
            # print("hablabla")
            # ctrl = dai.CameraControl()
            # ctrl.setCaptureStill(True)
            # self.qControl.send(ctrl)

    def autoCapture(self, imgPath, directoryName, processingObject):
        capture = time.time()
        print("START")
        while True:
            # img = 1  #instantiates img
            imgUpdated = False #img updated condition
            inRgb = self.qRgb.tryGet() 
            
            # if imgPath == "Test":
            #     imgPath = str(round(float(((str(datetime.datetime.now()).replace("-","")).replace(" ","")).replace(":",""))))+".jpg"
            
            # path = os.path.join(directoryName,imgPath)

            if inRgb is not None:
                frame = inRgb.getCvFrame()
                frame = cv.pyrDown(frame)
                frame = cv.pyrDown(frame)
                cv.imshow("captured", frame)     

            if self.qStill.has():
                fName = "Object_Detection\Photos\FRAME.jpg"
                with open(fName, "wb") as f:
                    f.write(self.qStill.get().getData())
                    # print('Image saved to', fName)
                    # imgUpdated = True
                img = cv.imread(fName)
                processingObject.setTestImg(img)
                error, diffImg = processingObject.compareImage()
                print(error)
            
            # print(time.time())
            key = cv.waitKey(1)
            # if self.qStill.has():
            #     dirname = os.path.dirname(path)
            #     if not os.path.exists(dirname):
            #         os.makedirs(dirname)
            #     with open(path, "wb") as f:
            #         f.write(self.qStill.get().getData())
                    # print('Image saved to', path)
                    # imgUpdated = True
            if (time.time() - capture) > 0.2:
                capture = time.time()
                ctrl = dai.CameraControl()
                ctrl.setCaptureStill(True)
                self.qControl.send(ctrl)
                # print("Sent 'still' event to the camera!")
            elif key == ord('q'):
                break
            # # print("not here")
            # if imgUpdated == True:
            #     return img, imgPath