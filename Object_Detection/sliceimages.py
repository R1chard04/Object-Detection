from imageSlicing import imageSlicing
import cv2 as cv

img = cv.imread("Object_Detection/Photos/MASKS/1675868011079.jpg")

img_slicer = imageSlicing(img)
result = img_slicer.imageSlicing()

for i, res in enumerate(result):
    cv.imwrite(f"./Quadrant {i+3}.jpg", res)