import cv2 as cv
import numpy as np

# Function filter orange into black image
def orange2Black(image):
    ORANGE_MIN = np.array([0, 50, 50], dtype = "uint8")
    ORANGE_MAX = np.array([30, 255, 255], dtype = "uint8")

    hsv_img = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    mask = cv.inRange(hsv_img, ORANGE_MIN, ORANGE_MAX)
    
    # Replace the orange pixels with black
    image[np.where(mask == 255)] = [0, 0, 0]

    cv.imwrite("image.jpg", image)
    # Save the output image
    return image

def repair(img):
  for row in range(img.shape[0]):
    # Find the left-most and right-most pixel in the sqare
    start, stop = 0, 0
    for col in range(img.shape[1]):
        # Find the left-most
        if img[row,col] != 0 and start == 0: start = col, row
        # Find the right-most
        if img[row,col] != 0: stop = col, row
    # If there was a pixel in that row, connect them with a line
    if start != 0:
        cv.line(img, start, stop, 255, 1)
      
  return img

def fillHoles():
  pass

def selectLargestContour():
  pass

def denoise(img):
  kernel = np.ones((3,3), np.uint8)
  img = cv.erode(img, kernel, iterations = 1)
  img = cv.dilate(img, kernel, iterations = 1)
  return img

  import cv2

def compare(img1, img2):
  part = orange2Black(img1)
  none = orange2Black(img2)

  subtractC = cv.subtract(part,none)
  subtractC = cv.fastNlMeansDenoisingColored(subtractC, subtractC, 7, 21)
  subtractC = cv.bilateralFilter(subtractC, d=9, sigmaColor=75, sigmaSpace=75)

  subtract = cv.cvtColor(subtractC, cv.COLOR_BGR2GRAY)
  kernel = np.ones((3, 3), np.uint8)
  opening = cv.morphologyEx(subtract, cv.MORPH_OPEN, kernel)
  
  # subtract = cv.fastNlMeansDenoising(subtract, subtract, 7,21)

  # Find the contours of the grayscale image
  # contours, _ = cv.findContours(subtract, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

  # Draw the contours on the grayscale image
  # cv.drawContours(subtractC, contours, -1, (0, 255, 0), 1)
  # binary = cv.adaptiveThreshold(subtract, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 61, 10)
  __, binary = cv.threshold(opening, 10, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)
  binary = cv.dilate(binary, kernel, iterations = 1)
  # binary = denoise(bindary)
  # feed = denoise(subtract)


  return binary



none = cv.imread('./mask_pics_1/NONE4.jpg')
part = cv.imread('./mask_pics_1/STANDARD4.jpg')


cv.imshow("result", compare(part, none))
cv.waitKey(0)
cv.destroyAllWindows()
