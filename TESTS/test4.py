# this is a test creating mask by adding 2 subtractions together
import cv2 as cv
import numpy as np
import os

noneDir = 'TESTS/NONE/'
stdDir = 'TESTS/STD/'
stdPath = ['STANDARD1.jpg','STANDARD2.jpg','STANDARD3.jpg','STANDARD4.jpg','STANDARD5.jpg']
nonePath = ['NONE1.jpg','NONE2.jpg','NONE3.jpg','NONE4.jpg','NONE5.jpg']
noneArray = []
stdArray = []

ref = cv.imread('TESTS/STD/STANDARD1.jpg', cv.IMREAD_GRAYSCALE)
__, ref = cv.threshold(ref, 0, 255, cv.THRESH_BINARY)
ref[ref != 0] = 0
cv.imshow("ref", ref)

for i in range(5):
  # image_path = os.path.join(stdDir, stdPath[i])
  image = cv.imread(stdDir + stdPath[i])
  stdArray.append(image)
  print(stdDir + stdPath[i])
  
for i in range(5):
  # Skip any files that are not images
  # photos_path = os.path.join(noneDir, nonePath[i])
  photos = cv.imread(noneDir + nonePath[i])
  noneArray.append(photos)
  # print(photos_path)

for i in range(len(stdArray)):
  std = stdArray[i]
  none = noneArray[i]

  # cv.imshow("standard{i}", std)
  # cv.imshow("none{i}", none)
  # cv.waitKey(0)

  std_gray = cv.cvtColor(std, cv.COLOR_BGR2GRAY)
  none_gray = cv.cvtColor(none, cv.COLOR_BGR2GRAY)

  subtract1 = cv.subtract(std_gray, none_gray)
  subtract2 = cv.subtract(none_gray, std_gray)

  addImg = cv.add(subtract1, subtract2)
  _, thresholdImg = cv.threshold(addImg, 50, 255, cv.THRESH_BINARY)

  denoiseImg = cv.GaussianBlur(addImg, (3,3), 7, 21)
  denoiseImg = cv.fastNlMeansDenoising(denoiseImg, 15, 21)
  kernel = np.ones((3, 3), np.uint8)
  opening = cv.morphologyEx(denoiseImg, cv.MORPH_OPEN, kernel)
  __, binary = cv.threshold(opening, 10, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)

  ref = cv.add(ref, binary)


  # cv.imshow("binary{i}.jpg", binary)
  
  # cv.waitKey(0)


contours, hierarchy = cv.findContours(ref, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv.contourArea, reverse=True)
largest_contour = contours[0]
img_contour = np.zeros((ref.shape[0], ref.shape[1], 3), np.uint8)
cv.drawContours(img_contour, [largest_contour], -1, (255, 255, 255), 1)

cv.imwrite("hi.jpg", img_contour)
print("KENT WAS WRONG")




#LEO WROTE THIS CODE


