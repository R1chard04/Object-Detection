import numpy as np
import cv2
 
std = cv2.imread('AutoMask\mask_pics\STANDARD.jpg')
blnk = cv2.imread('AutoMask\mask_pics\\NONE.jpg') 
 
# Convert to graycsale
std_gray = cv2.cvtColor(std, cv2.COLOR_BGR2GRAY)
blnk_gray = cv2.cvtColor(blnk, cv2.COLOR_BGR2GRAY)
# Blur the image for better edge detection
std_blur = cv2.GaussianBlur(std_gray, (3,3), 0) 
blnk_blur = cv2.GaussianBlur(blnk_gray, (3,3), 0) 
 
# Sobel Edge Detection
std_Sobelx = cv2.Sobel(src=std_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5) # Sobel Edge Detection on the X axis
std_Sobely = cv2.Sobel(src=std_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5) # Sobel Edge Detection on the Y axis
std_Sobelxy = cv2.Sobel(src=std_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5) # Combined X and Y Sobel Edge Detection

blnk_Sobelx = cv2.Sobel(src=blnk_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5) # Sobel Edge Detection on the X axis
blnk_Sobely = cv2.Sobel(src=blnk_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5) # Sobel Edge Detection on the Y axis
blnk_Sobelxy = cv2.Sobel(src=blnk_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5) # Combined X and Y Sobel Edge Detection
# Display Sobel Edge Detection Images
# cv2.imshow('Sobel X', cv2.resize(sobelx, (0,0), fx = 0.2, fy = 0.2))
# cv2.waitKey(0)
# cv2.imshow('Sobel Y', cv2.resize(sobely, (0,0), fx = 0.2, fy = 0.2))
# cv2.waitKey(0)
# cv2.imshow('Sobel X Y using Sobel() function', cv2.resize(sobelxy, (0,0), fx = 0.2, fy = 0.2))
# cv2.waitKey(0)

result = cv2.subtract(std_Sobelxy, blnk_Sobelxy)
cv2.imshow("result", cv2.resize(result, (0,0), fx = 0.2, fy = 0.2))
 
# # Canny Edge Detection
std_edges = cv2.Canny(image=std, threshold1=0, threshold2=100) # Canny Edge Detection
blnk_edges = cv2.Canny(image=blnk, threshold1=0, threshold2=100) # Canny Edge Detection

result = cv2.subtract(std_edges, blnk_edges)
# # Display Canny Edge Detection Image
cv2.imshow('Canny Edge Detection', cv2.resize(result, (0,0), fx = 0.2, fy = 0.2))
cv2.waitKey(0)
 
cv2.destroyAllWindows()