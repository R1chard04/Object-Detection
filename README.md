# Winter Workterm - Parts Present Detection Project (2023)

## Contributors = [Eren Yilmaz, Henrique Rodrigues, Jamie Yen, Kent Tran, Leo You]

## This is a work term project using camera to develop an AI system detects the presence of objects inside a frame, which is connected to a PLC and shown on UI.

### Our process:

- Installing multiple cameras to get different perspective of the same object.
- Using algorithms to generate two images from two point of view.
- Using openCV's calibration method to undistort all the distortions of the images.
- Using stitching method to find the overlapped part of two images, then combine them into one image.
- Running through several algorithms to process the images such as detecting the edges of the object or calculate for the offset.

The result would be a camera that can detect whether the object is in the right place from anywhere in the room before we can proceed to further operations like manufacturing.

### Requirements:

- [Python 3.9 to 3.11.1](https://www.python.org/downloads/release/python-3111/) is required.
- [OpenCV Python (4.7.0)](https://pypi.org/project/opencv-python/) installation.
- [DepthAI](https://docs.luxonis.com/projects/api/en/latest/install/) installation.
- [NodeJS 16](https://nodejs.org/en/download/) is required.

### Local Development:

```
# Clone the repo
$ git clone https://github.com/Kenttrann2302/Object-Detection/
# Move into directories
$ cd <directory-name>
# Install the requirements to run the program
$ pip install <packages-name>
# Start the program and have fun!!!
$ python main.py

# How to start live photos on http://localhost:3000/
# Install all the dependencies
$ npm install
# Start local host server
$ npm start
```

![Test Image 1](https://github.com/Kenttrann2302/Object-Detection/blob/main/GB5JR7Q.png)
![Test Image 1](https://github.com/Kenttrann2302/Object-Detection/blob/main/GB5JR7Q.png)
![Test Image 1](https://github.com/Kenttrann2302/Object-Detection/blob/main/GB5JR7Q.png)![Test Image 1](https://github.com/Kenttrann2302/Object-Detection/blob/main/GB5JR7Q.png)![Test Image 1](https://github.com/Kenttrann2302/Object-Detection/blob/main/GB5JR7Q.png)![Test Image 1](https://github.com/Kenttrann2302/Object-Detection/blob/main/GB5JR7Q.png)![Test Image 1](https://github.com/Kenttrann2302/Object-Detection/blob/main/GB5JR7Q.png)![Test Image 1](https://github.com/Kenttrann2302/Object-Detection/blob/main/GB5JR7Q.png)![Test Image 1](https://github.com/Kenttrann2302/Object-Detection/blob/main/GB5JR7Q.png)![Test Image 1](https://github.com/Kenttrann2302/Object-Detection/blob/main/GB5JR7Q.png)![Test Image 1](https://github.com/Kenttrann2302/Object-Detection/blob/main/GB5JR7Q.png)![Test Image 1](https://github.com/Kenttrann2302/Object-Detection/blob/main/GB5JR7Q.png)![Test Image 1](https://github.com/Kenttrann2302/Object-Detection/blob/main/GB5JR7Q.png)
