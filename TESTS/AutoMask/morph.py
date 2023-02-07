import cv2
import numpy as np


array = ['AutoMask\mask_pics\\STANDARD4.jpg', 'AutoMask\mask_pics\\NONE4.jpg']
imgArray = []
# Load the image
for i in range(len(array)):
    img = cv2.imread(array[i])
    cv2.imshow("hi", img)
    cv2.waitKey(0)

    # Preprocess the image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)

    # Calculate the gradient magnitude
    sobelx = cv2.Sobel(blur, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(blur, cv2.CV_64F, 0, 1, ksize=3)
    magnitude = np.sqrt(sobelx ** 2 + sobely ** 2)

    # Define the initial contour
    magnitude = cv2.convertScaleAbs(magnitude)
    threshold = cv2.threshold(magnitude, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    initial_contour = threshold[1]

    # Define the morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    closing = cv2.morphologyEx(initial_contour, cv2.MORPH_CLOSE, kernel)
    dilation = cv2.dilate(closing, kernel, iterations=3)

    # Repeat the morphological operations and gradient vector flow until the contour converges
    while True:
        # Apply the morphological operations
        closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
        dilation = cv2.dilate(closing, kernel, iterations=3)

        # Calculate the gradient vector flow
        # ...
        break

        # Check if the contour has converged
        # ...
    imgArray.append(dilation)

# Display the final segmentation result

result = cv2.subtract(imgArray[0],imgArray[1])
cv2.imshow('Result', cv2.resize(result,(0,0), fx = 0.2, fy = 0.2))
cv2.waitKey(0)
cv2.destroyAllWindows()