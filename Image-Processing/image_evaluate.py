import cv2 as cv
import numpy as np
import os
from os import listdir
import sys

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

#-----------------------------------------Configuring Mask, MSE, Filter, Report-----------------------------------------#
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

#Report
report = open("report.txt", "w")
report.write("Report of deviations from reference image")

#-----------------------------------------Main Loop-----------------------------------------#

for i in range(len(folderDirectories)):
    report.write("\n\nFrom: ",)
    pieceIndex = 0

    for image in os.listdir(folderDirectories[i]):
        imagePath = os.path.join(folderDirectories[i], image)
        report.write("\n"+ str(pieceIndex) + " " + image + ": ")
        pieceIndex += 1

        inputImg = cv.convertScaleAbs(cv.imread(imagePath), alpha=alpha, beta=beta)
        inputImg = cv.cvtColor(inputImg, cv.COLOR_BGR2GRAY)
        inputImgM = cv.bitwise_and(inputImg,inputImg, mask= maskImgBinary)
        error, diffImg = mse(refImgM, inputImgM)

        report.write(str(error))
        report.write(" Pass") if error < 0.1 else report.write(" Fail")  
        #for this mask, the set tolerance is 0.1, this seems to work best, but this is experimentally tested (which isn't awesome)

report.close()

