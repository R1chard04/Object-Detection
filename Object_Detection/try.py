import cv2 as cv
import numpy as np
import os

refDir = "Object_Detection\Photos\Refs"
colDir = "Object_Detection\Photos\Col"
maskDir = "Object_Detection\Photos\Masks"

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

def createMask(std, col):
    ref = cv.cvtColor(std, cv.COLOR_BGR2GRAY)
    ref = np.zeros(ref.shape[:2], dtype = np.uint8)

    #Image subtraction
    diff = cv.subtract(std, col)

    #Denoising
    denoise = np.float32(diff) / 255.0
    kernel_size = 3
    blur = cv.GaussianBlur(denoise, (kernel_size, kernel_size),0)
    denoise = np.uint8(blur * 255)

    #Convert to gray
    gray = cv.cvtColor(denoise, cv.COLOR_BGR2GRAY)

    #Convert to binary
    kernel = np.ones((5, 5), np.uint8)
    opening = cv.morphologyEx(gray, cv.MORPH_OPEN, kernel)
    __, binary = cv.threshold(opening, 0, 255, cv.THRESH_TRIANGLE)

    #Finding Contours
    contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv.contourArea, reverse=True)
    largest_contour = contours[0]
    cv.drawContours(ref, largest_contour, -1, (255, 255, 255), 7)

    #Reparing contoured
    repair = fillByLine(ref, "V")
    repair = fillByLine(repair, "H")
    repair = floodFill(repair)

    mask = repair
    return mask


for image in os.listdir(refDir):

    path = os.path.join(refDir,image)
    std = cv.imread(path)
    path = os.path.join(colDir,image)
    col = cv.imread(path)

    maskPath = os.path.join(maskDir, image)

    mask = createMask(std, col)
    cv.imwrite('Object_Detection\Photos\Masks\leftNew.jpg', mask)



    frame = cv.pyrDown(mask)
    frame = cv.pyrDown(frame)
    
    cv.imshow("test", frame)
    print(mask.shape)
    cv.waitKey(0)
# mask = cv.imread('Object_Detection\Photos\Masks\left.jpg')

# mask[mask!=0] = 255
# print(mask.shape)

# # mask = cv.cvtColor(mask, cv.COLOR_BAYER_BG2BGR)
# # print(mask.shape)

# cv.imwrite('Object_Detection\Photos\Masks\leftNew.jpg', mask)

# frame = cv.pyrDown(mask)
# frame = cv.pyrDown(frame)

# cv.imshow("test", frame)
# print(mask.shape)
# cv.waitKey(0)