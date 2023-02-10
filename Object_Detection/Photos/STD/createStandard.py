import cv2 as cv

img = cv.imread('Photos\STD\STD.jpg')
height = img.shape[0]
width = img.shape[1]

cv.imwrite('Photos\STD\\topPart.jpg', img[:height//2, :width])
cv.imwrite('Photos\STD\leftPart.jpg', img[:height, :width//2])
cv.imwrite('Photos\STD\\bottomPart.jpg', img[height//2:, :width])
cv.imwrite('Photos\STD\\rightPart.jpg', img[:height, width//2:])

img = cv.imread('Photos\STD\\leftPart.jpg')
mask = cv.imread('Photos\MASKS\leftPartM.jpg')

print(img.shape)
print(mask.shape)