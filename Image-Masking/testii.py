from skimage.metrics import structural_similarity
import cv2
import numpy as np

# Load images
before = cv2.imread('mask_pics\\STANDARD.jpg')
after= cv2.imread('mask_pics\\NONE.jpg')
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
thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]

mask = np.zeros(before.shape, dtype='uint8')
filled_after = after.copy()

for c in contours:
    area = cv2.contourArea(c)
    if area > 40:
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(before, (x, y), (x + w, y + h), (36,255,12), 2)
        cv2.rectangle(after, (x, y), (x + w, y + h), (36,255,12), 2)
        cv2.rectangle(diff_box, (x, y), (x + w, y + h), (36,255,12), 2)
        cv2.drawContours(mask, [c], 0, (255,255,255), -1)
        cv2.drawContours(filled_after, [c], 0, (0,255,0), -1)

cv2.imshow('before', before)
cv2.imshow('after', after)
cv2.imshow('diff', diff)
cv2.imshow('diff_box', diff_box)
cv2.imshow('mask', mask)
cv2.imshow('filled after', filled_after)
cv2.waitKey()


# import cv2

# # load images
# image1 = cv2.imread('mask_pics\\STANDARD.jpg')
# image2= cv2.imread('mask_pics\\NONE.jpg')

# # compute difference
# difference = cv2.subtract(image1, image2)

# # color the mask red
# Conv_hsv_Gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
# ret, mask = cv2.threshold(Conv_hsv_Gray, 0, 255,cv2.THRESH_BINARY_INV |cv2.THRESH_OTSU)
# difference[mask != 255] = [0, 0, 255]

# # add the red mask to the images to make the differences obvious
# image1[mask != 255] = [0, 0, 255]
# image2[mask != 255] = [0, 0, 255]

# # store images
# cv2.imwrite('diffOverImage1.png', image1)
# cv2.imwrite('diffOverImage2.png', image1)
# cv2.imwrite('diff.png', difference)


# import cv2

# # Load images as grayscale
# image1 = cv2.imread("mask_pics\\STANDARD.jpg")
# image2 = cv2.imread("mask_pics\\NONE.jpg")


# # Calculate the per-element absolute difference between 
# # two arrays or between an array and a scalar
# diff = 255 - cv2.absdiff(image1, image2)
# diff = cv2.resize(image1, (0,0), fx = 0.2, fy = 0.2)
# cv2.imshow('diff', diff)
# cv2.waitKey()

