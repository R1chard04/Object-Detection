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

#-----------------------------------------Importing folders and images-----------------------------------------#
#Mask
maskImg = cv.imread('Image-Processing\photos\Test\mask.jpg')  #No tolerance around piece, 1-4 is increasing in tolerance

#Standard
refImg = cv.imread('Image-Processing\photos\Test\Reference\STANDARD.jpg')

#References
refDirectory = 'Image-Processing\photos\Test\Reference'

#Faults
faultDirectory = 'Image-Processing\photos\Test\Fault'

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

#-----------------------------------------Configuring Camera and Pictures Directory-----------------------------------------#
#Camera config
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

#Photos directory 
dirName = "Image-Processing\photos\Input"
Path(dirName).mkdir(parents=True, exist_ok=True)

#Pictures Name Generator
def timeStamp():
    now = str(datetime.datetime.now())
    now = round(float(((now.replace("-","")).replace(" ","")).replace(":","")))
    return now

#-----------------------------------------Main Loop-----------------------------------------#

with dai.Device(pipeline) as device:

    # Output queue will be used to get the rgb frames from the output defined above
    qRgb = device.getOutputQueue(name="rgb", maxSize=30, blocking=False)
    qStill = device.getOutputQueue(name="still", maxSize=30, blocking=True)
    qControl = device.getInputQueue(name="control")

    while True:
        inRgb = qRgb.tryGet()  # Non-blocking call, will return a new data that has arrived or None otherwise
        if inRgb is not None:
            frame = inRgb.getCvFrame()
            # 4k / 4
            frame = cv.pyrDown(frame)
            frame = cv.pyrDown(frame)
            # cv.imshow("rgb", frame)

        if qStill.has():
            fName = f"{dirName}/{timeStamp()}.jpeg"
            with open(fName, "wb") as f:
                f.write(qStill.get().getData())
                print('Image saved to', fName)
            time.sleep(3)
            # compare(fName)
            os.remove(fName)
        
        key = cv.waitKey(1)
        if key == ord('q'):
            break

        ctrl = dai.CameraControl()
        ctrl.setCaptureStill(True)
        qControl.send(ctrl)
        print("Sent 'still' event to the camera!")
        time.sleep(3)


# save_path = 'C:/example/'

# name_of_file = raw_input("What is the name of the file: ")

# completeName = os.path.join(save_path, name_of_file+".txt")         

# file1 = open(completeName, "w")

# toFile = raw_input("Write what you want into the field")

# file1.write(toFile)

# file1.close()



# report.close()

