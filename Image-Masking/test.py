# import cv2 as cv
# import numpy as np


# BGR = cv.subtract(partImg,noPartImg)
# BGR = cv.GaussianBlur(BGR,(3,3),0)
# BGR = cv.cvtColor(BGR, cv.COLOR_BGR2GRAY)


# gray = cv.cvtColor(BGR, cv.COLOR_BGR2GRAY)
# thresh = cv.threshold(gray, 130, 255, cv.THRESH_BINARY)[1]
# thresh = cv.fastNlMeansDenoising(thresh, None, 40, 7, 15)
# HSV = cv.cvtColor(thresh,cv.COLOR_BGR2HSV)

# add = cv.add(gray, thresh)
# add = cv.medianBlur(add, 15, 15)
# add = cv.threshold(add, 254, 255, cv.THRESH_BINARY)[1]


# # detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
# contours, hierarchy = cv.findContours(image = add, mode=cv.RETR_TREE, method=cv.CHAIN_APPROX_NONE)


# # draw contours on the original image
# image_copy = partImg.copy()
# cv.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=1, lineType=cv.LINE_AA)

# #Applying filters on image
# alpha = 3 # Contrast control (rec 1-3)
# beta = -300 # Brightness control (rec -300 <-> 300)
# subtract = cv.convertScaleAbs(subtract, alpha=alpha, beta=beta)
# subtract = cv.bitwise_not(subtract) #inverts

#
# subtract = cv.fastNlMeansDenoising(subtract, None, 40, 7, 15)

# # #Black and white configuration


# #Filling gaps
# thresh, imgThresh = cv.threshold(subtract,200,255,cv.THRESH_BINARY)
# fillMask = imgThresh.copy()
# height, width = imgThresh.shape[:2]
# mask = np.zeros((height+2,width+2),np.uint8)
# cv.floodFill(fillMask, mask,(0,0),(255,255,255))

# fillMask = cv.bitwise_not(fillMask)

# #Filling gaps
# subtract = subtract+fillMask

from skimage.metrics import structural_similarity
import cv2
import numpy as np

# Load images
before = cv2.imread('Image-Masking\\mask_pics\\STANDARD.jpg')

after = cv2.imread('Image-Masking\\mask_pics\\NONE.jpg')

# Convert images to grayscale
before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
after_gray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)

# Compute SSIM between the two images
(score, diff) = structural_similarity(before_gray, after_gray, full=True)
print("Image Similarity: {:.4f}%".format(score * 100))

# The diff image contains the actual image differences between the two images
# and is represented as a floating point data type in the range [0,1]
# so we must convert the array to 8-bit unsigned integers in the range
# [0,255] before we can use it with OpenCV
diff = (diff * 255).astype("uint8")
diff_box = cv2.merge([diff, diff, diff])

# Threshold the difference image, followed by finding contours to
# obtain the regions of the two input images that differ
thresh = cv2.threshold(
    diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]

mask = np.zeros(before.shape, dtype='uint8')
filled_after = after.copy()

for c in contours:
    area = cv2.contourArea(c)


# Resize and show
img = cv2.resize(thresh, (0, 0), fx=0.35, fy=0.35)
cv2.imwrite("Image-Masking\mask_pics\MASK.jpg", thresh)
cv2.imshow("MASK", img)
cv2.waitKey(0)
