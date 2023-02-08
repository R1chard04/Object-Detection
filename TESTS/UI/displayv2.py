import cv2 as cv

# define starting point
x1 = 100
y1 = 300

# define ending point
x2 = 400
y2 = 1600

color = (0,255,0)
text_color = (255,255,255)
label = "PASS"

# Load the image
frame = cv.imread('STD.jpg')

# For bounding box
frame = cv.rectangle(frame, (x1, y1), (x2, y2), color, 3)
 
# For the text background
# Finds space required by the text so that we can put a background with that amount of width.
(w, h), _ = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.6, 1)

# Prints the text.    
frame = cv.rectangle(frame, (x1, y1 - 20), (x1 + w, y1), color, -1)
frame = cv.putText(frame, label, (x1, y1 - 5), cv.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 1)

# For printing text
frame = cv.putText(frame, 'test', (x1, y1), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 3)

frame = cv.pyrDown(frame)
frame = cv.pyrDown(frame)

# Display the image
cv.imshow("Square on Image", frame)


# Wait for user to close the window
cv.waitKey(0)

# Destroy all windows
cv.destroyAllWindows()