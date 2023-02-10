import cv2 as cv
import os

img = cv.imread('STD.jpg')
height = 2160
width = 3840

slicedTestImgs = ["imagepath"]*4

# print(slicedTestImgs)
cv.imwrite('top.jpg', img[:height//2, :width]) 
cv.imwrite('left.jpg', img[:height, :width//2]) 
cv.imwrite('bottom.jpg', img[height//2:, :width]) 
cv.imwrite('right.jpg', img[:height, :width//2]) 

testImg = cv.pyrDown(img)
testImg = cv.pyrDown(img)
img = cv.pyrDown(img)

# Display the image
cv.imshow("Square on Image", img)

cv.waitKey(0)
cv.destroyAllWindows()

