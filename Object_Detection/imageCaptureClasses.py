import cv2 as cv
import os
from os import listdir
import os.path
import datetime
from pathlib import Path
import depthai as dai
from imageMaskGeneration import recalibrate

class initialise:
    def __init__(self, photosFolderPath) -> None:
        self.photosFolderPath = photosFolderPath

    def initialise(self):
        #Photos directory 
        Path(self.photosFolderPath).mkdir(parents=True, exist_ok=True)

        #Camera initialisation
        pipeline = dai.Pipeline()

        camRgb = pipeline.create(dai.node.ColorCamera)
        camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
        camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_4_K)

        xoutRgb = pipeline.create(dai.node.XLinkOut)
        xoutRgb.setStreamName("rgb")
        camRgb.video.link(xoutRgb.input)

        xin = pipeline.create(dai.node.XLinkIn)
        xin.setStreamName("control")
        xin.out.link(camRgb.inputControl)

        # Properties
        videoEnc = pipeline.create(dai.node.VideoEncoder)
        videoEnc.setDefaultProfilePreset(1, dai.VideoEncoderProperties.Profile.MJPEG)
        camRgb.still.link(videoEnc.input)

        # Linking
        xoutStill = pipeline.create(dai.node.XLinkOut)
        xoutStill.setStreamName("still")
        videoEnc.bitstream.link(xoutStill.input)

        return self.photosFolderPath, pipeline, camRgb, xoutRgb, xin, videoEnc, xoutStill

class imageCapture:
    def __init__(self, qRgb, qStill, qControl, photosDirectoryName) -> None:
        self.qRgb = qRgb
        self.qStill = qStill
        self.qControl = qControl
        self.directoryName = photosDirectoryName

    def autoCapture(self):
        while True:
            img = 1  #instantiates img
            imgUpdated = False #img updated condition

            inRgb = self.qRgb.tryGet() 

            now = round(float(((str(datetime.datetime.now()).replace("-","")).replace(" ","")).replace(":","")))
            imgPath = f"{self.directoryName}/{now}.jpg"

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

    def maskCapture(self):
        photoName = "null.jpg"
        dirName = "mask_pics"
        Path(dirName).mkdir(parents=True, exist_ok=True)

        print ("Press \'s\' to capture a standard photo that has parts on \nPress \'n\' to capture a photo that does not have parts on \nPress \'g\' to generate a mask\nPress \'q\' to quit")
        # take STANDARD
        while True:
            inRgb = self.qRgb.tryGet()  # Non-blocking call, will return a new data that has arrived or None otherwise
            if inRgb is not None:
                frame = inRgb.getCvFrame()
                # 4k / 4
                frame = cv.pyrDown(frame)
                frame = cv.pyrDown(frame)
                cv.imshow("rgb", frame)

            if self.qStill.has():
                fName = f"{dirName}/{photoName}.jpg"
                with open(fName, "wb") as f:
                    f.write(self.qStill.get().getData())
                    print('Image saved to', fName)
            
            key = cv.waitKey(1)
            if key == ord('q'):
                break
            elif key == ord('s'):
                photoName = "STANDARD"
                # dirName = "mask_pics"
                ctrl = dai.CameraControl()
                ctrl.setCaptureStill(True)
                self.qControl.send(ctrl)
                print("Sent 'still' event to the camera")
            elif key == ord('n'):
                photoName = "NONE"
                # dirName = "mask_pics"
                ctrl = dai.CameraControl()
                ctrl.setCaptureStill(True)
                self.qControl.send(ctrl)
                print("Sent 'still' event to the camera")
            elif key == ord('g'):
                partImg = cv.imread('mask_pics/STANDARD.jpg') # ?? img
                noPartImg = cv.imread('mask_pics/NONE.jpg')        # ?? no
                maskPath = "Object_Detection\photos\mask.jpg" #This has to be fixed

                maskCalibrationObject = recalibrate(noPartImg, partImg, maskPath)
                mask = maskCalibrationObject.maskGeneration() #this might not need to return anything

            elif key == ord('q'):
                break

            