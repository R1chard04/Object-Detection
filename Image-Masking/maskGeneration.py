#!/usr/bin/env python3

import time
from pathlib import Path
import cv2 as cv
import depthai as dai
import numpy as np

#-----------------------------------------OAK CAMERA SETUP-----------------------------------------#

# fixed focus setup
# camFocalLenth = 115
lensPos = 150
LENS_STEP = 3
def clamp(num, v0, v1):
    return max(v0, min(num, v1))

# Create pipeline
pipeline = dai.Pipeline()

camRgb = pipeline.create(dai.node.ColorCamera)
camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_4_K)
# camRgb.initialControl.setManualFocus(camFocalLenth) # set manual fixed-focus focal length

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

    controlQueue = device.getInputQueue('control')
    
    # Output queue will be used to get the rgb frames from the output defined above
    qRgb = device.getOutputQueue(name="rgb", maxSize=30, blocking=False)
    qStill = device.getOutputQueue(name="still", maxSize=30, blocking=True)
    qControl = device.getInputQueue(name="control")

    # Make sure the destination path is present before starting to store the examples
    # dirName = "rgb_data"
    # Path(dirName).mkdir(parents=True, exist_ok=True)
    photoName = "null.jpg"
    dirName = "mask_pics"
    Path(dirName).mkdir(parents=True, exist_ok=True)
    print ("Press \'s\' to capture a standard photo that has parts on \nPress \'n\' to capture a photo that does not have parts on \nPress \'g\' to generate a mask\nPress \'q\' to quit")
    # take STANDARD
    while True:
        inRgb = qRgb.tryGet()  # Non-blocking call, will return a new data that has arrived or None otherwise

        if inRgb is not None:
            frame = inRgb.getCvFrame()
            # 4k / 4
            frame = cv.pyrDown(frame)
            frame = cv.pyrDown(frame)
            cv.imshow("rgb", frame)

        if qStill.has():
            fName = f"{dirName}/{photoName}.jpg"
            with open(fName, "wb") as f:
                f.write(qStill.get().getData())
                print('Image saved to', fName)
        
        key = cv.waitKey(1)
        if key in [ord(','), ord('.')]:
            if key == ord(','): lensPos -= LENS_STEP
            if key == ord('.'): lensPos += LENS_STEP
            lensPos = clamp(lensPos, 0, 255)
            print("Setting manual focus, lens position: ", lensPos)
            ctrl = dai.CameraControl()
            ctrl.setManualFocus(lensPos)
            controlQueue.send(ctrl)
        elif key == ord('q'):
            break
        elif key == ord('s'):
            photoName = "STANDARD"
            # dirName = "mask_pics"
            ctrl = dai.CameraControl()

            # autofocus contro
            # ctrl.setAutoFocusMode(dai.CameraControl.AutoFocusMode.AUTO)
            # ctrl.setAutoFocusTrigger()

            ctrl.setCaptureStill(True)
            qControl.send(ctrl)
            print("Sent 'still' event to the camera")
        elif key == ord('n'):
            photoName = "NONE"
            # dirName = "mask_pics"
            ctrl = dai.CameraControl()
            ctrl.setCaptureStill(True)
            qControl.send(ctrl)
            print("Sent 'still' event to the camera")
        elif key == ord('g'):
            partImg = cv.imread('mask_pics\\STANDARD.jpg')
            noPartImg = cv.imread('mask_pics\\NONE.jpg')

            #Subtracting the two images to find the part area
            subtractOG = cv.subtract(cv.cvtColor(partImg,cv.COLOR_BGR2GRAY),cv.cvtColor(noPartImg,cv.COLOR_BGR2GRAY))
            # subtractOG = cv.cvtColor(partImg,cv.COLOR_BGR2GRAY) - cv.cvtColor(noPartImg,cv.COLOR_BGR2GRAY)

            #Applying filters on image
            alpha = 3 # Contrast control (rec 1-3)
            beta = -300 # Brightness control (rec -300 <-> 300)
            subtractOG = cv.convertScaleAbs(subtractOG, alpha=alpha, beta=beta)
            subtractOG = cv.bitwise_not(subtractOG) #inverts

            subtractOG = cv.fastNlMeansDenoising(subtractOG, None, 40, 7, 15)
            subtractOG = cv.fastNlMeansDenoising(subtractOG, None, 40, 7, 15)

            # #Black and white configuration

            subtractOG[subtractOG < 10] = 0
            subtractOG[subtractOG != 0] = 255

            kernel = np.ones((230,230), np.uint8)  # note this is a horizontal kernel
            subtractOG = cv.dilate(subtractOG, kernel, iterations=1)


            #Filling gaps
            thresh, imgThresh = cv.threshold(subtractOG,200,255,cv.THRESH_BINARY)
            fillMask = imgThresh.copy()
            height, width = imgThresh.shape[:2]
            mask = np.zeros((height+2,width+2),np.uint8)
            cv.floodFill(fillMask, mask,(0,0),(255,255,255))

            fillMask = cv.bitwise_not(fillMask)

            #Filling gaps
            subtractOG = subtractOG+fillMask
            subtractOG = cv.erode(subtractOG, kernel, iterations=1) 
            img = cv.resize(subtractOG, (0,0), fx = 0.2, fy = 0.2)
            cv.imwrite("Image-Masking\mask_pics\MASK.jpg",subtractOG)
            cv.imshow("MASK",img)
            cv.waitKey(0)

        elif key == ord('q'):
            break
        
        # elif key == ord('t'):
        #     print("Autofocus trigger (and disable continuous)")
        #     ctrl = dai.CameraControl()
        #     ctrl.setAutoFocusMode(dai.CameraControl.AutoFocusMode.AUTO)
        #     ctrl.setAutoFocusTrigger()
        #     controlQueue.send(ctrl)
        # elif key == ord('c'):
        #     dirName = rgb_data
        #     photoName = int(time.time() * 1000)
        #     ctrl = dai.CameraControl()
        #     ctrl.setCaptureStill(True)
        #     qControl.send(ctrl)
        #     print("Sent 'still' event to the camera")
            


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
        
    # key = cv.waitKey(1)
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