import cv2 as cv
import time
import depthai as dai
from cameraInitialisationClass import initialise
from imageProcessingClasses import imageProcessing
from imageCaptureClasses import imageCapture
from imageMaskGeneration import createMask
from imagePredictionClass import MSEStabilization, getPassRef
import numpy as np
import time
import os
import json
import pdb

# from pylogix import PLC
# from PLCUpdate import transferToPLC

#-----------------------------------------Directories-----------------------------------------#
#Photos Path
photosPath = "Photos\Init" #This is where all the images are being saved

#MSE Initialisation Photos Path
errDir = "Photos\Err" #This is whered the difference images can be saved; they are not currently

#Mask Paths
refDir = "Photos\Refs" #This is where the reference photos for each part at one station are being saved
colDir = "Photos\Col" #This is where the alternate colour reference photos for each part at one station are being saved
maskDir = "Photos\Masks" #This is where the generated masks are being saved

#IPs
IPString = "169.254.1."
IPEndpoint = 199

#Part List
with open(r'parts.json') as f:
  partList = json.load(f)
stations = list(partList.keys())

partsLayered = []
stationValues = list(partList.values())
for i in range(len(stationValues)):
    partsLayered.append(list(stationValues[i].values()))

partsPerStation = []
for i in range(len(partsLayered)):
    temp = [item for sub_list in partsLayered[i] for item in sub_list]
    partsPerStation.append(temp)

#Folders:
for i in range(len(stations)):
    refFolder = os.path.join(refDir, stations[i])
    colFolder = os.path.join(colDir, stations[i])
    maskFolder = os.path.join(maskDir, stations[i])
    errFolder = os.path.join(errDir, stations[i])
    initFolder = os.path.join(photosPath, stations[i])

    if not os.path.isdir(refFolder): 
        os.mkdir(refFolder)
    if not os.path.isdir(colFolder): 
        os.mkdir(colFolder)
    if not os.path.isdir(maskFolder): 
        os.mkdir(maskFolder)
    if not os.path.isdir(errFolder): 
        os.mkdir(errFolder)
    if not os.path.isdir(initFolder): 
        os.mkdir(initFolder)

#----------------------Initialisation---------------------#

def maskSetup(selected, captureObject, recalibrate, brightness, lensPos, name):
    refs = []
    cols = []
    masks = []    
    print("entered mask")
    
    # we don't want to recalibrate for now
    recalibrate = False
    
    if recalibrate == True:

        refFolder = os.path.join(refDir, stations[selected])
        colFolder = os.path.join(colDir, stations[selected])
        maskFolder = os.path.join(maskDir, stations[selected])

        for i in range(len(partsLayered[selected])):
            for j in range(len(partsLayered[selected][i])):
                refPath = os.path.join(refFolder, str(partsPerStation[selected][j]) + ".jpg")
                colPath = os.path.join(colFolder, str(partsPerStation[selected][j]) + ".jpg")
                maskPath = os.path.join(maskFolder, str(partsPerStation[selected][j]) + ".jpg")
                
                messageRef = "Load "
                messageRef += str(partsPerStation[selected][j]) + " part. Press `C`` to continue."
                # if i == 0:
                    
                # else:
                #     for k in range(len(partsLayered[selected][0])):
                #         messageRef += str(partsLayered[selected][k]) + " part, "
                #     messageRef += "and " + str(partsPerStation[selected][j]) +" part. Press `C` to continue."

                ans = input(messageRef)               
                # cv.waitKey(0)
                refs.append(captureObject.captureOne(refPath, brightness, lensPos))
                cv.destroyAllWindows()

                messageCol = "Change " + str(partsPerStation[selected][j]) + " part to coloured part. Press `C` to capture."
                ans = input(messageCol)
                # cv.waitKey(0)
                cols.append(captureObject.captureOne(colPath, brightness, lensPos))
                cv.destroyAllWindows()

                print("Creating a mask, this may take a minute.")
                masks.append(createMask(refs[j], cols[j], maskPath))
                print("Mask generated")
    else:
        temp = []
        pdb.set_trace()
        for image in os.dir.list(os.path.join(maskDir, stations[selected])):
            temp.append(image)
            masks.append(image)
        for i in range(len(temp)):
            for j in range(len(partsPerStation)):
                if temp[i] == (partsPerStation[j] + ".jpg"):
                    masks[j] = cv.imread(temp[i])
    
    return masks

def paramsSetup(selected, captureObject, recalibrate, name):
    #Station prameters
    with open(r'params.json') as f:
        paramsList = json.load(f)

    if recalibrate:
        #Camera frame and brightness setup window 
        print("press ,/. to adjust focal length")
        print("press k/l to adjust birghtness")
        print("press 1 to turn on/off auto white balance lock")
        print("press 2 to turn on/off auto exposure lock")
        print("press q to finish settings")
        brightness, lensPos = captureObject.setParameters(name)

        paramsList[stations[selected]]['brightness'] = brightness
        paramsList[stations[selected]]['lensPos'] = lensPos
        cv.destroyAllWindows()
    else:
        brightness = paramsList[stations[selected]]['brightness']
        lensPos = paramsList[stations[selected]]['lensPos']

    return brightness, lensPos

