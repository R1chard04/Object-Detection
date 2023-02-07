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


def mse(img1, img2):  # mean squared error
    height, width = img1.shape
    diffImg = cv.subtract(img1, img2)
    err = np.sum(diffImg**2)
    ans = err/(float(height*width))  # Closer to 0 is better
    return ans, diffImg

maskImg = cv.cvtColor(cv.imread('photos\Test\mask.jpg'), cv.COLOR_BGR2GRAY)
refImg = cv.cvtColor(cv.imread('photos\Test\Reference\STANDARD.jpg'), cv.COLOR_BGR2GRAY)
frame1 = cv.cvtColor(cv.imread('photos\Test\Reference\WIN_20230123_10_48_09_Pro.jpg'), cv.COLOR_BGR2GRAY)
frame2 = cv.cvtColor(cv.imread('photos\Test\Fault\WIN_20230123_10_46_58_Pro.jpg'), cv.COLOR_BGR2GRAY)

refDirectory = "photos\Test\Reference"
faultDirectory = "photos\Test\Fault"
folderDirectories = [refDirectory, faultDirectory]

# Mask
# maskImgG = cv.cvtColor(maskImg, cv.COLOR_BGR2GRAY)
(maskThresh, maskImgBW) = cv.threshold(maskImg, 127, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
maskImgBinary = cv.threshold(maskImg, maskThresh, 255, cv.THRESH_BINARY)[1]

# Filter
alpha = 3  # Contrast control (rec 1-3)
beta = 0  # Brightness control (rec -300 <-> 300)

refImg = cv.convertScaleAbs(refImg, alpha=alpha, beta=beta)
# refImg = cv.cvtColor(refImg, cv.COLOR_BGR2GRAY)

# Standard Mask
refImgM = cv.bitwise_and(refImg, refImg, mask=maskImgBinary)


# height, width = maskImg.shape()
totalPixels = np.sum(maskImg) 
whitePixels = np.sum(maskImg == 255)

# inputImgM1 = cv.bitwise_and(frame1, frame1, mask=maskImg)
# inputImgM2 = cv.bitwise_and(frame2, frame2, mask=maskImg)
refImgM = cv.bitwise_and(refImgM, refImgM, mask=maskImg)

def compare(testPath):
    report.write("\n"+testPath)
    testImg = cv.convertScaleAbs(cv.imread(testPath), alpha=alpha, beta=beta)
    testImg = cv.cvtColor(testImg, cv.COLOR_BGR2GRAY)
    inputImgM = cv.bitwise_and(testImg, testImg, mask=maskImgBinary)
    # error, diffImg = mse1(refImgM, inputImgM)
    error, diffImg= mse(refImgM, inputImgM)
    error = error*totalPixels/whitePixels
    report.write(str(error))
    # report.write(" Pass") if error < 0.1 else report.write(" Fail")
    # for this mask, the set tolerance is 0.1, this seems to work best, but this is experimentally tested (which isn't awesome)

# Report
report = open("report.txt", "w")
report.write("Report of deviations from reference image")

for i in range(len(folderDirectories)):

    report.write("\n" + folderDirectories[i] + ":\n")

    for images in os.listdir(folderDirectories[i]):
        print(images)
        images = os.path.join(folderDirectories[i], images)
        compare(images)

# # error, diffImg = mse1(refImgM, inputImgM)
# error1, pic = mse(ref, inputImgM1)
# error2, pic = mse(ref, inputImgM2)

# print("totalPixels: ", totalPixels)
# print("whitePixels: ", whitePixels)
# print("error1: ", error1)
# print("error2: ", error2)
# print("average MSE error per white pixel: ", error1*totalPixels/whitePixels)
# print("average MSE error per white pixel: ", error2*totalPixels/whitePixels)


# get total num of pixels for the pic
# get num of white and black pixels for the mask


# get average MSE per white pixel 


