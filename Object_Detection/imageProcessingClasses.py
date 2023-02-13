import cv2 as cv
import numpy as np

from imagePredictionClass import Prediction

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

class imageProcessing:
    def __init__(self, maskArray, ref, test, partList) -> None:

        self.masks = maskArray
        self.ref = ref  
        self.test = test
        self.MSEResults = []
        self.parts = partList

    def setTestImg(self, img) -> None:
        self.test = img

    def setRefImg(self, img) -> None:
        self.ref = img

    def setMaskImg(self, array) -> None:
        self.masks = array
    
    def compareImage(self):
        
        # return a result array
        errors = []
    
        for i in range(len(self.masks)):
            ref = cv.bitwise_and(self.ref, self.ref, mask = self.masks[i])
            test = cv.bitwise_and(self.test, self.test, mask = self.masks[i])
            error = mse(test, ref)

            errors.append(error)

        self.MSEResults = errors
        return errors
    
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
    