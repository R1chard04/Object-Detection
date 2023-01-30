import cv2 as cv
import numpy as np

partImg = cv.imread('Image-Masking\STANDARD1.jpg') # ?? img
noPartImg = cv.imread('Image-Masking/NONE.jpg')        # ?? no
#Subtracting the two images to find the part area
subtractOG = cv.subtract(cv.cvtColor(partImg,cv.COLOR_BGR2GRAY),cv.cvtColor(noPartImg,cv.COLOR_BGR2GRAY))
# subtractOG = cv.cvtColor(partImg,cv.COLOR_BGR2GRAY) - cv.cvtColor(noPartImg,cv.COLOR_BGR2GRAY)

#Applying filters on image
alpha = 3 # Contrast control (rec 1-3)
beta = -300 # Brightness control (rec -300 <-> 300)
subtractOG = cv.convertScaleAbs(subtractOG, alpha=alpha, beta=beta)
subtractOG = cv.bitwise_not(subtractOG) #inverts

subtractOG = cv.fastNlMeansDenoising(subtractOG, None, 40, 7, 15)
subtractOG = cv.fastNlMeansDenoising(subtractOG, None, 40, 7, 15)

# #Black and white configuration

subtractOG[subtractOG < 10] = 0
subtractOG[subtractOG != 0] = 255

kernel = np.ones((230,230), np.uint8)  # note this is a horizontal kernel
subtractOG = cv.dilate(subtractOG, kernel, iterations=1)


#Filling gaps
thresh, imgThresh = cv.threshold(subtractOG,200,255,cv.THRESH_BINARY)
fillMask = imgThresh.copy()
height, width = imgThresh.shape[:2]
mask = np.zeros((height+2,width+2),np.uint8)
cv.floodFill(fillMask, mask,(0,0),(255,255,255))

fillMask = cv.bitwise_not(fillMask)



#Filling gaps
subtractOG = subtractOG+fillMask
subtractOG = cv.erode(subtractOG, kernel, iterations=1) 
img = cv.resize(subtractOG, (0,0), fx = 0.2, fy = 0.2)
cv.imwrite("Image-Masking\mask_pics\MASK.jpg",subtractOG)
cv.imshow("MASK",img)
cv.waitKey(0)