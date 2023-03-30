import cv2 as cv
import numpy as np

def mse(img1, img2, pixels):
    # height, width = img1.shape
    diffImg = cv.absdiff(img1, img2)
    err = np.sum(diffImg**2)
    ans = err/ float(pixels)
    #Closer to 0 is better
    return ans


img1 = cv.imread("backend\Photos\Col\station100\left.jpg")
img2 = cv.imread("backend\Photos\Refs\station100\left.jpg")
mask = cv.imread("backend\Photos\Masks\station100\left.jpg",0)

img1 = cv.bitwise_and(img1, img1, mask = mask)
img2 = cv.bitwise_and(img2, img2, mask = mask)

# img1 = cv.cvtColor(img1, cv.COLOR_BGR2HSV)
# img2 = cv.cvtColor(img2, cv.COLOR_BGR2HSV)

# h1, s1, v1 = cv.split(img1)
# h2, s2, v2 = cv.split(img2)

pixels = img1.size
print(pixels)

ans = mse(img1,img2,pixels)
print(ans)

cv.imshow("h1", cv.pyrDown(img1))
cv.imshow("h2", cv.pyrDown(img2))
cv.waitKey(0)