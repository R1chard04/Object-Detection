import cv2 as cv
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# declare arrays to store the errors for top, left, bottom, right
myArray0 = []
myArray1 = []
myArray2 = []
myArray3 = []
totalArray = [myArray0, myArray1, myArray2, myArray3]

class MSEStabilization:
    def __init__(self, errors, response) -> None:
        self.errors = errors
        self.response = response
    
    def appendErrors(self) -> list:
        for i in range(len(totalArray)):
            totalArray[i].append(self.errors[i])
            

        
    