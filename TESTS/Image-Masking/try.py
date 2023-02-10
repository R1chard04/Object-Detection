#!/usr/bin/env python3

import time
from pathlib import Path
import cv2 as cv
import depthai as dai
import numpy as np
import argparse

def mse():  # mean squared error
    img1 = cv.imread("Image-Masking\mask_pics\MASK.jpg")
    img2 = cv.imread("Image-Masking\mask_pics\RESULT.jpg")
    height, width = img1.shape[:2]
    diffImg = cv.subtract(img1, img2)
    err = np.sum(diffImg**2)
    ans = err/(float(height*width))  # Closer to 0 is betterr
    return ans, diffImg

def filterImage(std, na):
    std = cv.cvtColor(std, cv.COLOR_BGR2HSV)
    na = cv.cvtColor(na, cv.COLOR_BGR2HSV)

    subtract = cv.subtract(std,na)
    subtract = cv.cvtColor(subtract, cv.COLOR_HSV2BGR)
    subtract = cv.cvtColor(subtract, cv.COLOR_BGR2GRAY)
    print("something")

    # result = cv.fastNlMeansDenoising(subtract,(3,3))
    # result = cv.bilateralFilter(subtract, 9, 75,75)
    # result[result < 40] = 0
    # result[result > 10] = 255

    return subtract

# Function filter orange into black image
def orange2Black(image):
    ORANGE_MIN = np.array([5, 50, 50], np.uint8)
    ORANGE_MAX = np.array([15, 255, 255], np.uint8)

    hsv_img = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    frame_threshed = cv.inRange(hsv_img, ORANGE_MIN, ORANGE_MAX)
    cv.imwrite('output2.jpg', frame_threshed)

    


# -----------------------------------------OAK CAMERA SETUP-----------------------------------------#

# fixed focus setup
# camFocalLenth = 115
lensPos = 150
brightness = 0
BRIGHT_STEP = 1
LENS_STEP = 3
ref = cv.imread('Image-Masking\mask_pics\\MASK.jpg')
na = cv.imread('Image-Masking\mask_pics\\NONE.jpg')
test = cv.imread('Image-Masking\mask_pics\\FRAME.jpg')

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

# -----------------------------------------MAIN LOOP-----------------------------------------#

# Connect to device and start pipeline
# # Force USB2 communication
# with dai.Device(pipeline, usb2Mode = True) as device:

with dai.Device(pipeline) as device:
    # Output queue will be used to get the rgb frames from the output defined above
    qRgb = device.getOutputQueue(name="rgb", maxSize=30, blocking=False)
    qStill = device.getOutputQueue(name="still", maxSize=30, blocking=True)
    qControl = device.getInputQueue(name="control")

    # Make sure the destination path is present before starting to store the examples
    # dirName = "rgb_data"
    # Path(dirName).mkdir(parents=True, exist_ok=True)
    photoName = "null.jpg"
    dirName = "Image-Masking\mask_pics"
    Path(dirName).mkdir(parents=True, exist_ok=True)
    
    # Instruction
    print("Press \'s\' to capture a standard photo that has parts on")
    print("Press \'n\' to capture a photo that does not have parts on")
    print("Press \'g\' to generate a mask")
    print("Press ,/. to adjest focal length")
    print("Press k/l to adjest brightness")
    print("Press \'t\' to start or end evaluating")
    print("Press \'q\' to quit")
    
    
    # take STANDARD
    
    start = time.time()
    startEvalutating = False
    
    while True:
        # Non-blocking call, will return a new data that has arrived or None otherwise
        inRgb = qRgb.tryGet()
        
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
            
            if (startEvalutating):
                test = cv.imread('Image-Masking\mask_pics\\FRAME.jpg')
                result = filterImage(test, na)
                cv.imwrite("Image-Masking\mask_pics\\RESULT.jpg", result)
                error, diff = mse()    
                print(error)
                print("Sent 'still' event to the camera!")
            
        key = cv.waitKey(1)
        # focal length adjestment
        if key in [ord(','), ord('.')]:
            if key == ord(','):
                lensPos -= LENS_STEP
            if key == ord('.'):
                lensPos += LENS_STEP
            lensPos = clamp(lensPos, 0, 255)
            print("Setting manual focus, lens position: ", lensPos)
            ctrl = dai.CameraControl()
            ctrl.setManualFocus(lensPos)
            qControl.send(ctrl)
        
        # brightness adjestment
        if key in [ord('k'), ord('l')]:
            if key == ord('k'):
                brightness -= BRIGHT_STEP
            if key == ord('l'):
                brightness += BRIGHT_STEP
            brightness = clamp(brightness, -10, 10)
            print("Brightness:", brightness)
            ctrl = dai.CameraControl()
            ctrl.setBrightness(brightness)
            qControl.send(ctrl)
            
        if key == ord('q'):
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
            std = cv.imread('Image-Masking\mask_pics\\STANDARD.jpg')
            na = cv.imread('Image-Masking\mask_pics\\NONE.jpg')
            result = cv.absdiff(std, na)
            # result = cv.cvtColor(result, cv.COLOR_BGR2GRAY)
            # result[result >= 30] = 255
            # result - cv.threshold(result, 10, 255, cv.THRESH_BINARY)
            # img = cv.resize(result, (0, 0), fx=0.2, fy=0.2)
            cv.imwrite("Image-Masking\mask_pics\MASK.jpg", result)
            # cv.imshow("MASK", img)
            cv.waitKey(0)

        elif key == ord('t'):
            if (startEvalutating):
                startEvalutating = False
                print("END TESTING")
            else:
                startEvalutating = True
                print("START TESTING")
                
        elif (time.time() - start > 1) and startEvalutating:
            photoName = "FRAME"
            ctrl = dai.CameraControl()
            ctrl.setCaptureStill(True)
            qControl.send(ctrl)
            start = time.time()
        

        # elif key == ord('r'):
        #     ref = cv.imread('Image-Masking\mask_pics\\MASK.jpg')
        #     na = cv.imread('Image-Masking\mask_pics\\NONE.jpg')
        #     test = cv.imread('Image-Masking\mask_pics\\TEST.jpg')
        #     while True:
        #         result = filterImage(test, na)
        #         cv.imwrite("Image-Masking\mask_pics\\RESULT.jpg", result)
        #         error, diff = mse()

                
        #         print(error)
        #         time.sleep(1)

        

        # elif key == ord('t'):
        #     print("Autofocus trigger (and disable continuous)")
        #     ctrl = dai.CameraControl()
        #     ctrl.setAutoFocusMode(dai.CameraControl.AutoFocusMode.AUTO)
        #     ctrl.setAutoFocusTrigger()
        #     qControl.send(ctrl)
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


# ------------------take photoNametures and put it to our program-----------------#
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
