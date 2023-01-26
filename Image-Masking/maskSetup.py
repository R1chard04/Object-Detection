#!/usr/bin/env python3

import time
from pathlib import Path
import cv2
import depthai as dai

#-----------------------------------------OAK CAMERA SETUP-----------------------------------------#

# Create pipeline
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

#-----------------------------------------MAIN LOOP-----------------------------------------#

# Connect to device and start pipeline
with dai.Device(pipeline) as device:

    # Output queue will be used to get the rgb frames from the output defined above
    qRgb = device.getOutputQueue(name="rgb", maxSize=30, blocking=False)
    qStill = device.getOutputQueue(name="still", maxSize=30, blocking=True)
    qControl = device.getInputQueue(name="control")

    # Make sure the destination path is present before starting to store the examples
    dirName = "rgb_data"
    Path(dirName).mkdir(parents=True, exist_ok=True)
    ans = input ("Press \'s\' to capture a standard photo that has parts on \nPress \'w\' to capture a photo that does not have parts on \nPress \'g\' to generate a mask")
    # take STANDARD
    while True:
        inRgb = qRgb.tryGet()  # Non-blocking call, will return a new data that has arrived or None otherwise
        photoName = STANDARD
        if inRgb is not None:
            frame = inRgb.getCvFrame()
            # 4k / 4
            frame = cv2.pyrDown(frame)
            frame = cv2.pyrDown(frame)
            cv2.imshow("rgb", frame)

        if qStill.has():
            fName = f"{dirName}/{photoName}.jpg"
            with open(fName, "wb") as f:
                f.write(qStill.get().getData())
                print('Image saved to', fName)
        
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('s'):
            photoName = STANDARD
            ctrl = dai.CameraControl()
            ctrl.setCaptureStill(True)
            qControl.send(ctrl)
            print("Sent 'still' event to the camera")
        elif key == ord('w'):
            photoName = WITHOUT
            ctrl = dai.CameraControl()
            ctrl.setCaptureStill(True)
            qControl.send(ctrl)
            print("Sent 'still' event to the camera")
        elif key == ord('g'):
            img = cv.imread('Image-Masking\\rgb_data\\STANDARD.jpg')
            no = cv.imread('Image-Masking\\rgb_data\\WITHOUT.jpg')
            #Subtracting the two images to find the part area
            subtractOG = cv.cvtColor(self.partImg,cv.COLOR_BGR2GRAY) - cv.cvtColor(self.noPartImg,cv.COLOR_BGR2GRAY)

            #Applying filters on image
            alpha = 3 # Contrast control (rec 1-3)
            beta = -300 # Brightness control (rec -300 <-> 300)
            subtractOG = cv.convertScaleAbs(subtractOG, alpha=alpha, beta=beta)
            subtractOG = cv.fastNlMeansDenoising(subtractOG, None, 40, 7, 15)
            subtractOG = cv.fastNlMeansDenoising(subtractOG, None, 40, 7, 15)

            #Black and white configuration
            subtractOG = cv.bitwise_not(subtractOG)
            subtractOG[subtractOG < 10] = 0
            subtractOG[subtractOG != 0] = 255

            #Filling gaps
            thresh, imgThresh = cv.threshold(subtractOG,200,255,cv.THRESH_BINARY)
            fillMask = imgThresh.copy()
            height, width = imgThresh.shape[:2]
            mask = np.zeros((height+2,width+2),np.uint8)
            cv.floodFill(fillMask, mask,(0,0),(255,255,255))

            fillMask = cv.bitwise_not(fillMask)
            
            #Filling gaps
            subtractOG = subtractOG+fillMask

        elif key == ord('c'):
            photoName = int(time.time() * 1000)
            ctrl = dai.CameraControl()
            ctrl.setCaptureStill(True)
            qControl.send(ctrl)
            print("Sent 'still' event to the camera")
            


    # generate a mask
    # show user the generated mask and ask them if they want to remake the mask

    # run the program


#------------------take photoNametures and put it to our program-----------------#
    # while True:
    #     inRgb = qRgb.tryGet()  # Non-blocking call, will return a new data that has arrived or None otherwise
        
    # if qStill.has():
    #     fName = f"{dirName}/{int(time.time() * 1000)}.jpg"
    #     with open(fName, "wb") as f:
    #         f.write(qStill.get().getData())
    #         print('Image saved to', fName)
        
    # key = cv2.waitKey(1)
    # if key == ord('q'):
    #     break
    # elif key == ord('c'):
    #     ctrl = dai.CameraControl()
    #     ctrl.setCaptureStill(True)
    #     qControl.send(ctrl)
    #     print("Sent 'still' event to the camera!")
    # '''
    # ctrl = dai.CameraControl()
    # ctrl.setCaptureStill(True)
    # qControl.send(ctrl)
    # print("Sent 'still' event to the camera!")
    # time.sleep(3)
    # '''