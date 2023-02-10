import cv2 as cv
import numpy as np


def mse(img1, img2):
    height, width, channels = img1.shape
    diffImg = cv.absdiff(img1, img2)
    err = np.sum(diffImg**2)
    ans = err/(float(height*width))  
    #Closer to 0 is better
    return ans, diffImg

class imageProcessing:
    def __init__(self, maskImg, refImg, testImg, parts) -> None:
        self.maskImg = maskImg
        self.refImg = refImg
        self.testImg = testImg
        # ['top.jpg', 'left.jpg', 'bottom.jpg', 'right.jpg']
        self.slicedRef = [refImg, refImg, refImg, refImg]
        self.slicedTestImgs = [refImg, refImg, refImg, refImg] 
        # self.slicedTestImgs = ["imagePath"]* len(parts) # initialize a empty list w num of parts ""
        # self.mseResults = [0]*4
        self.height = 2160
        self.width = 3840

    def setTestImg(self, img) -> None:
        self.testImg = img

    def setRefImg(self, img) -> None:
        
        # slice the ref images
        tmp = [img,img,img,img]
        self.refImg = img
    
        tmp[0] = self.refImg[:self.height//2, :self.width] # top
        tmp[1] = self.refImg[:self.height, :self.width//2] # left
        tmp[2] = self.refImg[self.height//2:, :self.width] # bottom
        tmp[3] = self.refImg[:self.height, :self.width//2] # right
        self.refImg = tmp

    def setMaskImg(self, img) -> None:
        self.maskImg = img

    def setFrame(self, img) -> None:
        # call the slicing method, slice the pic and save it to the array
        pass
    
    def compareImage(self):
        
        # return a result array
        i = 0
        MSEResults = [0]*4
        
        # comparing all the parts individually
        while i < len(self.parts):
            ref = cv.bitwise_and(self.slicedRef[i], self.slicedRef[i], mask = self.maskImg[i])
            test = cv.bitwise_and(self.slicedTestImgs[i], self.slicedTestImgs[i], mask = self.maskImg[i])
            error, diffImg = mse(test, ref)
            MSEResults[i] = error
        return MSEResults

    def sliceStation100(self) ->None:
        # slice the images in four parts 
        self.slicedTestImgs[0] = self.testImg[:self.height//2, :self.width] # top
        self.slicedTestImgs[1] = self.testImg[:self.height, :self.width//2] # left
        self.slicedTestImgs[2] = self.testImg[self.height//2:, :self.width] # bottom
        self.slicedTestImgs[3] = self.testImg[:self.height, :self.width//2] # right
        
    
    def displayResultPosition(self):
        # calculate the pixel value to display the part pics
        pass