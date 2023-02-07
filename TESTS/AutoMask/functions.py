import cv2 as cv
import numpy as np

def denoiseWhite(img):
    for i in range(3):
        img = cv.GaussianBlur(img, (3,3), 15, 15)
        img = cv.add(img, img)
        img = cv.fastNlMeansDenoising(img, None, 30, 7, 15)

    img[img != 255] = 0

    return img

def floodFill(img):
    __, imgThresh = cv.threshold(img,50,255,cv.THRESH_BINARY)
    fillMask = imgThresh.copy()
    height, width = imgThresh.shape[:2]
    mask = np.zeros((height+2,width+2),np.uint8)
    cv.floodFill(fillMask, mask,(0,0),(255,255,255))
    fillMask = cv.bitwise_not(fillMask)

    return cv.add(img, fillMask)

# final = feed+fillMask

def fillHoles(img):
    kernel = np.ones((1,5), np.uint8)  # note this is a horizontal kernel
    img = cv.dilate(img, kernel, iterations=5)
    kernel = np.ones((5,1), np.uint8)  # note this is a horizontal kernel
    img = cv.dilate(img, kernel, iterations=5)
    

    img = floodFill(img)


    kernel = np.ones((1,5), np.uint8)
    img = cv.erode(img, kernel, iterations=5)
    kernel = np.ones((5,1), np.uint8)
    img = cv.erode(img, kernel, iterations=5)

    return img

def isolate(img):
    # Find contours in the binary image
    contours, _ = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # Sort contours by area and keep only the largest contour
    contours = sorted(contours, key=cv.contourArea, reverse=True)
    largest_contour = contours[0]
    # Draw the largest contour on an empty image to create a binary mask
    mask = np.zeros_like(img)
    cv.drawContours(mask, [largest_contour], -1, 255, -1)

    return mask

def smoothen(img):
    
    # Create a structuring element for dilation and erosion
    # Perform morphological operations
    kernel = np.ones((5,5),np.uint8)
    dilation = cv.dilate(img,kernel,iterations = 1)
    erosion = cv.erode(dilation,kernel,iterations = 1)

    # Gaussian Blurring
    img = cv.GaussianBlur(erosion, (15,15), 0)
    
    return img