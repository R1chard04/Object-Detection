import depthai as dai
import numpy as np
import cv2 as cv

# Create pipeline
pipeline = dai.Pipeline()
# This might improve reducing the latency on some systems
pipeline.setXLinkChunkSize(0)

# Define source and output
camRgb = pipeline.create(dai.node.ColorCamera)
camRgb.setFps(1)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_4_K)
camRgb.setPreviewSize(1920, 1080)

xout = pipeline.create(dai.node.XLinkOut)
xout.setStreamName("out")
camRgb.isp.link(xout.input)

device_info = dai.DeviceInfo("169.254.1.202")

# Connect to device and start pipeline
with dai.Device(pipeline, device_info) as device:
    print(device.getUsbSpeed())
    q = device.getOutputQueue(name="out")
    diffs = np.array([])
    while True:
        imgFrame = q.get()
        # Latency in miliseconds 
        latencyMs = (dai.Clock.now() - imgFrame.getTimestamp()).total_seconds() * 1000
        diffs = np.append(diffs, latencyMs)
        print('Latency1: {:.2f} ms, Average latency: {:.2f} ms, Std: {:.2f}'.format(latencyMs, np.average(diffs), np.std(diffs)))
        
        # Not relevant for this example
        img = imgFrame.getCvFrame()
        cv.imwrite("photos.jpg", img)
        cv.imshow('frame', cv.imread("photos.jpg"))
        cv.waitKey(1)
        
        
# if self.qStill.has():
#                 with open(path, "wb") as img:
#                     img.write(self.qStill.get().getData())
                
#                     img = cv.imread(path)
#                     return path