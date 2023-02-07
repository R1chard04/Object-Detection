import cv2
import numpy as np
import os
from os import listdir
import os.path

# Get user input numbers
input_numbers = []
print("1: image_topleft \n2: image_topright \n3: image_bottomleft \n4: image_bottomright \nInput a quadrant that should be split out")
while len(input_numbers) < 4:
    user_input = input()
    if user_input == 'p':
        break
    elif user_input.isdigit() and 1 <= int(user_input) <= 4:
        if int(user_input) in input_numbers:
            print("Number already chosen. Enter another number or enter 'p' to end inputting numbers.")
        else:
            input_numbers.append(int(user_input))
            print("Input another quadrant to be split or enter 'p' to end inputting numbers.")
    else:
        print("Invalid input. Enter a number from 1 to 4 or enter 'p' to end inputting numbers.")

# Get image height and width
img = cv2.imread("./NONE.jpg")

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

# Convert user input to result
result = []
non_chosen_images = []
for i in range(1, 5):
    if i in input_numbers:
        result.append(quadrant_map[i])
    else:
        if i == 1:
            non_chosen_image = img[:height_cutoff, :width_cutoff]
        elif i == 2:
            non_chosen_image = img[:height_cutoff, width_cutoff:]
        elif i == 3:
            non_chosen_image = img[height_cutoff:, :width_cutoff]
        else:
            non_chosen_image = img[height_cutoff:, width_cutoff:]
        non_chosen_images.append(non_chosen_image)

# Combine non-chosen images
if len(non_chosen_images) == 2:
    if 1 in input_numbers and 2 in input_numbers:
        result.append(cv2.hconcat(non_chosen_images))
    elif 3 in input_numbers and 4 in input_numbers:
        result.append(cv2.hconcat(non_chosen_images))
    elif 1 in input_numbers and 3 in input_numbers:
        result.append(cv2.vconcat(non_chosen_images))
    elif 2 in input_numbers and 4 in input_numbers:
        result.append(cv2.vconcat(non_chosen_images))
        
    # Get aspect ratio of the quadrant
    aspect_ratio = height / width

    # Get height of combined image
    combined_height = int(result[0].shape[1] * aspect_ratio)

    # Resize the combined image to have the same aspect ratio as the quadrant but different width to fit everything
    result[0] = cv2.resize(result[0], (result[0].shape[1], combined_height),
                       interpolation=cv2.INTER_CUBIC)

# Use cv.imshow to output the result
for i, res in enumerate(result):
    window_height = int(res.shape[0] * 0.7)
    window_width = int(res.shape[1] * 0.7)
    cv2.namedWindow(f"Quadrant {i+1}", cv2.WINDOW_NORMAL)
    cv2.resizeWindow(f"Quadrant {i+1}", window_width, window_height)
    cv2.imwrite(f"./Quadrant {i+1}", res)

cv2.waitKey(0)
cv2.destroyAllWindows()