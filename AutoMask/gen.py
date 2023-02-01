import cv2 as cv
import numpy as np
from functions import denoiseWhite, floodFill, isolate, smoothen



#-------------------------------------------------------------------------------------#
#Import
partImg = cv.imread('Image-Masking\mask_pics\STANDARD.jpg')
noPartImg = cv.imread('Image-Masking\mask_pics\\NONE.jpg')

#Regular subtraction
subtract1 = cv.subtract(partImg, noPartImg)

# Modified subtraction 
# Mask of the areas where noPartImg pixels < partImg
mask = np.zeros(noPartImg.shape[:2], dtype= np.uint8)
for i in range(partImg.shape[0]):
    for j in range(partImg.shape[1]):
        if partImg[i, j, 0] >= noPartImg[i, j, 0]:
            mask[i, j] = 255



subtract1 = denoiseWhite(cv.cvtColor(subtract1, cv.COLOR_BGR2GRAY))

#Subtracting the two images to find the part area
noPartImgMasked = cv.bitwise_and(noPartImg,noPartImg,mask=mask)
subtract2 = cv.subtract(partImg, noPartImgMasked)
subtract2 = denoiseWhite(cv.cvtColor(subtract2,cv.COLOR_BGR2GRAY))



# #Turning to binary image
__, subtract2Mask = cv.threshold(subtract2, 10, 255, cv.THRESH_BINARY)


#First image --dilation--> Canvas
kernel = np.ones((10,10), np.uint8)  
subtract1Dilate = cv.dilate(subtract1, kernel, iterations=10)

#Masking the dilate to remove unwanted region then readding to its original to add light obscured region
maskSubtract1Dilate = cv.bitwise_and(subtract1Dilate, subtract1Dilate, mask = subtract2Mask)

added = smoothen(cv.add(subtract1, maskSubtract1Dilate))
added = cv.bilateralFilter(added, 15, 300, 300)
# result = cv.bitwise_and(added,added,mask=subtract2)
result = smoothen(floodFill(isolate(added)))


cv.imwrite("AutoMask\progress\mask.jpg", mask)
cv.imwrite("AutoMask\progress\subtract1.jpg", subtract1)
cv.imwrite("AutoMask\progress\subtract2.jpg", subtract2)
cv.imwrite("AutoMask\progress\subtract2Mask.jpg", subtract2Mask)
cv.imwrite("AutoMask\progress\subtract1Dilate.jpg", subtract1Dilate)
cv.imwrite("AutoMask\progress\maskSubtract1Dilate.jpg", maskSubtract1Dilate)
cv.imwrite("AutoMask\progress\\added.jpg", added)
cv.imwrite("AutoMask\progress\\result.jpg", result)
#Passing
feed = cv.bitwise_and(partImg, partImg, mask = result)



cv.imshow("ref", cv.resize(feed, (0,0), fx = 0.2, fy = 0.2))


#-------------------------------------------------------------------------------------#
# denoise = feed

#
#-------------------------------------------------------------------------------------#


cv.waitKey(0)