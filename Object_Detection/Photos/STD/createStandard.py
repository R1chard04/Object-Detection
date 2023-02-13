import cv2 as cv

img = cv.imread('Photos\STD\\topPart.jpg')

print(img.shape)

img = cv.imread('Photos\MASKS\\topPartM.jpg')
print(img.shape)

# height = img.shape[0]
# width = img.shape[1]
# cv.imwrite('Photos\STD\\topPart.jpg', img[:height//2, :width])
# cv.imwrite('Photos\STD\leftPart.jpg', img[:height, :width//2])
# cv.imwrite('Photos\STD\\bottomPart.jpg', img[height//2:, :width])
# cv.imwrite('Photos\STD\\rightPart.jpg', img[:height, width//2:])



# mask = cv.imread('Photos\MASKS\\topPartM.jpg')

# # cv.imwrite('Photos\MASKS\\rightPartM.jpg', mask[1:, :])

# print(img.shape)
# print(mask.shape)

# 1.875 tb
# 1.055 lr

#14 23 12 34