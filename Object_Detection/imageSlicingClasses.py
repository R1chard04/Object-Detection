import cv2
import numpy as np
import os
from os import listdir
import os.path

def input_number(input_number) -> None:       

    # Get user input numbers
    print("1: image_topleft \n2: image_topright \n3: image_bottomleft \n4: image_bottomright \n5: vertical cut \n6: horizontal cut\nInput a quadrant or a cut that should be split out")
    while len(input_number) < 2:
        user_input = input()
        if user_input == 'p':
            break
        elif user_input.isdigit() and 1 <= int(user_input) <= 6:
            if int(user_input) in input_number:
                print("Number already chosen. Enter another number or enter 'p' to end inputting numbers.")
            else:
                input_number.append(int(user_input))
                print("Input another quadrant to be split or enter 'p' to end inputting numbers.")
        else:
            print("Invalid input. Enter a number from 1 to 4 or enter 'p' to end inputting numbers.")

class imageSlicing:
    def __init__(self, img, input_number):

        self.img = img
        self.input_number = input_number
    
    def slice_image(self) -> any:
                
            # Get image height and width
            img = self.img
            height, width = img.shape[:2]

            #Slice image into 4 quadrants
            width_cutoff = width // 2
            height_cutoff = height // 2
            quadrant_map = {
                1: img[:height_cutoff, :width_cutoff],
                2: img[:height_cutoff, width_cutoff:],
                3: img[height_cutoff:, :width_cutoff],
                4: img[height_cutoff:, width_cutoff:],
            }

            # Convert user input to result
            result = []
            for i in range(1, 5):
                if i in self.input_number:
                    result.append(quadrant_map[i])
            
            # Combine non-chosen images
            if len(result) == 2:
                if 1 in self.input_number and 2 in self.input_number:
                    non_chosen_images = [quadrant_map[3], quadrant_map[4]]
                    result.append(cv2.hconcat(non_chosen_images))
                elif 3 in self.input_number and 4 in self.input_number:
                    non_chosen_images = [quadrant_map[1], quadrant_map[2]]
                    result.append(cv2.hconcat(non_chosen_images))
                elif 1 in self.input_number and 3 in self.input_number:
                    non_chosen_images = [quadrant_map[2], quadrant_map[4]]
                    result.append(cv2.vconcat(non_chosen_images))
                elif 2 in self.input_number and 4 in self.input_number:
                    non_chosen_images = [quadrant_map[1], quadrant_map[3]]
                    result.append(cv2.vconcat(non_chosen_images))
                        
                #Resize the combined image to have the same aspect ratio as the quadrant but different width to fit everything
                aspect_ratio = height / width
                combined_height = int(result[0].shape[1] * aspect_ratio)
                result[0] = cv2.resize(result[0], (result[0].shape[1], combined_height),
                                interpolation=cv2.INTER_CUBIC)

            if self.input_number and 5 in self.input_number:
                result.append(cv2.vconcat([quadrant_map[1], quadrant_map[3]]))
                result.append(cv2.vconcat([quadrant_map[2], quadrant_map[4]]))
                
            if self.input_number and 6 in self.input_number:
                result.append(cv2.hconcat([quadrant_map[1], quadrant_map[2]]))
                result.append(cv2.hconcat([quadrant_map[3], quadrant_map[4]]))
            
            return result

    def show_cut_images(self, result) -> None:
        #Use cv.imshow to output the result
        for i, res in enumerate(result):
            window_height = int(res.shape[0] * 0.7)
            window_width = int(res.shape[1] * 0.7)
            cv2.namedWindow(f"Quadrant {i+1}", cv2.WINDOW_NORMAL)
            cv2.resizeWindow(f"Quadrant {i+1}", window_width, window_height)
            cv2.imshow(f"Quadrant {i+1}", res)
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()

#How to call script:

#from imageSlicingClasses import imageSlicing, input_number
#import cv2 as cv
    
#input_number_array = []
#input_number(input_number_array)

# Put above outside of the loop

#frame = cv.imread("./Quadrant1.jpg")
#img_slicer = imageSlicing(frame, input_number_array)
#result = img_slicer.slice_image()
#img_slicer.show_cut_images(result)
                



