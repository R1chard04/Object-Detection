import cv2 as cv
import numpy as np
import os
from os import listdir
 

folderDirectory = "Image-Processing\photos\Depth\Original"

imageIndex = 0

for image in os.listdir(folderDirectory):

    if (image.endswith(".jpg")):
        imagePath = os.path.join(folderDirectory, image)
        print(imageIndex, image, imagePath)
        imageIndex += 1

        img = cv.imread(imagePath)
        
        scale_percent = 50 # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        img = cv.resize(img, dim, interpolation = cv.INTER_AREA)

        cv.imshow('img', show)
        cv.waitKey(0)



# dim = (width, height)
# img=cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
# cv2.imshow('img', img)

# dst = cv2.fastNlMeansDenoisingColored(img,None,9,9,7,21)
# cv2.imshow("denoised", dst)
# # gray = cv2.cvtColor(blurImg, cv2.COLOR_BGR2GRAY)

# alpha = 3 # Contrast control (1.0-3.0)
# beta = -300 # Brightness control (0-100)
# adjusted = cv2.convertScaleAbs(dst, alpha=alpha, beta=beta)
# # cv2.imshow('adjusted', adjusted)

# # Edge Cascade
# canny = cv2.Canny(adjusted, 15, 175)
# cv2.imshow('Canny Edges', canny)

# cv2.waitKey(0)