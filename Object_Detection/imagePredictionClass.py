import cv2 as cv
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# calculuate the mean square errors 
# def mse(img1, img2):
#     # img1 is the reference mask
#     # img2 is the test mask
#     height, width, channels = img1.shape
#     diffImg = cv.absdiff(img1, img2)
#     err = np.sum(diffImg**2)
#     # divide the error by the total white pixels of the mask image
#     # convert reference mask image into grayscale
#     gray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)

     # Threshold the image to get only the white pixels
#     _, thresh = cv.threshold(gray, 250, 255, cv.THRESH_BINARY)
    
#     # Find the coordinates of all the white pixels
#     coords = np.column_stack(np.where(thresh == 255))

#     # Get the proportion between the error and the white pixels
#     ans = err/float(coords.shape[0])

#     return ans, diffImg

# Sort an array
def sortArray(error) -> list:
    if len(error) <= 1:
        return error
    median = error[0]
    smaller = [x for x in error[1:] if x <= median]
    greater = [x for x in error[1:] if x > median]
    return sortArray(smaller) + median + sortArray(greater) 

class Prediction:
    def __init__(self, errors, response) -> None:
        self.errors = errors
        self.response = response
        
    def trend(self) -> object: 
        # sort the errors into ascending order
        sorted_errors = sortArray(self.errors)

        # convert the list of errors to a 2D Array
        sorted_errors = np.array(sorted_errors).reshape(-1,1)

        # Define the response variable (pass/fail)
        for i in len(sorted_errors):
            if i == 0:
                self.response.append(1)
            else:
                self.response.append(0)
        
        # Create a linear regression object
        regr = LinearRegression()

        # Fit the linear regression model to the data
        regr.fit(np.array(self.errors).reshape(-1, 1), np.array(self.response).reshape(-1, 1))

        return regr
    
    def prediction(self, new_errors, myRegr) -> list:
        # Make predictions for a new set of errors
        predictions = myRegr.predict(new_errors)

        # Convert the predictions to binary (pass/fail)
        predictions = np.round(predictions)
        return predictions