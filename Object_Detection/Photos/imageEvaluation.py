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
# -----------------------------------------Importing folders and images-----------------------------------------#
# Mask
# No tolerance around piece, 1-4 is increasing in tolerance
# maskImg = cv.imread('Image_Processing\photos\Test\subtractOG.jpg')
maskImg =cv.imread('INIT\\mask.jpg')
maskImg = cv.cvtColor(maskImg, cv.COLOR_BGR2GRAY)
maskImg = cv.resize(maskImg, (0,0), fx = 1.875, fy = 1.875)

# Standard
# refImg = cv.imread('Image_Processing\photos\Test\Reference\STANDARD.jpg')
refImg = cv.imread('STD\\STD1.jpg')
refImg = cv.cvtColor(refImg, cv.COLOR_BGR2GRAY)

# References
refDirectory = "Image_Processing\photos\Test\Reference"

# Faults
faultDirectory = "Image_Processing\photos\Test\Fault"

init = "INIT"

# Folders
# folderDirectories = [refDirectory, faultDirectory]
folderDirectories = [init]

# -----------------------------------------Configuring Mask, MSE, Filter, Comparison, Report-----------------------------------------#
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
print(refImg.shape)
print(maskImgBinary.shape)
refImgM = cv.bitwise_and(refImg, refImg, mask=maskImgBinary)

# MSE


def mse(img1, img2):  # mean squared error
    height, width = img1.shape
    diffImg = cv.subtract(img1, img2)
    err = np.sum(diffImg**2)
    ans = err/(float(height*width))  # Closer to 0 is better
    return ans, diffImg


def mse2(before, after):
    # Convert images to grayscale
    # before_gray = cv.cvtColor(before, cv.COLOR_BGR2GRAY)
    before_gray = before
    after_gray = cv.cvtColor(after, cv.COLOR_BGR2GRAY)

    # Compute SSIM between the two images
    (score, diff) = structural_similarity(before_gray, after_gray, full=True)
    score = score*100
    return score
    # print("Image Similarity: {:.4f}%".format(score * 100))

    # # The diff image contains the actual image differences between the two images
    # # and is represented as a floating point data type in the range [0,1]
    # # so we must convert the array to 8-bit unsigned integers in the range
    # # [0,255] before we can use it with OpenCV
    # diff = (diff * 255).astype("uint8")
    # diff_box = cv.merge([diff, diff, diff])

    # # Threshold the difference image, followed by finding contours to
    # # obtain the regions of the two input images that differ
    # thresh = cv.threshold(
    #     diff, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
    # contours = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # contours = contours[0] if len(contours) == 2 else contours[1]

    # mask = np.zeros(before.shape, dtype='uint8')
    # filled_after = after.copy()

    # for c in contours:
    #     area = cv.contourArea(c)

# Comparison


def compare(testPath):
    report.write("\n"+testPath)
    testImg = cv.convertScaleAbs(cv.imread(testPath), alpha=alpha, beta=beta)
    testImg = cv.cvtColor(testImg, cv.COLOR_BGR2GRAY)
    inputImgM = cv.bitwise_and(testImg, testImg, mask=maskImgBinary)
    # error, diffImg = mse1(refImgM, inputImgM)
    error= mse(refImgM, inputImgM)

    report.write(str(error))
    # report.write(" Pass") if error < 0.1 else report.write(" Fail")
    # for this mask, the set tolerance is 0.1, this seems to work best, but this is experimentally tested (which isn't awesome)

def compareNoMask(testPath):
    report.write("\n"+testPath)
    testImg = cv.convertScaleAbs(cv.imread(testPath), alpha=alpha, beta=beta)
    # testImg = cv.cvtColor(testImg, cv.COLOR_BGR2GRAY)
    # inputImgM = cv.bitwise_and(testImg, testImg, mask=maskImgBinary)
    # error, diffImg = mse1(refImgM, inputImgM)
    error = mse2(refImg, testImg)

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
        compareNoMask(images)
