import cv2 as cv
import numpy as np

#-------------------------------------------------------------------------------------#
#Import
partImg = cv.imread('Image-Masking\mask_pics\STANDARD.jpg')
noPartImg = cv.imread('Image-Masking\mask_pics\\NONE.jpg')

partImg = cv.cvtColor(partImg, cv.COLOR_BGR2GRAY)
noPartImg = cv.cvtColor(noPartImg, cv.COLOR_BGR2GRAY)

#Regular subtraction
subtract1 = cv.subtract(partImg, noPartImg)
# subtract1 = cv.cvtColor(subtract1, cv.COLOR_BGR2GRAY)

# Modified subtraction 
# Mask of the areas where noPartImg pixels < partImg
mask = np.zeros(noPartImg.shape[:2], dtype= np.uint8)
for i in range(partImg.shape[0]):
    for j in range(partImg.shape[1]):
        if partImg[i, j] >= noPartImg[i, j]:
            mask[i, j] = 255

#Subtracting the two images to find the part area
noPartImgMasked = cv.bitwise_and(noPartImg,noPartImg,mask=mask)
subtract2 = cv.subtract(partImg, noPartImgMasked)
# subtract2 = cv.cvtColor(subtract2, cv.COLOR_BGR2GRAY)
# subtract2 = cv.bitwise_not(subtract2)

# #Splitting to channels
# b1, g1, r1 = cv.split(subtract1)
# b2, g2, r2 = cv.split(subtract2)
# channelledImages = [(b1,b2),(g1,g2),(r1,r2)]

# #Processing each channel
# for i in range(len(channelledImages)):
#     print('urmom')
#     img1 = channelledImages[i][0]
#     img2 = channelledImages[i][1]

#     img1 += img1
#     img2 += img2

#     channelledImages[i] = (img1, img2)

subtract1 = subtract1+subtract1+subtract1+subtract1
cv.imshow("filtered", cv.resize(subtract1, (0,0), fx = 0.2, fy = 0.2))

  # #Turning to binary image
    # __, subtract1 = cv.threshold(subtract1, 10, 255, cv.THRESH_BINARY)
    # __, subtract2 = cv.threshold(subtract2, 10, 255, cv.THRESH_BINARY)

    # cv.imshow("filteredn", cv.resize(subtract2, (0,0), fx = 0.2, fy = 0.2))

    # #Strengthening images:
    # for i in range(3):
    #     subtract1 = cv.add(subtract1, subtract1)
    #     subtract2 = cv.add(subtract2, subtract2)

    # #Creating a mask of the second subtraction to add light bits back
    # subtract2Mask = cv.bitwise_not(subtract2) 

    # #First image --dilation--> Canvas
    # kernel = np.ones((5,5), np.uint8)  # note this is a horizontal kernel
    # subtract1Dilate = cv.dilate(subtract1, kernel, iterations=3)

    # #Masking the dilate to remove unwanted region then readding to its original to add light obscured region
    # maskSubtract1Dilate = cv.bitwise_and(subtract1Dilate, subtract1Dilate, mask = subtract2Mask)
    # result = cv.add(subtract1, maskSubtract1Dilate)

    # #Passing
    # feed = result

#-------------------------------------------------------------------------------------#
# denoise = feed

# kernel = np.ones((2,2), np.uint8) 

# for i in range(2):
#     for i in range(3):
#         denoise = cv.GaussianBlur(denoise, (5,5), 15, 15)
#         # denoise = cv.bilateralFilter(denoise, 7, 30, 30)
#         denoise = cv.add(denoise, denoise)
#         denoise = cv.fastNlMeansDenoising(denoise, None, 30, 7, 15)

#         # denoise = cv.erode(denoise, kernel, iterations=1)
#     # denoise = cv.dilate(feed, kernel, iterations=1)

#     denoise[denoise != 255] = 0

# denoise = cv.bitwise_and(partImg,partImg,mask = denoise)

# denoise = cv.bilateralFilter(denoise, 15, 100, 100)


# denoise = cv.fastNlMeansDenoising(denoise, None, 400, 7, 15)


# feed = denoise

# cv.imshow("test",cv.resize(feed, (0,0), fx = 0.2, fy = 0.2))
#-------------------------------------------------------------------------------------#


# threshold_type = cv.ADAPTIVE_THRESH_GAUSSIAN_C
# block_size = 75
# C = 15
# thresholded = cv.adaptiveThreshold(feed, 255, threshold_type, cv.THRESH_BINARY, block_size, C)
# thresholded  = cv.bitwise_not(thresholded)
# _, thresholded = cv.threshold(thresholded, 128, 255, cv.THRESH_BINARY)



# feed = thresholded

# cv.imshow("test",cv.resize(feed, (0,0), fx = 0.2, fy = 0.2))
#-------------------------------------------------------------------------------------#

# kernel = np.ones((1,10), np.uint8)  # note this is a horizontal kernel
# denoise = cv.dilate(feed, kernel, iterations=5)
# kernel = np.ones((5,5), np.uint8)
# denoise = cv.erode(denoise, kernel, iterations=4)



# feed = denoise

# # Find contours in the binary image
# contours, _ = cv.findContours(feed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
# # Sort contours by area and keep only the largest contour
# contours = sorted(contours, key=cv.contourArea, reverse=True)
# largest_contour = contours[0]
# # Draw the largest contour on an empty image to create a binary mask
# mask = np.zeros_like(thresholded)
# cv.drawContours(mask, [largest_contour], -1, 255, -1)

# feed = mask

# cv.imshow("test",cv.resize(feed, (0,0), fx = 0.2, fy = 0.2))
# #-------------------------------------------------------------------------------------#

# #Filling gaps
# thresh, imgThresh = cv.threshold(feed,50,255,cv.THRESH_BINARY)
# fillMask = imgThresh.copy()
# height, width = imgThresh.shape[:2]
# mask = np.zeros((height+2,width+2),np.uint8)
# cv.floodFill(fillMask, mask,(0,0),(255,255,255))
# fillMask = cv.bitwise_not(fillMask)

# final = feed+fillMask

# input = final
# cv.imwrite("mask_pics\MASK.jpg",final)
# # cv.imshow("MASK",cv.resize(input, (0,0), fx = 0.2, fy = 0.2))
cv.waitKey(0)