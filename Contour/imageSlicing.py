import cv2
import numpy as np
import os
from os import listdir
import os.path

# Get input numbers
input_numbers = []
while len(input_numbers) < 4:
    user_input = input("Input number from 1 to 4: ")
    if user_input == 'p':
        break
    elif user_input.isdigit() and 1 <= int(user_input) <= 4:
        if int(user_input) in input_numbers:
            print("Number already chosen. Enter another number or press 'p' to end inputting numbers.")
        else:
            input_numbers.append(int(user_input))
            print("Input another number or press 'p' to end inputting numbers.")
    else:
        print("Invalid input. Enter a number from 1 to 4 or press 'p' to end inputting numbers.")

# Get image height and width
img = cv2.imread("./STANDARD.jpg")
height = img.shape[0]
width = img.shape[1]

#Slice image into 4 quadrants
width_cutoff = width // 2
height_cutoff = height // 2
image_topleft = img[:height_cutoff, :width_cutoff]
image_topright = img[:height_cutoff, width_cutoff:]
image_bottomleft = img[height_cutoff:, :width_cutoff]
image_bottomright = img[height_cutoff:, width_cutoff:]

# Assign a quadrant to each number 1 to 4
quadrant_map = {
    1: image_topleft,
    2: image_topright,
    3: image_bottomleft,
    4: image_bottomright,
}

#Convert user input to result
result = []
non_chosen_images = []
for i in range(1, 5):
    if i in input_numbers:
        result.append(quadrant_map[i])
    else:
        result.append
        non_chosen_images.append(img[:height_cutoff, :width_cutoff])

#Combine non-chosen images
if len(non_chosen_images) == 2:
    if 1 in input_numbers and 2 in input_numbers:
        result.append(cv2.hconcat(non_chosen_images))
    elif 3 in input_numbers and 4 in input_numbers:
        result.append(cv2.hconcat(non_chosen_images))
    elif 1 in input_numbers and 3 in input_numbers:
        result.append(cv2.vconcat(non_chosen_images))
    elif 2 in input_numbers and 4 in input_numbers:
        result.append(cv2.vconcat(non_chosen_images))
        
# Use cv.imshow to output the result
for i, res in enumerate(result):
    cv2.imshow(f"Quadrant {i+1}", res)

cv2.waitKey(0)
cv2.destroyAllWindows()