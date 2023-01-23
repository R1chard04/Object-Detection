import cv2 as cv
import numpy as np
import os
from os import listdir
import sys

#-----------------------------------------Importing folders and images-----------------------------------------#
#Mask
maskImg = cv.imread('Image-Processing\photos\Test\mask3.jpg')

#Standard
refImg = cv.cvtColor(cv.imread('Image-Processing\photos\Test\Reference\STANDARD.jpg'), cv.COLOR_BGR2GRAY)


#References
refDirectory = 'Image-Processing\photos\Test\Reference'

#Faults
faultDirectory = 'Image-Processing\photos\Test\Fault'

#Folders
folderDirectories = [refDirectory,faultDirectory]

#-----------------------------------------Configuring Mask, MSE, Report-----------------------------------------#
#Mask
maskImgG = cv.cvtColor(maskImg, cv.COLOR_BGR2GRAY)
(maskThresh, maskImgBW) = cv.threshold(maskImgG, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
thresh = 127
maskImgBinary = cv.threshold(maskImgG, maskThresh, 255, cv.THRESH_BINARY)[1]

#Standard Mask
refImgM = cv.bitwise_and(refImg,refImg, mask = maskImgBinary)

#MSE
def mse(img1, img2):
    height, width = img1.shape
    diffImg = cv.subtract(img1, img2)
    err = np.sum(diffImg**2)
    ans = err/(float(height*width)) #Closer to 0 is better
    return ans, diffImg

#Report
report = open("report.txt", "w")
report.write("Report of deviations from reference image")

#-----------------------------------------Main Loop-----------------------------------------#

for i in range(len(folderDirectories)):
    report.write("\n\nFrom: ",)
    imageIndex = 0

    for image in os.listdir(folderDirectories[i]):
        imagePath = os.path.join(folderDirectories[i], image)
        report.write("\n"+ str(imageIndex) + " " + image + ": ")
        imageIndex += 1

        inputImg = cv.cvtColor(cv.imread(imagePath), cv.COLOR_BGR2GRAY)
        inputImgM = cv.bitwise_and(inputImg,inputImg, mask= maskImgBinary)
        error, diffImg = mse(refImgM, inputImgM)
        report.write(str(error))