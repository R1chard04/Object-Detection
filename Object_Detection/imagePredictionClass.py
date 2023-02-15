import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import pdb

# declare arrays to store the errors for top, left, bottom, right
myArray0 = []
myArray1 = []
myArray2 = []
myArray3 = []
totalArray = [myArray0, myArray1, myArray2, myArray3]

def getPassRef(error, final):
    for i in range(len(error)):
        if final[i] < error[i]:
            final[i] = error[i] * 3
    return final
# for live video
class MSEStabilization:
    def __init__(self, errors, passRef) -> None:
        self.errors = errors
        self.passRef = passRef
    
    def result(self) -> list:
        # declare the result to store the string "pass" or "fail"
        resultTop = []
        resultLeft = []
        resultBottom = []
        resultRight = []
        totalResult = [resultTop, resultLeft, resultBottom, resultRight]
        for i in range(4):
            totalArray[i].append(self.errors[i])
            ans = self.errors[i] - self.passRef[i]
            if ans <= 0:
                totalResult[i].append("PASS")
            else:
                totalResult[i].append("FAIL")
        return totalResult
    
             

        
    