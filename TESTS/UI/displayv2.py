import cv2 as cv

frame = cv.imread('STD.jpg')
# 2160*3840 window size
# parts = ["Top: ", "Left: ", "Bottom: ", "Right: "]
parts = ["Top: ", "Left: ", "Bottom: ", "Right: ", "your mom: "]

MSEResults = [0]*len(parts)
partsFontthickness = 3
fontColor = (75, 25 ,23)
partsFontScale = 3
font = cv.FONT_HERSHEY_SIMPLEX

x2 = 3840 - 60
y2 = 2160 - 60
x1 = x2 - 1000
y1 = 0
output_x = []
# text location for the parts
output_x.append(x1 + 10)
# text location for the mseResults
output_x.append(x1 + 400)
output_y = []
line_p1 = (0,0)
line_p2 = (0,0)

def displayResultPosition(partList):
    num = len(partList)
    n = 0
    while (n < num):
        output_y.append(y2 -40 -90* (num-n-1))
        n = n + 1

print("hellow")
displayResultPosition(parts)
line_p1 = (x1+20, output_y[0]-100)
line_p2 = (x2 -10,output_y[0]-100)
print("line_p1: ", line_p1)
print("line_p2: ", line_p2)

y1 = output_y[0] - 205
print(output_y)
print(y1)

frame = cv.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), -1)
frame = cv.putText(frame, "RESULTS", (output_x[0] , output_y[0] - 120), font, partsFontScale, fontColor, partsFontthickness+3)
frame = cv.line(frame, line_p1, line_p2, fontColor, 3)


i = len(parts) -1
while i >= 0:
    frame = cv.putText(frame, parts[i], (output_x[0], output_y[i]), font, partsFontScale, fontColor, partsFontthickness)
    frame = cv.putText(frame, str(MSEResults[i]), (output_x[1], output_y[i]), font, partsFontScale, fontColor, partsFontthickness)
    i = i -1

frame = cv.pyrDown(frame)
frame = cv.pyrDown(frame)

# Display the image
cv.imshow("Square on Image", frame)

cv.waitKey(0)
cv.destroyAllWindows()