import cv2 as cv
import numpy as np

# from imagePredictionClass import Prediction

def mse(img1, img2, pixels):
    # height, width = img1.shape
    diffImg = cv.absdiff(img1, img2)
    err = np.sum(diffImg**2)
    ans = err/ float(pixels)
    #Closer to 0 is better
    return ans

class imageProcessing:
    def __init__(self, maskArray, ref, test, partList) -> None:

        self.masks = maskArray
        self.masksPixels = []
        self.parts = partList
        
        # calculate position for displaying result
        self.output_y = []
        self.output_x = []

        x2 = ref.shape[1] - 60
        y2 = ref.shape[0] - 60
        x1 = x2 - 1000
        for i in range(len(partList)):
            
            # count num of white pixels for each masks
            pixels = np.sum(self.masks[0])
            self.masksPixels.append(pixels)
            
            # count the pixel position to display result
            self.output_y.append(y2 -40 -90* (len(partList) - i -1))    
        # text location for the parts
        self.output_x.append(x1 + 10)
        # text location for the mseResults
        self.output_x.append(x1 + 400)
        self.line_p1 = (x1+20, self.output_y[0]-100)
        self.line_p2 = (x2 -10,self.output_y[0]-100)

        
        self.ref = ref  
        self.test = test
        self.MSEResults = [0]*4
        

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
            # pdb.set_trace()
            ref = cv.bitwise_and(self.ref, self.ref, mask = self.masks[i])
            
            test = cv.bitwise_and(self.test, self.test, mask = self.masks[i])
            error = mse(test, ref, self.masksPixels[i])

            errors.append(error*100)

        self.MSEResults = errors
        return errors
    
    def displayResultPosition(self):
        
        frame = self.test
        partsFontthickness = 3
        fontColor = (75, 25 ,23)
        partsFontScale = 3
        font = cv.FONT_HERSHEY_SIMPLEX

        x2 = frame.shape[1] - 60
        y2 = frame.shape[0] - 60
        x1 = x2 - 1000
        y1 = self.output_y[0] - 205

        frame = cv.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), -1)
        frame = cv.putText(frame, "RESULTS", (self.output_x[0] , self.output_y[0] - 120), font, partsFontScale, fontColor, partsFontthickness+3)
        frame = cv.line(frame, self.line_p1, self.line_p2, fontColor, 3)


        i = len(self.parts) -1
        while i >= 0:
            frame = cv.putText(frame, self.parts[i], (self.output_x[0], self.output_y[i]), font, partsFontScale, fontColor, partsFontthickness)
            frame = cv.putText(frame, str(round(self.MSEResults[i],3)), (self.output_x[1], self.output_y[i]), font, partsFontScale, fontColor, partsFontthickness)
            i = i -1
            
        return frame