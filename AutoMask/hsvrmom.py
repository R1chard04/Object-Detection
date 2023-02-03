import cv2 as cv
import numpy as np
from functions import floodFill, denoiseWhite, fillHoles

std = cv.imread("AutoMask\mask_pics\\STANDARD5.jpg")
na = cv.imread("AutoMask\mask_pics\\NONE5.jpg")

std = cv.cvtColor(std, cv.COLOR_BGR2HSV_FULL)
na = cv.cvtColor(na, cv.COLOR_BGR2HSV_FULL)

subtract = cv.subtract(std,na)
subtract = cv.cvtColor(subtract, cv.COLOR_HSV2BGR)
subtract = cv.cvtColor(subtract, cv.COLOR_BGR2GRAY)

result = cv.fastNlMeansDenoising(subtract,(3,3))
# result = cv.GaussianBlur(subtract,(5,5), 7, 15)
# result[result < 30] = 0
result = cv.bilateralFilter(subtract, 9, 75,75)
# result = cv.medianBlur(subtract,11,11)
result[result < 40] = 0
result[result > 10] = 255

cv.imshow("ref", cv.resize(result, (0,0), fx = 0.2, fy = 0.2))
cv.imwrite("std.jpg", result)
cv.waitKey(0)
cv.destroyAllWindows()