import cv2 as cv
import numpy as np
from imagePredictionClass import Prediction
from imageSlicingClasses import imageSlicing, input_number

def mse(img1, img2):
    # height, width = img1.shape
    diffImg = cv.absdiff(img1, img2)
    err = np.sum(diffImg**2)
    ans = err/(float(2160*3840))  
    #Closer to 0 is better
    return ans

# a list of response to compare with the errors
response = []
myArray0 = []
myArray1 = []
myArray2 = []
myArray3 = []




input_number_array = []
input_number(input_number_array)

class imageProcessing:
    def __init__(self, station, maskArray, refArray, testArray) -> None:

        self.station = station
        self.parts = ["Top", "Left", "Bottom", "Right"]

        self.masks = maskArray
        self.refs = refArray  
        self.tests = testArray 
        
        #needs to be fixed
        self.MSEResults = [0]*4
        self.height = 2160
        self.width = 3840

    def setTestImg(self, array) -> None:
        self.tests = array

    def setRefImg(self, array) -> None:
        self.refs = array

    def setMaskImg(self, array) -> None:
        self.masks = array
    
    def compareImage(self):
        
        # return a result array
        i = 0
        while i < 4:
            ref = cv.bitwise_and(self.refs[i], self.refs[i], mask = self.masks[i])
            test = cv.bitwise_and(self.tests[i], self.tests[i], mask = self.masks[i])
            error = mse(test, ref)

            self.MSEResults[i] = error
            if i == 0:
                myArray0.append(self.MSEResults[i])
            elif i == 1:
                myArray1.append(self.MSEResults[i])
            elif i == 2:
                myArray2.append(self.MSEResults[i])
            else:
                myArray3.append(self.MSEResults[i])
            i += 1
        
    def sliceStation100(self, img) ->None:
        
        self.slicedTestImgs = imageSlicing(self.testImg, [1, 2, 3, 4]).slice_image()
        
        # self.slicedTestImgs[0] = self.testImg[:self.height//2, :self.width] # top
        # self.slicedTestImgs[1] = self.testImg[:self.height, :self.width//2] # left
        # self.slicedTestImgs[2] = self.testImg[self.height//2:, :self.width] # bottom
        # self.slicedTestImgs[3] = self.testImg[:self.height, :self.width//2] # right
    
    def displayResultPosition(self):
        
        frame = self.testImg
        # 2160*3840 window size
        font = cv.FONT_HERSHEY_SIMPLEX
        
        blue = (75, 25 ,23)
        shift_x = 10
        shift_x_error = 400
        gap = 90
        partsFontScale = 3
        partsFontthickness = 4

        text_x = 2980
        text_y = 1700
        # 2160*3840
        box_x1 = text_x 
        box_x2 = 3780
        box_y1 = 1700 - 115
        box_y2 = 2100

        # start_point, end_point
        frame = cv.rectangle(frame, (box_x1, box_y1), (box_x2, box_y2), (255, 255, 255), -1)
        title_y = 1610+60 #1610
        line_y = title_y +20

        frame = cv.putText(frame, "RESULTS", (text_x + shift_x, title_y), font, partsFontScale, blue, partsFontthickness+3)
        frame = cv.line(frame, (box_x1 + 20, line_y), (box_x2-20, line_y), blue, 3)
        frame = cv.putText(frame, "Right: ", (text_x + shift_x, text_y + gap*4), font, partsFontScale, blue, partsFontthickness)
        frame = cv.putText(frame, str(self.MSEResults[3]), (text_x + shift_x + shift_x_error, text_y + gap*4), font, partsFontScale, blue, partsFontthickness)
        
        frame = cv.putText(frame, "Bottom: ", (text_x + shift_x, text_y + gap*3), font, partsFontScale, blue, partsFontthickness)
        frame = cv.putText(frame, str(self.MSEResults[2]), (text_x + shift_x + shift_x_error, text_y + gap*3), font, partsFontScale, blue, partsFontthickness)
        
        frame = cv.putText(frame, "Left: ", (text_x + shift_x, text_y + gap*2), font, partsFontScale, blue, partsFontthickness)
        frame = cv.putText(frame, str(self.MSEResults[1]), (text_x + shift_x + shift_x_error, text_y + gap*2), font, partsFontScale, blue, partsFontthickness)
        
        frame = cv.putText(frame, "Top: ", (text_x + shift_x, text_y + gap), font, partsFontScale, blue, partsFontthickness)
        frame = cv.putText(frame, str(self.MSEResults[0]), (text_x + shift_x + shift_x_error, text_y + gap), font, partsFontScale, blue, partsFontthickness)
        
        return frame
    