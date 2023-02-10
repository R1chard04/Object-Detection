import cv2 as cv

# Load the image
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





#---------------put text----------------#
# Define the text to be displayed

# Set the font and size of the text
font = cv.FONT_HERSHEY_SIMPLEX
font_scale = 10
thickness = 30

# Get the size of the text
text_size = cv.getTextSize(text, font, font_scale, thickness)[0]

# Get the text position
# text_x = (frame.shape[1] - text_size[0]) // 2
# text_y = (frame.shape[0] + text_size[1]) // 2

# text_x = frame.shape[1] * 3//4 -20 #2860
text_x = 2800
# print(text_x)
# text_y = frame.shape[0] * 7//8 #1890
text_y = 1700
# print(text_y)

color = (0, 255, 0)

# for the parts
blue = (255, 0 ,0)
shift_y = 0
shift_x = 10
gap = 90
partsFontScale = 3
partsFontthickness = 4

# 2160*3840
box_x1 = 2800 
box_x2 = 3780
box_y1 = 1700 - 115
box_y2 = 2100

# 17 19 42 hexcode for martinrea blue

# Display the text on the image
# cv.putText(frame, text, (text_x, text_y), font, font_scale, color, thickness)

# start_point, end_point
frame = cv.rectangle(frame, (box_x1, box_y1), (box_x2, box_y2), (255, 255, 255), -1)

title_y = 1610+60 #1610
line_y = title_y +20

frame = cv.putText(frame, "RESULTS", (text_x + shift_x, title_y), font, partsFontScale, blue, partsFontthickness+4)
frame = cv.line(frame, (box_x1+20, line_y), (box_x2-20, line_y), blue, 3)
frame = cv.putText(frame, "Bottom: ", (text_x + shift_x, text_y + gap*4- shift_y), font, partsFontScale, blue, partsFontthickness)
frame = cv.putText(frame, "Top: ", (text_x + shift_x, text_y + gap*3- shift_y), font, partsFontScale, blue, partsFontthickness)
frame = cv.putText(frame, "Right: ", (text_x + shift_x, text_y + gap*2- shift_y), font, partsFontScale, blue, partsFontthickness)
frame = cv.putText(frame, "Left: ", (text_x + shift_x, text_y + gap- shift_y), font, partsFontScale, blue, partsFontthickness)


# Save the image
cv.imwrite("square_on_image.jpg", frame)

frame = cv.pyrDown(frame)
frame = cv.pyrDown(frame)

# Display the image
cv.imshow("Square on Image", frame)


# Wait for user to close the window
cv.waitKey(0)

# Destroy all windows
cv.destroyAllWindows()

# # For bounding box
# img = cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
 
# # For the text background
# # Finds space required by the text so that we can put a background with that amount of width.
# (w, h), _ = cv2.getTextSize(
#         label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)

# # Prints the text.    
# img = cv2.rectangle(img, (x1, y1 - 20), (x1 + w, y1), color, -1)
# img = cv2.putText(img, label, (x1, y1 - 5),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 1)

# # For printing text
# img = cv2.putText(img, 'test', (x1, y1),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)