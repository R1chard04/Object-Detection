# import libraries
import cv2 as cv
import numpy as np
import glob as glob
from calibration import cameraCalibration
from undistortion import undistortion
from remapping import remapping
from reprojection import reprojection
from stitching import stitching

#################### STITCHING THE IMAGE ###############
image_paths = ['Photos/myImage1.png', 'Photos/myImage2.png']
imgs = []
myStitching = stitching
myStitching.imageStitching(image_paths, imgs)

#################### SETUP OBJECTS #################
# First of all, find the corners - objPoints and imagePoints
# Declare the object size and frame size of the camera
chessboardSize = (24,17) # chessboard's size
frameSize = (1440,1080) # frame's size

# Standard termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare the object points
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0], 0:chessboardSize[1]].T.reshape(-1,2)

# 2 arrays to store the object points and image points from all of the images
objPoints = [] # 3D points in real world space
imgPoints = [] # 2D points in image plane

# start opening the images in the images folder
images = glob.glob('Photos/Image5.png')

# for loop to read in each image that is stored inside the folder
for image in images:
    print(image) # print image each time the loop overlap
    img = cv.imread(image) # read in each image
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) # convert the image into grayscale

    # Find the chessboard corners
    ret, corners = cv.findChessboardCorners(gray, chessboardSize, None)

    # If found the corners, add the object points and image points into the array
    if ret == True:
        objPoints.append(objp) 
        corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        imgPoints.append(corners)

        # Draw and display the corners on the image
        cv.drawChessboardCorners(img, chessboardSize, corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(100000)

# destroy all the windows after completing the for loop
cv.destroyAllWindows()

################### CALIBRATIONS #################
myCalibration = cameraCalibration
ret, cameraMatrix, dist, rvecs, tvecs = myCalibration.calibration(objPoints, imgPoints, frameSize)


################## UNDISTORT THE IMAGE ####################
img = cv.imread("Photos/Image5.png") # start reading an image
w,h = img.shape[:2] # set the width and height
newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))
myDistortion = undistortion()
myDistortion.imageDistortion(image, cameraMatrix, dist, newCameraMatrix, roi)

################# REMAPPING METHOD #######################
myRemapping = remapping()
myRemapping.imageRemapping(cameraMatrix, dist, newCameraMatrix, w, h, roi)

################# REPROJECTION ERRORS #####################
# initialize the mean error
mean_error = 0
myReprojection = reprojection()
myReprojection.myReprojection(objPoints, rvecs, tvecs, cameraMatrix, dist, imgPoints)