import cv2 as cv
import numpy as np

class imageFiltering:
    def __init__(self) -> None:
        pass

    def mse(img1, img2):
        height, width = img1.shape
        diffImg = cv.subtract(img1, img2)
        err = np.sum(diffImg**2)
        ans = err/(float(height*width)) #Closer to 0 is better
        return ans, diffImg

filteringObject = imageFiltering()

class imageProcessing:
    def __init__(self, maskImg, refImg, testImg) -> None:
        self.maskImg = filteringObject.filterMask(maskImg)
        self.refImg = filteringObject.filterImage(refImg, self.maskImg)
        self.testImg = filteringObject.filterImage(testImg, self.maskImg)

    def setTestImg(self, img) -> None:
        self.testImg = img

    def setRefImg(self, img) -> None:
        self.refImg = img

    def setMaskImg(self, img) -> None:
        self.maskImg = img

    def compareImage(self):

        ref = cv.bitwise_and(self.refImg, self.refImg, mask = self.maskImg)
        test = cv.bitwise_and(self.testfImg, self.testImg, mask = self.maskImg)

        error, diffImg = filteringObject.mse(test, ref)
        return error






