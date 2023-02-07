#!/usr/bin/env python3

import cv2 as cv
import numpy as np
import os
from os import listdir
import sys
import time
import datetime
from pathlib import Path
import depthai as dai
import os.path
from skimage.metrics import structural_similarity

#-------------------------Camera Settings-------------------------#
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

def compare()->None:
    # Convert images to grayscale
    before = cv.imread('')
    after = cv.imread('FRAME.jpg')    
    before_gray = cv.cvtColor(before, cv.COLOR_BGR2GRAY)
    after_gray = cv.cvtColor(after, cv.COLOR_BGR2GRAY)

    # Compute SSIM between the two images
    (score, diff) = structural_similarity(before_gray, after_gray, full=True)
    print("Image Similarity: {:.4f}%".format(score * 100))

#---------------camera setup-----------------#

# Connect to device and start pipeline
with dai.Device(pipeline) as device:

    # Output queue will be used to get the rgb frames from the output defined above
    qRgb = device.getOutputQueue(name="rgb", maxSize=30, blocking=False)
    qStill = device.getOutputQueue(name="still", maxSize=30, blocking=True)
    qControl = device.getInputQueue(name="control")

    # Make sure the destination path is present before starting to store the examples
    dirName = "rgb_data"
    Path(dirName).mkdir(parents=True, exist_ok=True)

    # decide if it is the time to take a picture
    start = time.time()

    while True:
        inRgb = qRgb.tryGet()  # Non-blocking call, will return a new data that has arrived or None otherwise

        # keep showing the current frame to the user
        if inRgb is not None:
            frame = inRgb.getCvFrame()
            # 4k / 4
            frame = cv.pyrDown(frame)
            frame = cv.pyrDown(frame)
            cv.imshow("rgb", frame)
        
        # get the current frame and save it to the file
        if qStill.has():
            fName = f"{dirName}/{int(time.time() * 1000)}.jpg"
            with open(fName, "wb") as f:
                f.write(qStill.get().getData())
                print('Image saved to', fName)
            # compare()
        
        key = cv.waitKey(1)
        # focal length adjestment
        if key in [ord(','), ord('.')]:
            if key == ord(','): lensPos -= LENS_STEP
            if key == ord('.'): lensPos += LENS_STEP
            lensPos = clamp(lensPos, 0, 255)
            print("Setting manual focus, lens position: ", lensPos)
            ctrl = dai.CameraControl()
            ctrl.setManualFocus(lensPos)
            qControl.send(ctrl)
            
        # brightness adjestment
        if key in [ord('k'), ord('l')]:
            if key == ord('k'): brightness -= BRIGHT_STEP
            if key == ord('l'): brightness += BRIGHT_STEP
            brightness = clamp(brightness, -10, 10)
            print("Brightness:", brightness)
            ctrl = dai.CameraControl()
            ctrl.setBrightness(brightness)
            qControl.send(ctrl)
        if key == ord('q'):
            break
        elif key == ord('c'):
            ctrl = dai.CameraControl()
            ctrl.setCaptureStill(True)
            qControl.send(ctrl)
            print("Sent 'still' event to the camera!")
        # elif time.time() - start > 1:
        #     ctrl = dai.CameraControl()
        #     ctrl.setCaptureStill(True)
        #     qControl.send(ctrl)
        #     start = time.time()
        #     print("Sent 'still' event to the camera!")


'''

#-----------------------------------------Importing folders and images-----------------------------------------#
#Mask
maskImg = cv.imread('Image-Masking\mask_pics\MASK.jpg')  #No tolerance around piece, 1-4 is increasing in tolerance

#Standard
refImg = cv.imread('Image-Masking\mask_pics\STANDARD.jpg')

#References
refDirectory = "Image_Processing\photos\Test\Reference"

#Faults
faultDirectory = "Image_Processing\photos\Test\Fault"

#Folders
folderDirectories = [refDirectory,faultDirectory]

#-----------------------------------------Configuring Mask, MSE, Filter, Comparison, Report-----------------------------------------#
#Mask
maskImgG = cv.cvtColor(maskImg, cv.COLOR_BGR2GRAY)
(maskThresh, maskImgBW) = cv.threshold(maskImgG, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
thresh = 127
maskImgBinary = cv.threshold(maskImgG, maskThresh, 255, cv.THRESH_BINARY)[1]

#Filter
alpha = 3 # Contrast control (rec 1-3)
beta = 0 # Brightness control (rec -300 <-> 300)

refImg = cv.convertScaleAbs(refImg, alpha=alpha, beta=beta)
refImg = cv.cvtColor(refImg, cv.COLOR_BGR2GRAY)

#Standard Mask
refImgM = cv.bitwise_and(refImg,refImg, mask = maskImgBinary)

#MSE
def mse(img1, img2): #mean squared error
    height, width = img1.shape
    diffImg = cv.subtract(img1, img2)
    err = np.sum(diffImg**2)
    ans = err/(float(height*width)) #Closer to 0 is better
    return ans, diffImg

#Comparison
def compare(testPath):
    report.write("\n"+testPath)
    testImg = cv.convertScaleAbs(cv.imread(testPath), alpha=alpha, beta=beta)
    testImg = cv.cvtColor(testImg, cv.COLOR_BGR2GRAY)
    inputImgM = cv.bitwise_and(testImg,testImg, mask= maskImgBinary)
    error, diffImg = mse(refImgM, inputImgM)

    report.write(str(error))
    report.write(" Pass") if error < 0.1 else report.write(" Fail")  
    # for this mask, the set tolerance is 0.1, this seems to work best, but this is experimentally tested (which isn't awesome)

#Report
report = open("report.txt", "w")
report.write("Report of deviations from reference image")

for i in range(len(folderDirectories)):

    report.write("\n" + folderDirectories[i] + ":\n")

    for images in os.listdir(folderDirectories[i]):
        print(images)
        images = os.path.join(folderDirectories[i],images)
        compare(images)
'''