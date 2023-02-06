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
maskImgG = cv.cvtColor(maskImg, cv.COLOR_BGR2GRAY)
(maskThresh, maskImgBW) = cv.threshold(
    maskImgG, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
thresh = 127
maskImgBinary = cv.threshold(maskImgG, maskThresh, 255, cv.THRESH_BINARY)[1]

# Filter
alpha = 3  # Contrast control (rec 1-3)
beta = 0  # Brightness control (rec -300 <-> 300)

refImg = cv.convertScaleAbs(refImg, alpha=alpha, beta=beta)
refImg = cv.cvtColor(refImg, cv.COLOR_BGR2GRAY)

# Standard Mask
refImgM = cv.bitwise_and(refImg, refImg, mask=maskImgBinary)


# height, width = maskImg.shape()
totalPixels = np.sum(maskImg) 
whitePixels = np.sum(maskImg == 255)

inputImgM1 = cv.bitwise_and(frame1, frame1, mask=maskImg)
inputImgM2 = cv.bitwise_and(frame2, frame2, mask=maskImg)
refImgM = cv.bitwise_and(refImgM, refImgM, mask=maskImg)


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


