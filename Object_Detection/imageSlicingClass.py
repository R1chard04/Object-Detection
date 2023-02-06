import cv2
import numpy as np
import datetime

class imageSlicing:
    def __init__(self, img, all_images) -> None:
        self.img = img
        self.all_images = all_images
        self.counter = 1
    
    def slicingImage(self) -> None:
        #Get image hieght and width
        height = self.img.shape[0]
        width = self.img.shape[1]

        width_cutoff = width // 2
        height_cutoff = height // 2
        self.image_topleft = self.img[:height_cutoff, :width_cutoff]
        self.image_topright = self.img[:height_cutoff, width_cutoff:]
        self.image_bottomleft = self.img[height_cutoff:, :width_cutoff]
        self.image_bottomright = self.img[height_cutoff:, width_cutoff:]

        self.all_images = ([self.image_topleft, self.image_topright, self.image_bottomleft, self.image_bottomright])
        
        current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        
        for i, img in enumerate(self.all_images):
            if i == 0:
                filename = "image_topleft"
            elif i == 1:
                filename = "image_topright"
            elif i == 2:
                filename = "image_bottomleft"
            else:
                filename = "image_bottomright"
                
            cv2.imwrite(f'./{filename}({current_time})({self.counter}).jpg', img)
        
        self.counter += 1
            
image = cv2.imread("./STANDARD.jpg")
all_images = 0
myImage = imageSlicing(image, all_images)
myImage.slicingImage()


