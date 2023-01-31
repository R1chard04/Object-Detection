import cv2 as cv
import numpy as np

partImg = cv.imread('Image-Masking\mask_pics\STANDARD.jpg')
noPartImg = cv.imread('Image-Masking\mask_pics/NONE.jpg')

BGR = cv.subtract(partImg,noPartImg)
BGR = cv.GaussianBlur(BGR,(3,3),0)
# BGR = cv.cvtColor(BGR, cv.COLOR_BGR2GRAY)
 

gray = cv.cvtColor(BGR, cv.COLOR_BGR2GRAY)
thresh = cv.threshold(gray, 130, 255, cv.THRESH_BINARY)[1]
thresh = cv.fastNlMeansDenoising(thresh, None, 40, 7, 15)
# HSV = cv.cvtColor(thresh,cv.COLOR_BGR2HSV)

# add = cv.add(gray, thresh)
# add = cv.medianBlur(add, 15, 15)
# add = cv.threshold(add, 254, 255, cv.THRESH_BINARY)[1]



# # detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
# contours, hierarchy = cv.findContours(image = add, mode=cv.RETR_TREE, method=cv.CHAIN_APPROX_NONE)

      

# # draw contours on the original image
# image_copy = partImg.copy()
# cv.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=1, lineType=cv.LINE_AA)

# #Applying filters on image
# alpha = 3 # Contrast control (rec 1-3)
# beta = -300 # Brightness control (rec -300 <-> 300)
# subtract = cv.convertScaleAbs(subtract, alpha=alpha, beta=beta)
# subtract = cv.bitwise_not(subtract) #inverts

# 
# subtract = cv.fastNlMeansDenoising(subtract, None, 40, 7, 15)

# # #Black and white configuration



# #Filling gaps
# thresh, imgThresh = cv.threshold(subtract,200,255,cv.THRESH_BINARY)
# fillMask = imgThresh.copy()
# height, width = imgThresh.shape[:2]
# mask = np.zeros((height+2,width+2),np.uint8)
# cv.floodFill(fillMask, mask,(0,0),(255,255,255))

# fillMask = cv.bitwise_not(fillMask)

# #Filling gaps
# subtract = subtract+fillMask





#Resize and show
img = cv.resize(thresh, (0,0), fx = 0.35, fy = 0.35)
cv.imwrite("Image-Masking\mask_pics\MASK.jpg",thresh)
cv.imshow("MASK",img)
cv.waitKey(0)