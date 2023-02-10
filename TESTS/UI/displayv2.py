import cv2 as cv

frame = cv.imread('STD.jpg')
# 2160*3840 window size
station100 = ["Top", "Left", "Bottom", "Right"]
x2 = 3840 - 60
y2 = 2160 - 60
x1 = x2 - 800
y1 = 0
output_x = x2 - 40
output_y = []
line_p1 = (0,0)
line_p2 = (0,0)

def displayResultPosition(parts):
    num = len(parts)
    n = 0
    while (n < num):
        output_y.append(y2 -40 -90* (num-n-1))
        n = n + 1

line_p1 = (x1+20, output_y[-1]-100)
line_p2 = (0,output_y[-1]-100)
print("line_p1: ", line_p1)
print("line_p2: ", line_p2)

y1 = output_y[-1] - 205

displayResultPosition(station100)
for i in output_y:
    print (i)

frame = cv.pyrDown(frame)
frame = cv.pyrDown(frame)

# Display the image
cv.imshow("Square on Image", frame)

cv.waitKey(0)
cv.destroyAllWindows()