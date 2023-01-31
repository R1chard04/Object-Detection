import cv2
import numpy as np
import os
from os import listdir
import sys

# load the input images
off1 = cv2.imread('photos\Test\Reference\WIN_20230123_10_46_36_Pro.jpg')
standard = cv2.imread('photos\Test\Reference\STANDARD.jpg')


alpha = 3 # Contrast control (1.0-3.0)
beta = 0 # Brightness control (0-100)
off1 = cv2.convertScaleAbs(off1, alpha=alpha, beta=beta)
standard = cv2.convertScaleAbs(standard, alpha=alpha, beta=beta)
# convert the images to grayscale
off1 = cv2.cvtColor(off1, cv2.COLOR_BGR2GRAY)
standard = cv2.cvtColor(standard, cv2.COLOR_BGR2GRAY)
cv2.imshow('adjustedX', off1)
cv2.imshow('adjustedS', standard)

def mse(img1, img2):
    h, w = img1.shape
    diff = cv2.subtract(img1, img2)
    err = np.sum(diff**2)
    ans = err/(float(h*w)) #Closer to 0 is better
    return ans, diff

#Masking
maskImg = cv2.imread('photos\Test\subtractOG.jpg')
grayMask = cv2.cvtColor(maskImg, cv2.COLOR_BGR2GRAY)
(thresh, maskBW) = cv2.threshold(grayMask, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
thresh = 127
binaryMask = cv2.threshold(grayMask, thresh, 255, cv2.THRESH_BINARY)[1]

off1M = cv2.bitwise_and(off1,off1, mask= binaryMask)
standardM = cv2.bitwise_and(standard,standard, mask= binaryMask)

error, diff1 = mse(standardM, off1M)

print("Error between the two images1: ", error)

# cv2.imshow("diff1", diff1)
# cv2.imshow("off1", off1M)
# cv2.imshow("standard", standardM)
cv2.waitKey(0)
#cv2.destroyAllWindows()
