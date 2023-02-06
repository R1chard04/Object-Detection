# this is a test creating mask by adding 2 subtractions together
import cv2 as cv
import numpy as np

image = cv.imread("TESTS/STD/STANDARD3.jpg") # part
image1 = cv.imread("TESTS/NONE/NONE3.jpg") # no part

gray1 = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
gray2 = cv.cvtColor(image1, cv.COLOR_BGR2GRAY)

subtract1 = cv.absdiff(gray1, gray2)
subtract2 = cv.subtract(gray2, gray1)

cv.imshow("Subtract 1", subtract1)
cv.imshow("Subtract 2", subtract2)

addImg = cv.add(subtract1, subtract2)
_, thresholdImg = cv.threshold(addImg, 30, 255, cv.THRESH_BINARY)


denoiseImg = cv.fastNlMeansDenoising(addImg, 15, 21)
denoiseImg1 = cv.fastNlMeansDenoising(thresholdImg, 15, 21)

kernel = np.ones((3, 3), np.uint8)

opening = cv.morphologyEx(denoiseImg, cv.MORPH_OPEN, kernel)
__, binary = cv.threshold(opening, 10, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)




# Find the contours of the image
contours, hierarchy = cv.findContours(denoiseImg1, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv.contourArea, reverse=True)
largest_contour = contours[0]
img_contour = np.zeros((binary.shape[0], binary.shape[1], 3), np.uint8)
cv.drawContours(img_contour, [largest_contour], -1, (255, 255, 255), 3)

cv.imshow("Image contour", binary)

cv.imshow("Result", img_contour)
cv.waitKey(0)



cv.waitKey(0)
cv.destroyAllWindows()
