from imageSlicing import imageSlicing
import cv2 as cv

img = cv.imread("")

img_slicer = imageSlicing(img)
result = img_slicer.imageSlicing()

for i, res in enumerate(result):
    cv.imwrite(f"./Quadrant {i+1}", res)