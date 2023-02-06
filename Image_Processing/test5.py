# this is a test creating mask by adding 2 subtractions together
import cv2 as cv
import numpy as np
import os

img1 = cv.imread("Object_Detection\\testPics\\ready-STA100.jpg")
# img2 = cv.imread("Image_Processing\photos\Test\Reference\WIN_20230123_10_46_36_Pro.jpg")
none = cv.imread("Object_Detection\\testPics\empty-STA100.jpg")

subtract1 = cv.absdiff(img1, none)
# subtract2 = cv.absdiff(img2, none)

# result = cv.absdiff(subtract1, subtract2)

cv.imshow("hello.jpg", subtract1)
cv.waitKey(0)