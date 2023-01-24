import cv2
import numpy as np
import matplotlib.pyplot as plt

'''
# object = cv2.createBackgroundSubtractorM0G2(history, varThreshold, detectShadows)


#Load a video
cap = cv2.VideoCapture('Photos/IMG_4965.mp4')

# you can optionally work on the live web cam

# create the background object, if shadow is not detected then shown as gray. 
# History controls how many images stored for foreground. (Default value = 500.)
# varThreshold detects squared distance between pixel to decide if pixel is apart of background model. (Default value = 16)
backgroundobject = cv2.createBackgroundSubtractorMOG2(varThreshold = 100, history = 10, detectShadows = True)

while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break
    else:

        # apply the background object on each frame
        fgmask = backgroundobject.apply(frame)

        # also extracting the real detected foreground part of the image (optional)
        real_part = cv2.bitwise_and(frame,frame,mask=fgmask)

        # masking fgmask 3 channeled so it can be stacked with others.
        # 2 channel image is black/white, and 3 channel image is RGB. COLOR_GRAY2BGR duplicates GRAY channel to get 3 channels.

        fgmask_3 = cv2.cvtColor(fgmask, cv2.COLOR_GRAY2BGR)

        # Stack all three frames and show the image
        stacked = np.hstack((fgmask_3,frame,real_part))
        cv2.imshow('All three',cv2.resize(stacked,None,fx=0.65,fy=0.65))
    
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    
cap.release()
cv2.destroyAllWindows()
#____________________________________________________________________
'''

#Load video
video = cv2.VideoCapture('Photos/IMG_4965.mp4')
#Initialize background object
#Detect shadows seperates entities from their shadows so objects with overlapping shadows do not count as 1, is not visual.
BackgroundObject = cv2.createBackgroundSubtractorMOG2(detectShadows = True)

while(video.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break
    else:
        #Apply the background object on the frame to get the segmented mask.
        fgmask = BackgroundObject.apply(frame)

        #Array of numerical co-efficents for pixels in an image. None is default 3x3 size.
        kernel = None

        #Since shadows are masked as grey and objects as white. We can set threshold to ignore grey.
        _, fgmask = cv2.threshold(fgmask, 250, 255, cv2.TRESH_BINARY)

        #Dilation increases white area of figures
        #Erode increases black area of mask
        fgmask = cv2.erode(fgmask, kernel, iterations = 1)
        fgmask = cv2.dilate(fgmask, kernel, iterations = 2)








        






