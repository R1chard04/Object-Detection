# !!!!! THIS IS A SECOND METHOD TO UNDISTORT THE IMAGE !!!!!
# import libraries
import cv2 as cv

# class implementation
class remapping:
    def __init__(self) -> None:
        pass
    
    def imageRemapping(img, cameraMatrix, dist, newCameraMatrix, w, h, roi) -> None:
        # start remapping the image using the matrix of the camera
        mapx, mapy = cv.initUndistortRectifyMap(cameraMatrix, dist, None, newCameraMatrix, (w,h), 5)
        dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)
        # crop the image
        x,y,w,h = roi
        dst = dst[y:y+h, x:x+w]
        cv.imwrite("resultImage2.png", dst)