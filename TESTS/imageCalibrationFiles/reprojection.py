# import libraries
import cv2 as cv

# class implementation
class reprojection:
    def __init__(self) -> None:
        pass

    def myReprojection(mean_error, objPoints, rvecs, tvecs, cameraMatrix, dist, imgPoints) -> None:
        for i in range(len(objPoints)):
            imgPoints2, _ = cv.projectPoints(objPoints[i], rvecs[i], tvecs[i], cameraMatrix, dist)
            error = cv.norm(imgPoints[i], imgPoints2, cv.NORM_L2)/len(imgPoints2)
            mean_error += error

        print("\ntotal_error: {}".format(mean_error/len(objPoints)))
        print("\n\n\n")