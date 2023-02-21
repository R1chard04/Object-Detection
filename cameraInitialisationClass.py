import cv2 as cv
from pathlib import Path
import depthai as dai

class initialise:
    def __init__(self, photosFolderPath) -> None:
        self.photosFolderPath = photosFolderPath

    def initialise(self) -> any:
        #Photos directory 
        Path(self.photosFolderPath).mkdir(parents=True, exist_ok=True)

        #Camera initialisation
        pipeline = dai.Pipeline()
        pipeline_1 = dai.Pipeline()


        # pipeline
        camRgb = pipeline.create(dai.node.ColorCamera)
        # specify which board socket to use
        camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
        # set sensor resolution
        camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_4_K)
        # camRgb.initialControl.setManualFocus(100)

        # pipeline 1
        camRgb1 = pipeline_1.create(dai.node.ColorCamera)
        camRgb1.setBoardSocket(dai.CameraBoardSocket.RGB)
        camRgb1.setResolution(dai.ColorCameraProperties.SensorResolution.THE_4_K)

        # pipeline
        xoutRgb = pipeline.create(dai.node.XLinkOut)
        xoutRgb.setStreamName("rgb")
        camRgb.video.link(xoutRgb.input)

        # pipeline 1
        xoutRgb1 = pipeline_1.create(dai.node.XLinkOut)
        xoutRgb1.setStreamName("rgb1")
        camRgb1.video.link(xoutRgb1.input)

        # pipeline
        xin = pipeline.create(dai.node.XLinkIn)
        xin.setStreamName("control")
        xin.out.link(camRgb.inputControl)

        # pipeline 1
        xin1 = pipeline_1.create(dai.node.XLinkIn)
        xin1.setStreamName("control")
        xin1.out.link(camRgb1.inputControl)


        # Properties
        # pipeline
        videoEnc = pipeline.create(dai.node.VideoEncoder)
        videoEnc.setDefaultProfilePreset(1, dai.VideoEncoderProperties.Profile.MJPEG)
        camRgb.still.link(videoEnc.input)

        # pipeline 1
        videoEnc1 = pipeline_1.create(dai.node.VideoEncoder)
        videoEnc1.setDefaultProfilePreset(1, dai.VideoEncoderProperties.Profile.MJPEG)
        camRgb1.still.link(videoEnc1.input)

        # Linking
        # pipeline
        xoutStill = pipeline.create(dai.node.XLinkOut)
        xoutStill.setStreamName("still")
        videoEnc.bitstream.link(xoutStill.input)

        # pipeline 1
        xoutStill1 = pipeline_1.create(dai.node.XLinkOut)
        xoutStill1.setStreamName("still 1")
        videoEnc1.bitstream.link(xoutStill1.input)

        return self.photosFolderPath, pipeline, camRgb, xoutRgb, xin, videoEnc, xoutStill, pipeline_1