#imageStitchingClasses.py#

# import libraries
import numpy as np
import cv2 as cv
import glob
import imutils

class imageStitching:
    def __init__(self, image_paths) -> None:
        self.image_paths = image_paths

    def stitchImgs(self) -> any:
        # open the images folder
        pathImgs = glob.glob(self.image_paths)
        images = []

        # a for loop to loop through the images
        for image in pathImgs:
            img = cv.imread(image)
            (self.images).append(img)
            cv.imshow("Image", img)
            cv.waitKey(0)

        # stitch an images
        imageStitcher = cv.Stitcher_create()

        # if not able to stitch images
        error, stitched_img = imageStitcher.stitch(images)

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

            # Set the contours
            contours = imutils.grab_contours(contours)
            areaOI = max(contours, key=cv.contourArea)

            # Set up the mask
            mask = np.zeros(thresh_img.shape, dtype="uint8")
            x,y,w,h = cv.boundingRect(areaOI)
            cv.rectangle(mask,(x,y), (x+w,y+h), 255, -1)

            minRectangle = mask.copy()
            sub = mask.copy()

            # A while loop 
            while cv.countNonZero(sub) > 0:
                minRectangle = cv.erode(minRectangle, None)
                sub = cv.subtract(minRectangle, thresh_img)

            contours = cv.findContours(minRectangle.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

            contours = imutils.grab_contours(contours)
            areaOI = max(contours, key=cv.contourArea)

            cv.imshow("minRectangle Image", minRectangle)
            cv.waitKey(0)

            x,y,w,h = cv.boundingRect(areaOI)

            stitched_img = stitched_img[y:y + h, x:x + w]

            cv.imwrite("stitchedOutputProcessed.png", stitched_img)
            cv.imshow("Stitched Image Processed", stitched_img)

            cv.waitKey(0)

        else:
            print("Images could not be stitched!")
            print("Likely not enough keypoints being detected!")


