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
    def __init__(self, maskImg, refImg, testImg, testImgPath) -> None:
        self.maskImg = filteringObject.filterMask(maskImg)
        self.refImg = filteringObject.filterImage(refImg, self.maskImg)
        self.testImg = filteringObject.filterImage(testImg, self.maskImg)
        self.testImgPath = testImgPath

    def setTestImg(self, img, imgPath) -> None:
        self.testImg = filteringObject.filterImgage(img, self.maskImg)
        self.testImgPath = imgPath

    def compareImage(self):

        error, diffImg = filteringObject.mse(self.testImg, self.refImg)
        return bool(error<0.1)