def controlSetup(selected, captureObject, recalibrate, brightness, lensPos):
    path = os.path.join(refDir, stations[selected], "STD.jpg")
    # if recalibrate is True or os.path.isfile(path) is False:
    #     print("Load all parts. Press `C`` to continue")
    #     cv.waitKey(0)
    #     tempRef = captureObject.captureOne(path, brightness, lensPos) #Creating a stand-in initialisation picture
    # else:
    #     tempRef = cv.imread(path)
    tempRef = cv.imread(path)
    return tempRef

def errorSetup(selected, captureObject, processingObject, recalibrate, brightness, lensPos):
    # pdb.set_trace()
    with open(r'errors.json') as f:
        passref = json.load(f)

    if recalibrate is True:
        for i in range(10):
            testImg = captureObject.captureOne(os.path.join(errDir, stations[selected],"Test " + str(i) + ".jpg"), brightness, lensPos)
            time.sleep(0.5)
        # Taking a standard image
        ref = captureObject.captureOne(os.path.join(refDir, stations[selected],"STD.jpg"), brightness, lensPos)
        #Post-processing of captured images for MSE threshold creation
        passRef = [0] * len(passref[stations[selected]])

        for image in os.listdir(os.path.join(errDir, stations[selected])):
            path = os.path.join(errDir, stations[selected], image)
            img = cv.imread(path)

            processingObject.setTestImg(img)   
            error = processingObject.compareImage()
            passRef = getPassRef(error, passRef)
            print(error, passRef)
        passref[stations[selected]] = passRef

    else:
        ref = cv.imread(os.path.join(refDir, stations[selected],"STD.jpg"))
    return ref, passref

#-----------------------------------------Main Loop-----------------------------------------#
def mainloop(selected):
    print("here")
    #-----------------------------------------Camera Initialisation-----------------------------------------#
    time.sleep(selected+0.1)
    IP = IPEndpoint + selected
    
    
    IP = IPString + str(IP)
    
    recalibrate = True

    initialisationObject = initialise(photosPath)
    print("here1")
    photoDirectoryName, pipeline, camRgb, xoutRgb, xin, videoEnc, xoutStill = initialisationObject.initialise()

    for device in dai.Device.getAllAvailableDevices():
        print(f"{device.getMxId()} {device.state}")
    # print(IP)
    device_info = dai.DeviceInfo(IP)
    device_info.state = dai.XLinkDeviceState.X_LINK_BOOTLOADER
    device_info.protocol = dai.XLinkProtocol.X_LINK_TCP_IP
    

    #----------------------Camera Capture Initialisation---------------------#
    #This needs to be setup for multiple cameras
    
    with dai.Device(pipeline, device_info) as device:
        
        captureObject = imageCapture(device.getOutputQueue(name="rgb", maxSize=30, blocking=False), 
                                    device.getOutputQueue(name="still", maxSize=30, blocking=True), 
                                    device.getInputQueue(name="control"))
        # brightness, lensPos = paramsSetup(selected, captureObject, recalibrate, IP)
        brightness = -1
        lensPos = 108
        print(IP)
        # print("done params")

        # masks = maskSetup(selected, captureObject, recalibrate, brightness, lensPos, IP)
    
        # print("done masks")
        # tempRef = controlSetup(selected, captureObject, recalibrate, brightness, lensPos)
        # print("done control setup")
        # processingObject = imageProcessing(masks, tempRef, tempRef, partsPerStation[selected]) #Initialisation of the processing object
        # print("processing object initialized")

        # ref, passref = errorSetup(selected, captureObject, processingObject, recalibrate, brightness, lensPos)
        # print("errorsetup")
        # processingObject.setRefImg(ref)
        # print("refsetup")

    #-------------------------------------------------------------------------------------------#   
        # while True:
            # print("here5")

            # capture a test image
        captureObject.captureOne(os.path.join(photosPath, stations[selected],"Test.jpg"), brightness, lensPos, IP)
            # cv.waitKey(1)
            # time.sleep(0.5)
            # processingObject.setTestImg(img)  
            # # display the result on the frame
            # frame = processingObject.displayResultPosition()
            # # get the mse error
            # error = processingObject.compareImage() 
            # #Generates PASS/FAIL array
            # prediction = MSEStabilization(error, passref[stations[selected]], len(passref[stations[selected]])) 

            # result = prediction.result()
            # # print(result)

            # # transferToPLC("OP100", result)
            # cv.waitKey(1)
            # frame = cv.pyrDown(frame)
            # frame = cv.pyrDown(frame)
            # cv.imshow(IP, frame)
            

