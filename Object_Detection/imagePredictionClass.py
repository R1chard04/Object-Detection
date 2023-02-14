import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# declare arrays to store the errors for top, left, bottom, right
myArray0 = []
myArray1 = []
myArray2 = []
myArray3 = []
totalArray = [myArray0, myArray1, myArray2, myArray3]

# function that get the pass reference 
def getPassRef(errors) -> list:
    # declare the pass reference list for top, left, bottom, right
    passRef = [[], [], [], []]  
    for i in range(4):
        passRef[i].append(errors[i])
    
    # get the maximum pass rate in the pass reference
    greatestNumber = 0
    finalpassRef = []
    for j in len(passRef):
        for k in len(j):
            if greatestNumber < passRef[j][k]:
                greatestNumber = passRef[j][k]
        finalpassRef.append(greatestNumber)
    return finalpassRef

# for live video
class MSEStabilization:
    def __init__(self, errors) -> None:
        self.errors = errors
    
    def result(self) -> list:
        # declare the result to store the string "pass" or "fail"
        resultTop = []
        resultLeft = []
        resultBottom = []
        resultRight = []
        totalResult = [resultTop, resultLeft, resultBottom, resultRight]
        for i in range(len(totalArray)):
            totalArray[i].append(self.errors[i])
            ans = self.errors[i] - getPassRef(self.errors)[i]
            if ans >= 0:
                totalResult[i].append("PASS")
            else:
                totalResult[i].append("FAIL")
        return totalResult
        
    

             

        
    