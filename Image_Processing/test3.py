
import time
from pathlib import Path
import cv2 
import depthai as dai

maskii = cv2.imread('rgb_data\\bottle.jpg')
# maskDim = maskImg.shape
maskii = cv2.cvtColor(maskii, cv2.COLOR_BGR2GRAY)
(thresh, maskii) = cv2.threshold(maskii, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
#maskImgG = cv.cvtColor(maskImg, cv.COLOR_BGR2GRAY)

#frame = cv2.imread('rgb_data\\1674660972138.jpg')
#frameDim = frame.shape

# print ('dimension: ', maskDim, ' ', frameDim)
'''
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
'''

# output = cv2.subtract(frame,maskImg)
maskii = cv2.resize(maskii, (0,0), fx = 0.2, fy = 0.2)
cv2.imshow("refImgM", maskii)
cv2.waitKey(0)

#fill up black pixels
import cv2
import numpy as py

img = cv2.imread('rgb_data\\bottle.jpg')
img[img != 255] = 0 # change everything to white where pixel is not black
cv2.imshow("hihi", img)
cv2.waitKey(0)
# cv2.imwrite('my_img2.jpeg', img)