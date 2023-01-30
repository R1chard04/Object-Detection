import cv2 as cv
import numpy as np
import os

class recalibrate:
    def __init__(self, noPart, part, maskPath) -> None:
        self.partImg = part
        self.noPartImg = noPart
        self.maskPath = maskPath

    def setSTANDARD:
        # Overwrite the standard picture
        photoName = "STANDARD"
        # dirName = "mask_pics"
        ctrl = dai.CameraControl()
        ctrl.setCaptureStill(True)
        qControl.send(ctrl)
        print("Sent 'still' event to the camera")

    def setNONE:
        # Overwrite the none part picture
        photoName = "NONE"
        # dirName = "mask_pics"
        ctrl = dai.CameraControl()
        ctrl.setCaptureStill(True)
        qControl.send(ctrl)
        print("Sent 'still' event to the camera")
    
    def maskGenertion(self):
        #Subtracting the two images to find the part area
        subtractOG = cv.cvtColor(self.partImg,cv.COLOR_BGR2GRAY) - cv.cvtColor(self.noPartImg,cv.COLOR_BGR2GRAY)

        '''
        partImg = cv.imread('mask_pics\\STANDARD.jpg') # ?? img
        noPartImg = cv.imread('mask_pics\\NONE.jpg')        # ?? no
        #Subtracting the two images to find the part area
        subtractOG = cv.cvtColor(partImg,cv.COLOR_BGR2GRAY) - cv.cvtColor(noPartImg,cv.COLOR_BGR2GRAY)

        '''


        #Applying filters on image
        alpha = 3 # Contrast control (rec 1-3)
        beta = -300 # Brightness control (rec -300 <-> 300)
        subtractOG = cv.convertScaleAbs(subtractOG, alpha=alpha, beta=beta)
        subtractOG = cv.fastNlMeansDenoising(subtractOG, None, 40, 7, 15)
        subtractOG = cv.fastNlMeansDenoising(subtractOG, None, 40, 7, 15)

        #Black and white configuration
        subtractOG = cv.bitwise_not(subtractOG)
        subtractOG[subtractOG < 10] = 0
        subtractOG[subtractOG != 0] = 255

        #Filling gaps
        thresh, imgThresh = cv.threshold(subtractOG,200,255,cv.THRESH_BINARY)
        fillMask = imgThresh.copy()
        height, width = imgThresh.shape[:2]
        mask = np.zeros((height+2,width+2),np.uint8)
        cv.floodFill(fillMask, mask,(0,0),(255,255,255))

        fillMask = cv.bitwise_not(fillMask)
        
        #Filling gaps
        subtractOG = subtractOG+fillMask
        
        cv.imwrite("mask.jpg")

        return subtractOG, 


