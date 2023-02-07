import cv2 as cv
import numpy as np

std = cv.imread("AutoMask\mask_pics\\STANDARD1.jpg")
na = cv.imread("AutoMask\mask_pics\\NONE1.jpg")

subtract1 = cv.subtract(std,na)

na = cv.subtract(na, subtract1)


# hsv = cv.cvtColor(na, cv.COLOR_BGR2HSV)
# h,s,v = cv.split(hsv)

# cv.imshow("h",cv.resize(h, (0,0), fx = 0.2, fy = 0.2))
# cv.imshow("s",cv.resize(s, (0,0), fx = 0.2, fy = 0.2))
# cv.imshow("v",cv.resize(v, (0,0), fx = 0.2, fy = 0.2))

# hs = cv.merge([h,s,v])
cv.imshow("h",cv.resize(na, (0,0), fx = 0.2, fy = 0.2))

cv.waitKey(0)