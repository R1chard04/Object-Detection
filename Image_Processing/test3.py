
import time
from pathlib import Path
import cv2 as cv
import depthai as dai

maskImg = cv.imread('photos\Test\maski.jpg')
#maskImgG = cv.cvtColor(maskImg, cv.COLOR_BGR2GRAY)

frame = cv.imread('photos\Test\Fault\WIN_20230123_10_47_15_Pro.jpg')

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

output = cv.subtract(frame,maskImg)
cv.imshow("refImgM", output)
cv.waitKey(0)