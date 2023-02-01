# import cv2 as cv
# import numpy as np


# BGR = cv.subtract(partImg,noPartImg)
# BGR = cv.GaussianBlur(BGR,(3,3),0)
# BGR = cv.cvtColor(BGR, cv.COLOR_BGR2GRAY)


# gray = cv.cvtColor(BGR, cv.COLOR_BGR2GRAY)
# thresh = cv.threshold(gray, 130, 255, cv.THRESH_BINARY)[1]
# thresh = cv.fastNlMeansDenoising(thresh, None, 40, 7, 15)
# HSV = cv.cvtColor(thresh,cv.COLOR_BGR2HSV)

# add = cv.add(gray, thresh)
# add = cv.medianBlur(add, 15, 15)
# add = cv.threshold(add, 254, 255, cv.THRESH_BINARY)[1]



# # detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
# contours, hierarchy = cv.findContours(image = add, mode=cv.RETR_TREE, method=cv.CHAIN_APPROX_NONE)


# Apply threshold to remove low intensity differences
_, mask = cv.threshold(diff, 100, 255, cv.THRESH_BINARY)

# Apply morphological operations to fill in small holes
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
maskPart = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

# 
# subtract = cv.fastNlMeansDenoising(subtract, None, 40, 7, 15)

# # #Black and white configuration



# #Filling gaps
# thresh, imgThresh = cv.threshold(maskPart,200,255,cv.THRESH_BINARY)
# fillMask = imgThresh.copy()
# height, width = imgThresh.shape[:2]
# mask = np.zeros((height+2,width+2),np.uint8)
# cv.floodFill(fillMask, mask,(0,0),(255,255,255))

# fillMask = cv.bitwise_not(fillMask)

# #Filling gaps
# subtract = subtract+fillMask




