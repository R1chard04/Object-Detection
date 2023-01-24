import cv2 as cv
import numpy as np

class imageFiltering:
    def __init__(self) -> None:
        pass
    def filterImage(img, mask):
        #Filter
        alpha = 3 # Contrast control (rec 1-3)
        beta = 0 # Brightness control (rec -300 <-> 300)
                
        img = cv.convertScaleAbs(img, alpha=alpha, beta=beta)
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img = cv.bitwise_and(img,img, mask = mask)
        return img

    def filterMask(maskImg):
        maskImg = cv.cvtColor(maskImg, cv.COLOR_BGR2GRAY)
        (maskImgThresh, maskImgBW) = cv.threshold(maskImg, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
        thresh = 127
        maskBinary = cv.threshold(maskImg, maskImgThresh, 255, cv.THRESH_BINARY)[1]

        return maskBinary

    def mse(img1, img2):
        height, width = img1.shape
        diffImg = cv.subtract(img1, img2)
        err = np.sum(diffImg**2)
        ans = err/(float(height*width)) #Closer to 0 is better
        return ans, diffImg

filteringObject = imageFiltering()

class imageProcessing:
    def __init__(self, maskImg, refImg, testImg, reportFilepath, testImgPath) -> None:
        self.maskImg = filteringObject.filterMask(maskImg)
        self.refImg = filteringObject.filterImage(refImg, self.maskImg)
        self.testImg = filteringObject.filterImage(testImg, self.maskImg)
        self.reportFilepath = reportFilepath
        self.testImgPath = testImgPath

    def setTestImg(self, img, imgPath) -> None:
        self.testImg = filteringObject.filterImgage(img, self.maskImg)
        self.testImgPath = imgPath

    def compareImage(self):
        report = open(self.reportFilepath, "a")
        report.write("\n"+self.testImgPath)

        error, diffImg = filteringObject.mse(self.testImg, self.refImg)

        # report.write(str(error))
        # report.write(" Pass") if error < 0.1 else report.write(" Fail")  

        report.write(" Here")
        report.close()
        # for this mask, the set tolerance is 0.1, this seems to work best, but this is experimentally tested (which isn't awesome)
        return bool(error<0.1)






