import cv2

# Load the RGB image
img = cv2.imread("testPics/QuadEmpty4.jpg")

# Convert the image to greyscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Save the greyscale image
cv2.imwrite("testPics/QuadEmpty4Grey.jpg", gray)