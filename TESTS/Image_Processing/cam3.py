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

xout = pipeline.create(dai.node.XLinkOut)
xout.setStreamName("out")
camRgb.isp.link(xout.input)

device_info = dai.DeviceInfo("169.254.1.203")

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
        print('Latency3: {:.2f} ms, Average latency: {:.2f} ms, Std: {:.2f}'.format(latencyMs, np.average(diffs), np.std(diffs)))
        
        # Not relevant for this example
        cv.imshow('frame', imgFrame.getCvFrame())
        cv.waitKey(1)