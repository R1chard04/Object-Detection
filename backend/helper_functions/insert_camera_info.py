# This is a helper function that help getting the pipeline to connect the laptop to the device
import depthai as dai

def cameraInitialisation() -> any:
  #Camera initialisation
  pipeline = dai.Pipeline()

  # pipeline
  camRgb = pipeline.create(dai.node.ColorCamera)
  # specify which board socket to use
  camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
  # set sensor resolution
  camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
  camRgb.setFps(2)
  # camRgb.initialControl.setManualFocus(100)

  # pipeline
  xoutRgb = pipeline.create(dai.node.XLinkOut)
  xoutRgb.setStreamName("rgb")
  camRgb.video.link(xoutRgb.input)

  # pipeline
  xin = pipeline.create(dai.node.XLinkIn)
  xin.setStreamName("control")
  xin.out.link(camRgb.inputControl)

  # Properties
  # pipeline
  videoEnc = pipeline.create(dai.node.VideoEncoder)
  videoEnc.setDefaultProfilePreset(1, dai.VideoEncoderProperties.Profile.MJPEG)
  camRgb.still.link(videoEnc.input)

  # Linking
  # pipeline
  xoutStill = pipeline.create(dai.node.XLinkOut)
  xoutStill.setStreamName("still")
  videoEnc.bitstream.link(xoutStill.input)

  return pipeline


# This is a helper function that help insert the name of the device connected and the IP address associated with the station number
def insert_camera_info(station_number) -> tuple:
 if(station_number == 5):
  name = "19443010613C6E1300"
  IP = "169.254.1.201"
  return name, IP
 elif(station_number == 10):
  name = "1844301051B53C1300"
  IP = "169.254.1.202"
  return name, IP
 elif(station_number == 100):
  name = "1944301051766E1300"
  IP = "169.254.1.203"
  return name, IP
 

 