import cv2 as cv
import time
import depthai as dai
from cameraInitialisationClass import initialise
from imageProcessingClasses import imageProcessing
from imageCaptureClasses import imageCapture
from imageMaskGeneration import createMask
from imagePredictionClass import MSEStabilization, getPassRef
import time
import os
import json
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
IPEndpoint = 200

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

#----------------------Initialisation---------------------#

def maskSetup(selected, captureObject, recalibrate, brightness, lensPos):
    refs, cols, masks = []

    if recalibrate == True:
        for i in range(len(partsLayered[selected])):
            for j in range(len(partsLayered[selected][i])):
                refPath = os.path.join(refDir, stations[selected], partsLayered[j] + ".jpg")
                colPath = os.path.join(colDir, stations[selected], partsLayered[j] + ".jpg")
                maskPath = os.path.join(maskDir, stations[selected], partsLayered[j] + ".jpg")

                messageRef = "Load "
                if i == 0:
                    messageRef += partsLayered[j] + " part. Press `C`` to continue."
                else:
                    for k in range(len(partsLayered[0])):
                        messageRef += partsLayered[0][k] + " part, "
                    messageRef += "and " + partsLayered[j] +"part. Press `C` to continue."

                print(messageRef)
                cv.waitKey(0)

                refs.append(captureObject.captureOne(refPath, brightness, lensPos))
                cv.destroyAllWindows()

                messageCol = "Change " + partsLayered[j] + " part to coloured part. Press `C` to capture."
                print(messageCol)
                cv.waitKey(0)
                cols.append(captureObject.captureOne(colPath, brightness, lensPos))
                cv.destroyAllWindows()

                print("Creating a mask, this may take a minute.")
                masks.append(createMask(refs[i], cols[i], maskPath))
                print("Mask generated")
    else:
        temp = []
        for image in os.list.dir(os.path.join(maskDir, stations[selected])):
            temp.append(image)
            masks.append(image)
        for i in range(len(temp)):
            for j in range(len(partsPerStation)):
                if temp[i] == (partsPerStation[j] + ".jpg"):
                    masks[j] = cv.imread(temp[i])
    
        return masks

def paramsSetup(selected, captureObject, recalibrate):
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
        brightness, lensPos = captureObject.setParameters()

        paramsList[stations[selected]]['brightness'] = brightness
        paramsList[stations[selected]]['lensPos'] = lensPos

    else:
        brightness = paramsList[stations[selected]]['brightness']
        lensPos = paramsList[stations[selected]]['lensPos']

    return brightness, lensPos

def controlSetup(selected, captureObject, recalibrate, brightness, lensPos):
    path = os.path.join(refDir, stations[selected], "STD.jpg")
    if recalibrate is True or os.path.isfile(path) is False:
        print("Load all parts. Press `C`` to continue")
        cv.waitKey(0)
        tempRef = captureObject.captureOne(path, brightness, lensPos) #Creating a stand-in initialisation picture
    else:
        tempRef = cv.imread(path)
    return tempRef

def errorSetup(selected, captureObject, processingObject, recalibrate, brightness, lensPos):
    with open(r'errors.json') as f:
        passref = json.load(f)

    if recalibrate:
        for i in range(10):
            testImg = captureObject.captureOne(os.path.join(errDir, stations[selected],"Test " + str(i) + ".jpg"), brightness, lensPos)
            time.sleep(0.5)
        # Taking a standard image
        ref = captureObject.captureOne(os.path.join(refDir, stations[selected],"STD.jpg"), brightness, lensPos)

        #Post-processing of captured images for MSE threshold creation
        passRef = [None] * len(stations[selected])

        for image in os.listdir(os.path.join(errDir, stations[selected])):
            path = os.path.join(errDir, stations[selected], image)
            img = cv.imread(path)

            processingObject.setTestImg(img)   
            error = processingObject.compareImage()
            passref = getPassRef(error, passRef)
            print(error, passref)
        
        passref[stations[selected]] = passref
        cv.destroyAllWindows()

    else:
        ref = cv.imread(os.path.join(refDir, stations[selected],"STD.jpg"))

    return ref, passref

#-----------------------------------------Main Loop-----------------------------------------#
def mainloop(selected, recalibrate):
    #-----------------------------------------Camera Initialisation-----------------------------------------#
    IP = IPEndpoint + selected
    IP = IPString + str(IP)

    initialisationObject = initialise(photosPath)
    photoDirectoryName, pipeline, camRgb, xoutRgb, xin, videoEnc, xoutStill = initialisationObject.initialise()

    for device in dai.Device.getAllAvailableDevices():
        print(f"{device.getMxId()} {device.state}")

    device_info = dai.DeviceInfo(IP)
    device_info.state = dai.XLinkDeviceState.X_LINK_BOOTLOADER
    device_info.protocol = dai.XLinkProtocol.X_LINK_TCP_IP

    #----------------------Camera Capture Initialisation---------------------#
    #This needs to be setup for multiple cameras
    with dai.Device(pipeline) as device:
        
        captureObject = imageCapture(device.getOutputQueue(name="rgb", maxSize=30, blocking=False), 
                                    device.getOutputQueue(name="still", maxSize=30, blocking=True), 
                                    device.getInputQueue(name="control"))

        brightness, lensPos = paramsSetup(selected, captureObject, recalibrate)
        masks = maskSetup(selected, captureObject, recalibrate, brightness, lensPos)
        tempRef = controlSetup(selected, captureObject, recalibrate, brightness, lensPos)
        
        processingObject = imageProcessing(masks, tempRef, tempRef, partsPerStation[selected]) #Initialisation of the processing object

        ref, passref = errorSetup(selected, captureObject, processingObject, recalibrate, brightness, lensPos)
        processingObject.setRefImg(ref)

    #-------------------------------------------------------------------------------------------#   
        while True:
            # capture a test image
            img = cv.imread(captureObject.autoCapture("Test.jpg", photoDirectoryName)) #returns a path that can be read. For some reason this prevents the return of a corrupted image
                
            processingObject.setTestImg(img)  
            # display the result on the frame
            frame = processingObject.displayResultPosition()
            # get the mse error
            error = processingObject.compareImage() 
            #Generates PASS/FAIL array
            prediction = MSEStabilization(error, passref, 4) 

            result = prediction.result()
            print(result)

            # transferToPLC("OP100", result)

            frame = cv.pyrDown(frame)
            frame = cv.pyrDown(frame)
            cv.imshow("errors", frame)
            cv.waitKey(1)

