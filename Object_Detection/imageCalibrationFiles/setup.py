# import libraries
import cv2 as cv
import numpy as np
import glob as glob


#################### SET UP THE IMAGES FOR CALIBRATION ######################
# Standard termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Create a class to setup the images
class setupImages:
    def __init__(self, objectSize, frameSize, objPoints, imgPoints, imagesPath) -> None:
        self.objectSize = objectSize
        self.frameSize = frameSize
        self.objPoints = objPoints
        self.imgPoints = imgPoints
        self.imagesPath = imagesPath # a path to the images folder -> string 
    
    def setupImages(self) -> any:
        # Prepare the object points
        objp = np.zeros((self.objectSize[0] * self.objectSize[1], 3), np.float32)
        objp[:,:2] = np.mgrid[0:self.objectSize[0], 0:self.objectSize[1]].T.reshape(-1,2)

        # start opening the images folder
        images = glob.glob(self.imagesPath)

        # for loop to read in each image that is stored inside the folder
        for image in images:
            cv.imshow('Original Image', img)
            print(image) # print the image each time the loop overlap
            img = cv.imread(image) # read in each image
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) # convert the image into grayscale

            # find the chessboard corners
            ret, corners = cv.findChessboardCorners(gray, self.objectSize, None)

            # If found the corners, add the object points and image points into the 2 arrays
            if ret == True:
                (self.objPoints).append(objp)
                corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1.,-1), criteria)
                (self.imgPoints).append(corners)

                # Draw and display the corners on the image
                cv.drawChessboardCorners(img, self.objectSize, corners2, ret)
                cv.imshow('Calibrated Image', img)

        # destroy all the windows afrer completing the for loop
        cv.destroyAllWindows()