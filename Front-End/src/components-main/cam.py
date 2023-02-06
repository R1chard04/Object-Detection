import cv2 as cv
import time

# Initialize the webcam
cap = cv.VideoCapture(0)

# Define the folder to save the images
path = "C:/Users/henrique.engelke/Documents/GitHub/Welding-Project/Front-End/src"

# Take a picture every second and save it in the folder
while True:
    ret, frame = cap.read()
    if ret:
        cv.imwrite("C:/Users/henrique.engelke/Documents/GitHub/Welding-Project/Front-End/src/camPic.jpg", frame)
        time.sleep(1)
        key = cv.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    else:
        break

# Release the webcam
cap.release()
cv.destroyAllWindows()
