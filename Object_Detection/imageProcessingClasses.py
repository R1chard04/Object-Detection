import cv2 as cv
import numpy as np


def mse(img1, img2):
    height, width, channels = img1.shape
    diffImg = cv.subtract(img1, img2)
    err = np.sum(diffImg**2)
    ans = err/(float(height*width))  #Closer to 0 is better
    return ans, diffImg

class imageProcessing:
    def __init__(self, maskImg, refImg, testImg) -> None:
        self.maskImg = maskImg
        self.refImg = refImg
        self.testImg = testImg

    def setTestImg(self, img) -> None:
        self.testImg = img

    def setRefImg(self, img) -> None:
        self.refImg = img

    def setMaskImg(self, img) -> None:
        self.maskImg = img

    def compareImage(self):

        ref = cv.bitwise_and(self.refImg, self.refImg, mask = self.maskImg)
        test = cv.bitwise_and(self.testImg, self.testImg, mask = self.maskImg)

        error, diffImg = mse(test, ref)
        return error, diffImg






