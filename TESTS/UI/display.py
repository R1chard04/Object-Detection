import cv2 as cv

# Load the image
frame = cv.imread('STD.jpg')
# 2160*3840 window size

#---------------put box----------------#
# Define the square coordinates
x1, y1 = 50, 50
x2, y2 = 200, 200

# Draw the square on the image
cv.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), -1)


#---------------put text----------------#
# Define the text to be displayed
text = "PASS"

textt = "FAIL"

# Set the font and size of the text
font = cv.FONT_HERSHEY_SIMPLEX
font_scale = 10
thickness = 30

# Get the size of the text
text_size = cv.getTextSize(text, font, font_scale, thickness)[0]

# Get the text position
# text_x = (frame.shape[1] - text_size[0]) // 2
# text_y = (frame.shape[0] + text_size[1]) // 2

text_x = frame.shape[1] * 3//4 -20
print(text_x)
text_y = frame.shape[0] * 7//8

color = (0, 255, 0)

# for the parts
blue = (255, 0 ,0)
shift_y = 160
shift_x = 130
gap = 100
partsFontScale = 3
partsFontthickness = 4


# Display the text on the image
# cv.putText(frame, text, (text_x, text_y), font, font_scale, color, thickness)
cv.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), -1)

cv.putText(frame, "Top: ", (text_x , text_y - gap*4 - shift_y), font, partsFontScale, blue, partsFontthickness)
cv.putText(frame, "Left: ", (text_x , text_y - gap*3- shift_y), font, partsFontScale, blue, partsFontthickness)
cv.putText(frame, "Bottom: ", (text_x , text_y - gap*2- shift_y), font, partsFontScale, blue, partsFontthickness)
cv.putText(frame, "Right: ", (text_x , text_y - gap- shift_y), font, partsFontScale, blue, partsFontthickness)


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