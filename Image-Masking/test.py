import cv2 as cv
import numpy as np

partImg = cv.imread('Image-Masking\mask_pics\STANDARD.jpg')
noPartImg = cv.imread('Image-Masking\mask_pics/NONE.jpg')


# Convert to grayscale

normalizedPartImg = np.zeros((800, 800))
normalizedPartImg = cv.normalize(partImg,  normalizedPartImg, 0, 255, cv.NORM_MINMAX)

normalizedNoPartImg = np.zeros((800, 800))
normalizedNoPartImg = cv.normalize(noPartImg,  normalizedNoPartImg, 0, 255, cv.NORM_MINMAX)

partImg = cv.cvtColor(partImg, cv.COLOR_BGR2GRAY)
noPartImg = cv.cvtColor(noPartImg, cv.COLOR_BGR2GRAY)

# # Remove glare from images
# clahefilter = cv.createCLAHE(clipLimit=2.0, tileGridSize=(16,16))
# reference_gray = clahefilter.apply(partImg)
# target_gray = clahefilter.apply(noPartImg)

# Perform background subtraction
diff = cv.subtract(partImg, noPartImg)

# Apply threshold to remove low intensity differences
_, mask = cv.threshold(diff, 100, 255, cv.THRESH_BINARY)

# Apply morphological operations to fill in small holes
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
maskPart = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

# Find contours in the mask
contours, _ = cv.findContours(maskPart, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# Draw contours on the target image
contour_image = np.zeros(partImg.shape, dtype=np.uint8)
cv.drawContours(contour_image, contours, -1, (255, 255, 255), 2)

# Save the result
cv.imwrite("contour_image.jpg", contour_image)


# #Filling gaps
# thresh, imgThresh = cv.threshold(maskPart,200,255,cv.THRESH_BINARY)
# fillMask = imgThresh.copy()
# height, width = imgThresh.shape[:2]
# mask = np.zeros((height+2,width+2),np.uint8)
# cv.floodFill(fillMask, mask,(0,0),(255,255,255))

# fillMask = cv.bitwise_not(fillMask)

# #Filling gaps
# subtract = maskPart+fillMask

#Resize and show
img = cv.resize(mask, (0,0), fx = 0.25, fy = 0.25)
cv.imwrite("Image-Masking\mask_pics\MASK.jpg",mask)
cv.imshow("MASK",img)
cv.waitKey(0)