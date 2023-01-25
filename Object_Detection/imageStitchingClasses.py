# import libraries
import numpy as np
import cv2 as cv
import glob
import imutils

class imageStitching:
    def __init__(self, image_paths, images) -> None:
        self.image_paths = image_paths
        self.images = images

    def stitchImgs(self) -> any:
        # open the images folder
        pathImgs = glob.glob(self.image_paths)
        self.images = []

        # a for loop to loop through the images
        for image in pathImgs:
            img = cv.imread(image)
            (self.images).append(img)
            cv.imshow("Image", img)
            cv.waitKey(0)

        # stitch an images
        imageStitcher = cv.Stitcher_create()

        # if not able to stitch images
        error, stitched_img = imageStitcher.stitch(self.images)

        if not error:
            cv.imwrite("StitchedOutput.png", stitched_img)
            cv.imshow("Stitched Image", stitched_img)
            cv.waitKey(0)

        ################# POST IMAGE STITCHING #############
        # convert the images to threshold
        stitched_img = cv.copyMakeBorder(stitched_img, 10, 10, 10, 10, cv.BORDER_CONSTANT, (0,0,0))

        gray = cv.cvtColor(stitched_img, cv.COLOR_BGR2GRAY)
        thresh_img = cv.threshold(gray, 0, 255, cv.THRESH_BINARY)[1]


        cv.imshow("Threshold Image", thresh_img)
        cv.waitKey(0)

        # 

    


