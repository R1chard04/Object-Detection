import cv2 as cv
import numpy as np
import glob as glob


#################### SET UP THE IMAGES FOR CALIBRATION ######################
# Standard termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Create a class to setup the images
class setupImages:
    def __init__(self, frameSize, objPoints, imgPoints, imagesPath) -> None:
        self.frameSize = frameSize
        self.objPoints = objPoints
        self.imgPoints = imgPoints
        self.imagesPath = imagesPath # a path to the images folder -> string 
    
    def setupImages(self):
        # Prepare the object points
        objp = np.zeros((24*17, 3), np.float32)
        objp[:,:2] = np.mgrid[0:24, 0:17].T.reshape(-1,2)

           # start opening the images folder
        if isinstance(self.imagesPath, str):
            images = glob.glob(self.imagesPath)
        elif isinstance(self.imagesPath, list):
            images = [img for img in self.imagesPath if isinstance(img, str)]
        else:
            raise TypeError("Expected a string or a list of strings, but got:", type(self.imagesPath))

        # for loop to read in each image that is stored inside the folder
        for image in images:
            img = cv.imread(image) # read in each image
            print(image) # print the image each time the loop overlap
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) # convert the image into grayscale

            # find the chessboard corners
            ret, corners = cv.findChessboardCorners(gray, (24, 17), None)

            # If found the corners, add the object points and image points into the 2 arrays
            if ret == True:
                (self.objPoints).append(objp)
                corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1.,-1), criteria)
                (self.imgPoints).append(corners)

                # Draw and display the corners on the image
                cv.drawChessboardCorners(img, (24,17), corners2, ret)
                cv.imshow('Calibrated Image', img)

        # destroy all the windows afrer completing the for loop
        cv.destroyAllWindows()
