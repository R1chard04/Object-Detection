import cv2 as cv
import os
from os import listdir
import os.path
import datetime
from pathlib import Path
import depthai as dai

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
    def __init__(self, qRgb, qStill, qControl, directoryName) -> None:
        self.qRgb = qRgb
        self.qStill = qStill
        self.qControl = qControl
        self.directoryName = directoryName

    def capture(self) -> any:
        inRgb = self.qRgb.tryGet() 
        global frame, fName
        frame, fName = any
        if inRgb is not None:
            frame = inRgb.getCvFrame()
            frame = cv.pyrDown(frame)
            frame = cv.pyrDown(frame)

        if self.qStill.has():
            now = round(float(((str(datetime.datetime.now()).replace("-","")).replace(" ","")).replace(":","")))
            fName = f"{self.directoryName}/{now}.jpg"
            with open(fName, "wb") as f:
                f.write(self.qStill.get().getData())
                print('Image saved to', fName)

        ctrl = dai.CameraControl()
        ctrl.setCaptureStill(True)
        self.qControl.send(ctrl)
        print("Sent 'still' event to the camera!")

        return frame, fName