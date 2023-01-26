import cv2 as cv
import numpy as np

img = cv.imread('Image-Masking\STANDARD.jpg')
no = cv.imread('Image-Masking\WIN_20230123_10_47_10_Pro.jpg')
subtractOG = cv.cvtColor(img,cv.COLOR_BGR2GRAY) - cv.cvtColor(no,cv.COLOR_BGR2GRAY)
# subtractOG = cv.cvtColor(no,cv.COLOR_BGR2GRAY) - cv.cvtColor(img,cv.COLOR_BGR2GRAY)

alpha = 3 # Contrast control (rec 1-3)
beta = -300 # Brightness control (rec -300 <-> 300)

subtractOG = cv.convertScaleAbs(subtractOG, alpha=alpha, beta=beta)

subtractOG = cv.fastNlMeansDenoising(subtractOG, None, 40, 7, 15)
subtractOG = cv.fastNlMeansDenoising(subtractOG, None, 40, 7, 15)
subtractOG = cv.bitwise_not(subtractOG)


subtractOG[subtractOG < 20] = 0
cv.imshow("img", subtractOG)
for i in range(2):
    # subtractOG[subtractOG < 20] = 0
    subtractOG = cv.GaussianBlur(subtractOG,(5,5),0)
    subtractOG = cv.fastNlMeansDenoising(subtractOG, None, 40, 3, 3)
    subtractOG[subtractOG != 0] = 255

scale_percent = 70 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
  
# resize image
resized = cv.resize(subtractOG, dim, interpolation = cv.INTER_AREA)
cv.imshow("Resized image", resized)
cv.imwrite("subtractOG.jpg",subtractOG)
cv.waitKey(0)
