import cv2
import numpy as np

# Load image
img1 = cv2.imread('Image-Masking\mask_pics\\STANDARD.jpg')
img2 = cv2.imread('Image-Masking\mask_pics\\NONE.jpg')

# Create a mask with the same shape as the images
mask = np.zeros(img2.shape[:2], dtype= np.uint8)
TOL = 5
# Iterate over each pixel and set the value of the mask to 255 if the pixel value in img2 is greater than or equal to the pixel value in img1
for i in range(img1.shape[0]):
    for j in range(img1.shape[1]):
        if img1[i, j, 0] >= img2[i, j, 0]:
            # print("true")
            mask[i, j] = 255
            # print("success")


img1 = cv2.resize(img1, (0,0), fx = 0.5, fy = 0.5)
img2 = cv2.resize(img2, (0,0), fx = 0.5, fy = 0.5)
mask = cv2.resize(mask, (0,0), fx = 0.5, fy = 0.5)

kernel = np.ones((5,5), np.uint8)  # note this is a horizontal kernel
mask = cv2.dilate(mask, kernel, iterations=1)
mask = cv2.erode(mask, kernel, iterations=5)

# blue = np.array([255, 0, 0], dtype=np.uint8)
# # Replace all pixels that match the lue color with white (255, 255, 255)
# mask[np.all(mask == blue, axis=-1)] = [255, 255, 255]

print ("here")

# # Use the mask to perform the subtraction
img2 = cv2.bitwise_and(img2,img2,mask=mask)

result = cv2.subtract(img1, img2)
result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
result[result >= 200] = 255

cv2.imshow("mask", cv2.resize(mask, (0,0), fx = 0.5, fy = 0.5))
cv2.imshow("result", cv2.resize(result, (0,0), fx = 0.5, fy = 0.5))
cv2.waitKey(0)
cv2.destroyAllWindows()