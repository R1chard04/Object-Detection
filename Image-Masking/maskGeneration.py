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
brightness = 0
BRIGHT_STEP = 1
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
    print ("Press \'s\' to capture a standard photo that has parts on \nPress \'n\' to capture a photo that does not have parts on \nPress \'g\' to generate a mask\nPress \'q\' to quit\nPress ,/. to adjest focal length\nPress k/l to adjest brightness")
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
            qControl.send(ctrl)
        if key in [ord('k'), ord('l')]:
            if key == ord('k'): brightness -= BRIGHT_STEP
            if key == ord('l'): brightness += BRIGHT_STEP
            brightness = clamp(brightness, -10, 10)
            print("Brightness:", brightness)
            ctrl = dai.CameraControl()
            ctrl.setBrightness(brightness)
            qControl.send(ctrl)
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
            partImg = cv.imread('Image-Masking\mask_pics\STANDARD.jpg')
            noPartImg = cv.imread('Image-Masking\mask_pics\\NONE.jpg')

            # Convert image to HSV color space
            partImgHSV = cv.cvtColor(partImg, cv.COLOR_BGR2HSV)
            noPartImgHSV = cv.cvtColor(noPartImg, cv.COLOR_BGR2HSV)

            # Define lower and upper color bounds for orange
            lower_orange = np.array([0, 1, 1])
            upper_orange = np.array([150, 255, 255])

            # Threshold the HSV image to get only orange colors
            maskPart = cv.inRange(partImgHSV, lower_orange, upper_orange)
            maskNoPart = cv.inRange(noPartImgHSV, lower_orange, upper_orange)

            # Change all orange pixels to black
            partImg[maskPart > 0] = [0, 0, 0]
            noPartImg[maskNoPart > 0] = [0, 0, 0]

            #Subtracting the two images to find the part area
            subtractBGR = cv.subtract(partImg,noPartImg)
            subtractGray = cv.cvtColor(subtractBGR, cv.COLOR_BGR2GRAY)

            feed = subtractGray

            denoise = cv.bilateralFilter(feed, 15, 100, 100)
            denoise = cv.GaussianBlur(denoise, (5,5), 15, 15)
            denoise = cv.bilateralFilter(denoise, 15, 100, 100)
            denoise = cv.fastNlMeansDenoising(denoise, None, 400, 7, 15)
            denoise = cv.fastNlMeansDenoising(denoise, None, 400, 7, 15)
            denoise[denoise < 10] = 0

            feed = denoise
            
            threshold_type = cv.ADAPTIVE_THRESH_GAUSSIAN_C
            block_size = 75
            C = 5
            thresholded = cv.adaptiveThreshold(feed, 255, threshold_type, cv.THRESH_BINARY, block_size, C)
            thresholded  = cv.bitwise_not(thresholded)
            _, thresholded = cv.threshold(thresholded, 128, 255, cv.THRESH_BINARY)

            feed = thresholded

            # kernel = np.ones((5,10), np.uint8)  # note this is a horizontal kernel
            # denoise = cv.dilate(feed, kernel, iterations=1)

            # kernel = np.ones((10,1), np.uint8)  # note this is a horizontal kernel
            # denoise = cv.erode(denoise, kernel, iterations=3)

            # feed = denoise
            
            

            feed = feed

            # Find contours in the binary image
            contours, _ = cv.findContours(feed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            # Sort contours by area and keep only the largest contour
            contours = sorted(contours, key=cv.contourArea, reverse=True)
            largest_contour = contours[0]
            # Draw the largest contour on an empty image to create a binary mask
            mask = np.zeros_like(thresholded)
            cv.drawContours(mask, [largest_contour], -1, 255, -1)

            feed = mask

            #Filling gaps
            thresh, imgThresh = cv.threshold(feed,50,255,cv.THRESH_BINARY)
            fillMask = imgThresh.copy()
            height, width = imgThresh.shape[:2]
            mask = np.zeros((height+2,width+2),np.uint8)
            cv.floodFill(fillMask, mask,(0,0),(255,255,255))
            fillMask = cv.bitwise_not(fillMask)
            
            final = feed+fillMask

            input = denoise
            img = cv.resize(input, (0,0), fx = 0.2, fy = 0.2)
            cv.imwrite("mask_pics\MASK.jpg",final)
            cv.imshow("MASK",img)
            cv.waitKey(0)

        elif key == ord('q'):
            break
        
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