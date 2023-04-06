import depthai as dai
from imageCalibrationClass import Recalibration, createPipeline

#Creating the pass reference array
def create_pass_ref(camera, device_info):
 with dai.Device(createPipeline(), device_info) as device:
     camera.adjustCamera(device)
     camera.pressKeyCapture(device, camera.standardPath)
     camera.errorSetup(device)
     print("final error:")
     print(camera.passref)

     camera.updateJson(camera.station)
    
