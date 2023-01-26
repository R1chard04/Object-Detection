# import libraries
import cv2 as cv

# class implementation
class undistortion:
    def __init__(self) -> None:
        pass

    def imageDistortion(img, cameraMatrix, dist, newCameraMatrix, roi) -> None:
        # initialize the variable
        dst = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix)
        # crop the image
        x,y,w,h = roi
        dst = dst[y:y+h, x:x+w]
        cv.imwrite("resultImage1.png", dst)