import os
import cv2 as cv
import numpy as np

def mse(img1, img2):
    height, width, channels = img1.shape
    diffImg = cv.subtract(img1, img2)
    err = np.sum(diffImg**2)
    ans = err/(float(height*width))  #Closer to 0 is better
    return ans, diffImg

ref = cv.imread("Object_Detection\Photos\STD\STD1.jpg")
mask = cv.imread("Object_Detection\Photos\mask.jpg", cv.IMREAD_GRAYSCALE)
mask = cv.resize(mask, None, fx=1.875, fy=1.875, interpolation = cv.INTER_LINEAR)
mask[mask != 0 ] = 255

std = cv.bitwise_and(ref, ref, mask = mask)

dirName = "Object_Detection\Photos\INIT"
for images in os.listdir(dirName):
    path = os.path.join(dirName, images)
    img = cv.imread(path)

    img = cv.bitwise_and(img, img, mask = mask)

    error, diff = mse(img, std)

    print(error)