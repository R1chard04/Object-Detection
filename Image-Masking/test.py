import cv2 as cv
import numpy as np

def filter(img):
    #Filter
    alpha = 4 # Contrast control (rec 1-3)
    beta = -300 # Brightness control (rec -300 <-> 300)

    img = cv.convertScaleAbs(img, alpha=alpha, beta=beta)
    img = cv.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    img = cv.cvtColor(img, cv.COLOR_BGR2HSV)


    # # Define some colours for readability - these are in OpenCV **BGR** order - reverse them for PIL
    # white = [255,255,255]
    # black = [0,0,0]

    # blackMask = cv.inRange(img, np.array([0,0,0]), np.array([1,0,0]))
    
    # img = cv.bitwise_and(img,img, mask = blackMask)

    # output_img = img.copy()
    # output_img[np.where(blackMask==0)] = 0
    # cv.imshow("masked", output_img)

    # image = cv.imread('1.jpg')
    # result = image.copy()
    # image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    # lower = np.array([155,25,0])
    # upper = np.array([179,255,255])
    # mask = cv.inRange(image, lower, upper)
    # result = cv.bitwise_and(result, result, mask=mask)

    # cv.imshow('mask', mask)
    # cv.imshow('result', result)
    # cv.waitKey()

    return img

img = cv.imread('Image-Masking\STANDARD.jpg')

filterImg = filter(img)
cv.imshow('filter', filterImg)

# lap = cv.Laplacian(filterImg, cv.CV_64F)
# lap = np.uint8(np.absolute(lap))
# cv.imshow('Laplacian', lap)

# canny = cv.Canny(lap, 15, 175)
# cv.imshow('Canny', canny)

cv.waitKey(0)