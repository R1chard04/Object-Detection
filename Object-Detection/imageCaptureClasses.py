import cv2 as cv
import os
from os import listdir
import os.path
import datetime
from pathlib import Path
import depthai as dai

class initialise:
    def __init__(self, reportPath, photosFolderPath) -> None:
        self.reportPath = reportPath
        self.photosFolderPath = photosFolderPath

    def initialise(self):
        #Report head
        report = open(self.reportPath, "a")
        report.write("Report of deviations from reference image")
        report.close()

        #Photos directory 
        Path(self.photosDirectoryPath).mkdir(parents=True, exist_ok=True)

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

        return self.photosDirectoryPath, pipeline, camRgb, xoutRgb, xin, videoEnc, xoutStill

class imageCapture:
    def __init__(self, qRgb, qStill, qControl, directoryName) -> None:
        self.qRgb = qRgb
        self.qStill = qStill
        self.qControl = qControl
        self.directoryName = directoryName

    def capture(self):
        inRgb = self.qRgb.tryGet()  # Non-blocking call, will return a new data that has arrived or None otherwise
        if inRgb is not None:
            frame = inRgb.getCvFrame()
            frame = cv.pyrDown(frame)
            frame = cv.pyrDown(frame)

        if self.qStill.has():
            now = round(float(((str(datetime.datetime.now()).replace("-","")).replace(" ","")).replace(":","")))
            fName = f"{self.directoryName}/{now}.jpeg"
            with open(fName, "wb") as f:
                f.write(self.qStill.get().getData())
                print('Image saved to', fName)

        ctrl = dai.CameraControl()
        ctrl.setCaptureStill(True)
        self.qControl.send(ctrl)
        print("Sent 'still' event to the camera!")

        return frame, fName



    

















#Pictures Name Generator
def timeStamp():
    now = str(datetime.datetime.now())
    now = round(float(((now.replace("-","")).replace(" ","")).replace(":","")))
    return now
