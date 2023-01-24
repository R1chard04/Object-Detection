import cv2 as cv

# class implementation
class cameraCalibration:
    def __init__(self) -> None:
        pass

    def calibration(objPoints, imgPoints, frameSize) -> any:
        ret, cameraMatrix, dist, rvecs, tvecs = cv.calibrateCamera(objPoints, imgPoints, frameSize, None, None)
        
        # print out the values
        print("Camera Calibrated: ", ret)
        print("\nCamera Matrix:\n", cameraMatrix)
        print("\nDistortion Parameters:\n", dist)
        print("\nRotation Vectors:\n", rvecs)
        print("\nTransition Vectors:\n", tvecs)

        # return the values for undistortion process
        return ret, cameraMatrix, dist, rvecs, tvecs