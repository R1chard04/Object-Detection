import cv2
import numpy as np

img1 = cv2.imread("Image-Processing\photos\Depth\Original\oriPosition1-2.jpg")
img2 = cv2.imread("Image-Processing\photos\Depth\Original\offPosition2-1.jpg")
# img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
# img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
diff = cv2.absdiff(img1, img2)
mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

th = 1
imask =  mask>th

canvas = np.zeros_like(img2, np.uint8)
canvas[imask] = img2[imask]

cv2.imwrite("result.png", canvas)