from imageSlicing import imageSlicing
import cv2 as cv

<<<<<<< HEAD
img = cv.imread("")
=======
img = cv.imread("./mask.jpg")
>>>>>>> c7ae85b91b75f335783ef39e59dcea84f457f16b

img_slicer = imageSlicing(img)
result = img_slicer.imageSlicing()

for i, res in enumerate(result):
    cv.imwrite(f"./Quadrant {i+1}.jpg", res)