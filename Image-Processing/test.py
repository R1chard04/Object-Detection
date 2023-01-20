import cv2 as cv
import numpy as np
import os
from os import listdir
import sys

maskImg = cv.imread('Image-Processing\photos\Small\Mask.jpg')

folderDirectory = "Image-Processing\photos\Small\Original"
imageIndex = 0

for image in os.listdir(folderDirectory):

    if (image.endswith(".jpg")):
        imagePath = os.path.join(folderDirectory, image)
        print(imageIndex, image, imagePath)
        imageIndex += 1

        img = cv.imread(imagePath)

        grayMask = cv.cvtColor(maskImg, cv.COLOR_BGR2GRAY)
        (thresh, im_bw) = cv.threshold(grayMask, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
        thresh = 127
        binaryMask = cv.threshold(grayMask, thresh, 255, cv.THRESH_BINARY)[1]

        result = cv.bitwise_and(img,img, mask= binaryMask)
        cv.imshow("masked",result)

        # scale_percent = 50 # percent of original size
        # width = int(img.shape[1] * scale_percent / 100)
        # height = int(img.shape[0] * scale_percent / 100)
        # dim = (width, height)
        # img = cv.resize(img, dim, interpolation = cv.INTER_AREA)

        # alpha = 3 # Contrast control (1.0-3.0)
        # beta = 0 # Brightness control (0-100)
        # adjusted = cv.convertScaleAbs(img, alpha=alpha, beta=beta)
        # cv.imshow('adjusted', adjusted)
        
        # gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # dns = cv.fastNlMeansDenoising(gray,None,15,7,21)
        
  
        # # Find Canny edges
        # edged = cv.Canny(dns, 30, 200)
        
        # Finding Contours
        # Use a copy of the image e.g. edged.copy()
        # since findContours alters the image
        # contours, hierarchy = cv.findContours(edged, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        
        # print("Number of Contours found = " + str(len(contours)))
        
        # # Draw all contours
        # # -1 signifies drawing all contours
        # cv.drawContours(dns, contours, -1, (0, 255, 0), 2)
        
        # cv.imshow('Contours', dns)

        # gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        

        # cv.imshow('img', show)
        cv.waitKey(0)








# # Edge Cascade
# canny = cv2.Canny(adjusted, 15, 175)
# cv2.imshow('Canny Edges', canny)

# cv2.waitKey(0)