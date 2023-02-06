import cv2 as cv
import datetime
import depthai as dai

class imageCapture:
    def __init__(self, qRgb, qStill, qControl) -> None:
        self.qRgb = qRgb
        self.qStill = qStill
        self.qControl = qControl

    def autoCapture(self, imgPath, directoryName):
        while True:
            img = 1  #instantiates img
            imgUpdated = False #img updated condition

            inRgb = self.qRgb.tryGet() 
            
            if imgPath == "Test":
                imgPath = round(float(((str(datetime.datetime.now()).replace("-","")).replace(" ","")).replace(":","")))
            
            imgPath = f"{self.directoryName}/{imgPath}.jpg"

            if inRgb is not None:
                img = inRgb.getCvFrame()
                img = cv.pyrDown(img)
                img = cv.pyrDown(img)
                imgUpdated = True
                 #comment out later

            if self.qStill.has():
                with open(imgPath, "wb") as f:
                    f.write(self.qStill.get().getData())
                    print('Image saved to', imgPath)

            ctrl = dai.CameraControl()
            ctrl.setCaptureStill(True)
            self.qControl.send(ctrl)
            print("Sent 'still' event to the camera!")
            
            if imgUpdated == True:
                return img, imgPath

    def displayCapture():