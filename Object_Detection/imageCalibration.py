import cv2 as cv
from imageCalibrationFiles.setup import setupImages
from imageCalibrationFiles.calibration import cameraCalibration
from imageCalibrationFiles.undistortion import undistortion
from imageCalibrationFiles.reprojection import reprojection
from imageCalibrationFiles.remapping import remapping

# initialize variables for setting up the images
objectSize = (24,17) # use chessboard size
frameSize = (1440,1080)
objPoints = [] # 3D points in real world space
imgPoints = [] # 2D points in image plane

class imageCalibration:
    def __init__(self, imgPath) -> None:
        self.imgPath = imgPath

    def imageCalibration(self) -> any:
        # set up the image
        imageSetUp = setupImages(self.imgPath, objectSize, frameSize, objPoints, imgPoints)
        imageSetUp.setupImages()

        # calibrate the images
        myCalibration = cameraCalibration(objPoints, imgPoints, frameSize)
        ret, cameraMatrix, dist, rvecs, tvecs = myCalibration.calibration()

        # undistort the image
        img = cv.imread(self.imgPath) # start reading an image
        w,h = img.shape[:2] # set the width and height
        newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))
        myDistortion = undistortion()
        myDistortion.imageDistortion(img, cameraMatrix, dist, newCameraMatrix, roi)

        # remapping method to undistort the image
        myRemapping = remapping()
        myRemapping.imageRemapping(cameraMatrix, dist, newCameraMatrix, w, h, roi)

        # reprojection errors
        # initialize the mean error
        mean_error = 0
        myReprojection = reprojection()
        myReprojection.myReprojection(mean_error,objPoints, rvecs, tvecs, cameraMatrix, dist, imgPoints)
