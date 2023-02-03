from __future__ import print_function
import cv2 as cv
import argparse
import numpy as np
from functions import floodFill, denoiseWhite, fillHoles

std = cv.imread("AutoMask\mask_pics\\STANDARD4.jpg")
na = cv.imread("AutoMask\mask_pics\\NONE4.jpg")

# std = cv.cvtColor(std, cv.COLOR_BGR2GRAY)
# na = cv.cvtColor(na, cv.COLOR_BGR2GRAY)

# clahe = cv.createCLAHE(clipLimit = 5)
# na_dst = clahe.apply(na) + 30
# std_dst = clahe.apply(std) + 30
 
# cv.imshow('Source image', cv.resize(na, (0,0), fx = 0.2, fy = 0.2))
# cv.imshow('Equalized Image', cv.resize(na_dst, (0,0), fx = 0.2, fy = 0.2))
# cv.imshow('Source', cv.resize(std, (0,0), fx = 0.2, fy = 0.2))
# cv.imshow('Equalized', cv.resize(std_dst, (0,0), fx = 0.2, fy = 0.2))

result1 = cv.subtract(std, na)
binary = cv.cvtColor(result1, cv.COLOR_BGR2GRAY)
binary[binary!=0]=255

kernel = np.ones((10,10), np.uint8)
binary = cv.dilate(binary, kernel, iterations=1)
binary = cv.erode(binary, kernel, iterations=2) #correction

oppBinary = cv.bitwise_not(binary)
result2 = cv.bitwise_and(std,std,mask = oppBinary)
result = cv.add(result1,result2)


# cv.imshow("G", cv.resize(s, (0,0), fx = 0.2, fy = 0.2))
# cv.imshow("R", cv.resize(v, (0,0), fx = 0.2, fy = 0.2))


feed = result

#---------------------------------------------------------------#

denoise = cv.cvtColor(feed, cv.COLOR_BGR2GRAY)
kernel = np.ones((3,3),np.uint8)
denoise = cv.adaptiveThreshold(denoise,255,cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 51, 10)

denoise = denoiseWhite(denoise)
# denoise = cv.dilate(denoise, kernel, iterations=1)
# denoise = floodFill(denoise)
denoise = cv.erode(denoise, kernel, iterations=2)
denoise = fillHoles(denoise)
# denoise = cv.dilate(denoise, kernel, iterations=1)
# denoise = cv.erode(denoise, kernel, iterations=1)


cv.imshow("B", cv.resize(denoise, (0,0), fx = 0.2, fy = 0.2))

cv.waitKey()
