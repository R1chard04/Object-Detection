# Martinrea Hydroform Solution - Parts Present Detection Project (2023)

## This is a project using camera with machine learning to develop an AI system detects the present of objects inside a frame.

### Our process:
+ Installing two different cameras to get different perspective of the same object.
+ Using algorithms to generate two images from two point of view.
+ Using openCV's calibration method to undistort all the distortions of the images.
+ Using stitching method to find the overlapped part of two images, then combine them into one image.
+ Running through several algorithms to process the images such as detecting the edges of the object or calculate for the offset. 

The result would be a camera can detect whether the object is in the right place before we can proceed to further operations for example clamping or welding. 

### Requirements:
+ `<style>Python 3.9 to 3.11{color:Blue;}</style>` is required.
