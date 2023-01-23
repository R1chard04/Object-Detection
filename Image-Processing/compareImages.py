import cv2
import numpy as np

# load the input images
off1 = cv2.imread('Image-Processing\photos\Small\Original\OFF1.jpg')
off2 = cv2.imread('Image-Processing\photos\Small\Original\OFF6.jpg')
standard = cv2.imread('Image-Processing\photos\Small\Original\OG1.jpg')

# convert the images to grayscale
off1 = cv2.cvtColor(off1, cv2.COLOR_BGR2GRAY)
off2 = cv2.cvtColor(off2, cv2.COLOR_BGR2GRAY)
standard = cv2.cvtColor(standard, cv2.COLOR_BGR2GRAY)

def mse(img1, img2):
    h, w = img1.shape
    diff = cv2.subtract(img1, img2)
    err = np.sum(diff**2)
    ans = err/(float(h*w))
    return ans, diff

#Masking
maskImg = cv2.imread('Image-Processing\photos\Small\Mask.jpg')
grayMask = cv2.cvtColor(maskImg, cv2.COLOR_BGR2GRAY)
(thresh, maskBW) = cv2.threshold(grayMask, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
thresh = 127
binaryMask = cv2.threshold(grayMask, thresh, 255, cv2.THRESH_BINARY)[1]
#binaryMask = cv2.resize(diff1, (0,0), fx = 0.3, fy = 0.3)   
off1M = cv2.bitwise_and(off1,off1, mask= binaryMask)
off2M = cv2.bitwise_and(off2,off2, mask= binaryMask)
standardM = cv2.bitwise_and(standard,standard, mask= binaryMask)

error, diff1 = mse(standardM, off1M)
error2, diff2 = mse(standardM, standardM)

print("Error between the two images1: ", error)
print("Error between the two images2: ", error2)

diff1 = cv2.resize(diff1, (0,0), fx = 0.3, fy = 0.3)
diff = cv2.resize(diff2, (0,0), fx = 0.3, fy = 0.3)

cv2.imshow("diff1", diff1)
cv2.imshow("diff2", diff2)
cv2.waitKey(0)
cv2.destroyAllWindows()
