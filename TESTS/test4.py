# this is a test creating mask by adding 2 subtractions together
import cv2 as cv
import numpy as np
import os

#------------------------------------------------------------------------------------------------#

#FUNCTIONS:
def orange2Black(image):
  ORANGE_MIN = np.array([5, 50, 50], dtype = "uint8")
  ORANGE_MAX = np.array([20, 255, 255], dtype = "uint8")

  hsv_img = cv.cvtColor(image, cv.COLOR_BGR2HSV)

  mask = cv.inRange(hsv_img, ORANGE_MIN, ORANGE_MAX)
  
  # Replace the orange pixels with black
  image[np.where(mask == 255)] = [0, 0, 0]

  cv.imwrite("image.jpg", image)
  # Save the output image
  return image

def fillByLine(img, direction):
  if direction == "H":
    for row in range(img.shape[0]):
      start, stop = 0, 0
      for col in range(img.shape[1]):
        if img[row,col] != 0 and start == 0: 
          start = col, row
        if img[row ,col] != 0: 
          stop = col, row
      
        if start != 0 and np.abs(start[0]-stop[0]) <= 100: #MAX AMOUNT TO FILL
            cv.line(img, start, stop, 255, 1)
            start=stop
        elif start!= 0 and np.abs(start[0]-stop[0]) > 100:
          start=stop

  if direction == "V":
    for col in range(img.shape[1]):
      start, stop = 0, 0
      for row in range(img.shape[0]):
        if img[row,col] != 0 and start == 0: 
          start = col, row
        if img[row ,col] != 0: 
          stop = col, row
      
        if start != 0 and np.abs(start[1]-stop[1]) <= 100: #MAX AMOUNT TO FILL
            cv.line(img, start, stop, 255, 1)
            start=stop
        elif start!= 0 and np.abs(start[1]-stop[1]) > 100:
          start=stop
    
  return img 

def floodFill(imgThresh):
  fillMask = imgThresh.copy()
  height, width = imgThresh.shape[:2]
  mask = np.zeros((height+2,width+2),np.uint8)
  cv.floodFill(fillMask, mask,(0,0),(255,255,255))
  fillMask = cv.bitwise_not(fillMask)

  return cv.add(imgThresh, fillMask)

#------------------------------------------------------------------------------------------------#

noneDir = 'TESTS/NONE/'
stdDir = 'TESTS/STD/'
stdPath = ['STANDARD2.jpg','STANDARD3.jpg','STANDARD4.jpg']
nonePath = ['NONE2.jpg','NONE3.jpg','NONE4.jpg']
noneArray = []
stdArray = []

ref = cv.imread('TESTS/STD/STANDARD1.jpg', cv.IMREAD_GRAYSCALE)
__, ref = cv.threshold(ref, 0, 255, cv.THRESH_BINARY)
ref[ref != 0] = 0
# cv.imshow("ref", ref)

for i in range(len(stdPath)):
  # image_path = os.path.join(stdDir, stdPath[i])
  image = cv.imread(stdDir + stdPath[i])
  stdArray.append(image)
  print(stdDir + stdPath[i])
  
for i in range(len(nonePath)):
  # Skip any files that are not images
  # photos_path = os.path.join(noneDir, nonePath[i])
  photos = cv.imread(noneDir + nonePath[i])
  noneArray.append(photos)
  print(noneDir + nonePath[i])

for i in range(len(stdArray)):
  std = orange2Black(stdArray[i])
  none = orange2Black(noneArray[i])

  std_gray = cv.cvtColor(std, cv.COLOR_BGR2GRAY)
  none_gray = cv.cvtColor(none, cv.COLOR_BGR2GRAY)

  subtract1 = cv.subtract(std_gray, none_gray)
  subtract2 = cv.subtract(none_gray, std_gray)

  addImg = cv.add(subtract1, subtract2)
  cv.imshow('t', addImg)
  cv.waitKey(0)

  _, thresholdImg = cv.threshold(addImg, 50, 255, cv.THRESH_BINARY)

  denoiseImg = cv.GaussianBlur(addImg, (5,5), 7, 21)
  denoiseImg = cv.fastNlMeansDenoising(denoiseImg, 15, 21)
  kernel = np.ones((3, 3), np.uint8)
  opening = cv.morphologyEx(denoiseImg, cv.MORPH_OPEN, kernel)
  __, binary = cv.threshold(opening, 10, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)

  contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
  contours = sorted(contours, key=cv.contourArea, reverse=True)
  largest_contour = contours[0]
  img_contour = np.zeros((ref.shape[0], ref.shape[1], 3), np.uint8)
  cv.drawContours(ref, [largest_contour], -1, (255, 255, 255), 1)

  print("dodo")

ref[ref != 0] = 255

#Corrections
kernel = np.ones((3,3), np.uint8)

ref = fillByLine(ref, "H")
ref = floodFill(ref)
ref = fillByLine(ref, "V")

img = cv.imread('TESTS/STD/STANDARD4.jpg')
result = cv.bitwise_and(img, img, mask = ref)

cv.imwrite("hi.jpg", result)
print("KENT WAS WRONG")




#LEO WROTE THIS CODE





