# import libraries
import cv2 as cv

# class implementation
class stitching:
    def __init__(self) -> None:
        pass

    def imageStitching(image_paths, imgs):
        # a for loop to loop through each image
        for i in range(len(image_paths)):
            # keep adding more image after reading into the list
            imgs.append(cv.imread(image_paths[i]))
            # resize each image after appending it to the list
            imgs[i] = cv.resize(imgs[i], (0,0), fx=0.4, fy=0.4)
            # show the original picture
            cv.imshow("Picture " + str(i), imgs[i])


        # using stitching function to stitch the image together
        stitchy = cv.Stitcher.create()
        dummy, output = stitchy.stitch(imgs)
        
        if dummy != cv.STITCHER_OK:
            #checking if the stitching procedure is succesful
            # .stitch() function returns a true value if stitching was done succesfully
            print("Your stitching process cannot be done properly")

        else:
            print("Your stitching process has been done successfully!")

        # final output
        cv.imshow("Final Result", output)
        cv.waitKey(0)