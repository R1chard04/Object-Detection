import json
import depthai as dai
import cv2 as cv
import time
from imageMaskGeneration import createMask
from imageProcessingClasses import imageProcessing
from imagePredictionClass import MSEStabilization, getPassRef
import pdb
import os
import keyboard
import websocket
import requests
import pdb

def createPipeline():
    pipeline = dai.Pipeline()
    # This might improve reducing the latency on some systems
    pipeline.setXLinkChunkSize(0)

    # Define source and output
    camRgb = pipeline.create(dai.node.ColorCamera)
    camRgb.setFps(3)
    camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
    camRgb.setPreviewSize(1920, 1080)

    xout = pipeline.create(dai.node.XLinkOut)
    xout.setStreamName("out")
    xin = pipeline.create(dai.node.XLinkIn)
    xin.setStreamName("control")
    xin.out.link(camRgb.inputControl)
    camRgb.isp.link(xout.input)
    return pipeline

def clamp(num, v0, v1):
    return max(v0, min(num, v1))

# set up the mask, control and errors
class Recalibration:
    def __init__(self, station) -> None:
        with open (r'params.json') as f:
              partList = json.load(f)
              
        # select which station to use here
        self.station = station
        params = partList[station]
        self.passref = params["passref"]
        self.brightness = params["brightness"]
        self.lensPos = params["lensPos"]
        self.parts = params["parts"]
        self.IP = params["IP"]
        self.name = params["name"]
        self.maskPaths = params["masks"]
        self.refPaths = params["refs"]
        self.colPaths = params ["cols"]
        self.standardPath = params["standard"]
        self.testPath = params["test"]
    
    # this function setup params for stations
    def paramSetup(self, device, stationNumber):
        q = device.getOutputQueue(name="out")
        qControl = device.getInputQueue(name="control")
        
        # the url server to send the frame of the camera to
        url = 'http://127.0.0.1:5000/bt1xx/post-frames/' + stationNumber + '/'
        headers = {
            'Content-Type' : 'image/jpeg'
        }

        # send the GET request to '/bt1xx/get-updates/' url server to get the key event
        key_url = 'http://127.0.0.1:5000/bt1xx/get-updates/'
        # send the POST request to '/bt1xx/update-ui/' url server to change the frame and key event after the user pressed on the client side
        update_key_url = 'http://127.0.0.1:5000/bt1xx/update-ui/'

        while True:
            frame = q.get().getCvFrame()
            frame = cv.pyrDown(frame)

            cv.imshow(self.station, frame)
            
            key_code = cv.waitKey(1)


            # response = requests.get(url)

            # if response.status_code == 200:
            #     new_key = response.json().get('key')
            #     # convert new_key to its corresponding OpenCV key code
            #     if new_key is not None:
            #         key_code = cv.waitKeyEx(new_key)
            #     else:
            #         key_code = ord(new_key)

            # send the POST request along with the key pressed to the server
            # try:
            #     if key > 0 and key < 0x10FFFF:
            #         url = 'http://127.0.0.1:5000/bt1xx/update-ui/'
            #         data = {'key' : chr(key)}
            #         print(data)
            #         response = requests.post(url, json=data)
            #         time.sleep(10)
            #         if response.status_code != 200:
            #             print(f"Error sending key: {response.status_code}")

            # except requests.exceptions.RequestException as e:
            #     print(f"Error while sending key data: {e}")     
                # check if the key_code is valid
                # if key_code != -1:
            # brightness adjustment
            if key_code in [ord(','), ord('.')]:
                if key_code == ord(','):  
                    self.lensPos -= 2
                elif key_code == ord('.'):
                    self.lensPos += 2
                self.lensPos = clamp(self.lensPos, 0, 255)
                print("Setting manual focus, lens position: ", self.lensPos)
                ctrl = dai.CameraControl()
                ctrl.setManualFocus(self.lensPos)
                qControl.send(ctrl)
                
            elif key_code in [ord('k'), ord('l')]:
                if key_code == ord('k'):
                    self.brightness -= 1
                elif key_code == ord('l'):
                    self.brightness += 1
                self.brightness = clamp(self.brightness, -10, 10)
                print("Brightness:", self.brightness)
                ctrl = dai.CameraControl()
                ctrl.setBrightness(self.brightness)
                qControl.send(ctrl) 
            
            if key_code == ord('q'):
                return
        # else:
        #     pass
    
        # else:
        #     return "Error while getting key events with status code: " + str(response.status_code)

            # convert the frame to JPEG format
            _, buffer = cv.imencode('.jpg', frame)
            # send the frame to the server, perform the request to the server to see if the key event has been detected
            key_response = requests.get(key_url)
            if key_response.status_code == 200 and key_response.json() is not None:
                change_frame = key_response.json().get('change_frame')
                if change_frame == True:
                    response = requests.post(url, data=buffer.tobytes(), headers=headers)
                    if response.status_code == 200:
                        print('Frame uploaded successfully')
                        new_response = requests.post(update_key_url, json={
                            'change_frame' : False,
                            'key' : 'a'
                        })
                        if new_response.status_code == 200:
                            change_frame = False
                    else: 
                        print('Error uploading frame:', response.status_code)
            
    
    # this function setup masks for station
    def maskSetup(self, device):
        q = device.getOutputQueue(name="out")
        i = 0           
        
        while i < len(self.parts) :
        
            url = 'http://127.0.0.1:5000/bt1xx/getclickevent/'

            print("load"+ self.parts[i] + "silver part and press c to capture")
            while True:
                imgSil = q.get().getCvFrame()
                
                # send the GET request to '/bt1xx/getclickevent/' url server to get the response
                response = requests.get(url)

                if response.status_code == 200:
                    click = response.json().get('btnClick')

                key = cv.waitKey(1)
                if key == ord('c') and click == True:
                    cv.imwrite(self.refPaths[i], imgSil)
                    cv.destroyAllWindows()
                    break
                imgSil = cv.pyrDown(imgSil)
                cv.imshow("results", imgSil)
                
            print("load"+ self.parts[i] + "colour part and press c to capture")
            while True:
                imgCol = q.get().getCvFrame()

                # send the GET request to '/bt1xx/getclickevent/' url server to get the response
                response = requests.get(url)

                if response.status_code == 200:
                    click = response.json().get('btnClick')

                key = cv.waitKey(1)
                if key == ord('c') and click == True:
                    cv.imwrite(self.colPaths[i], imgCol)
                    cv.destroyAllWindows()
                    break
                imgCol = cv.pyrDown(imgCol)
                cv.imshow("results", imgCol)
            print("Creating a mask, this may take a minute")
            if createMask(imgSil, imgCol, self.maskPaths[i]):
                i += 1
                print("Mask generated")
            else:
                print(f"Mask is redoing!")
        
        print("all masks are done")
        return
    
    # function receive the redo mask command
    def redo_mask(self, device, part_number, part): # part number is the associate index of the part in the array
        q = device.getOutputQueue(name="out")
        i = 0

        url = 'http://127.0.0.1:5000/bt1xx/getclickevent/'
        
        # load the silver part
        print("Load" + part + "silver part and press C to capture")
        while True:
            imgSil = q.get().getCvFrame()

            # send the GET request to '/bt1xx/getclickevent/' url server to get the response
            response = requests.get(url)

            if response.status_code == 200:
                click = response.json().get('btnClick')

            key = cv.waitKey(1)
            if key == ord('c') and click == True:
                cv.imwrite(self.refPaths[part_number], imgSil)
                cv.destroyAllWindows()
                break
            imgSil = cv.pyrDown(imgSil)
            cv.imshow("results", imgSil)

        print("Load" + part + "colour part and press C to capture")
        while True:
            imgCol = q.get().getCvFrame()

            # send the GET request to '/bt1xx/getclickevent/' url server to get the response
            response = requests.get(url)

            if response.status_code == 200:
                click = response.json().get('btnClick')

            key = cv.waitKey(1)
            if key == ord('c') and click == True:
                cv.imwrite(self.colPaths[part_number], imgCol)
                cv.destroyAllWindows()
                break
            imgCol = cv.pyrDown(imgCol)
            cv.imshow("results", imgCol)
        print("Creating a mask, this may take a minute")
        if createMask(imgSil, imgCol, self.maskPaths[part_number]):
            print("Mask generated")
    
        print(f"Redoing mask for {part} is done")
        return
    
    # this method read all the parameters from the json again                
    def upDateParams(self, station):

        with open (r'params.json', 'r') as f:
              partList = json.load(f)
              
        # select which station to use here
        params = partList[station]
        self.brightness = params["brightness"]
        self.lensPos = params["lensPos"]
        return
    
    # this function updates all the values in the json
    def updateJson(self, station):
        with open(r'params.json', 'r') as f:
            partList = json.load(f)
        
        # change the settings in json
        partList[station]["brightness"] = self.brightness
        partList[station]["lensPos"] = self.lensPos
        partList[station]["passref"] = self.passref
        
        with open('params.json', 'w') as f:
            json.dump(partList, f, indent = 4)

        print(f"Json updated")
    
    # this function set up the passref for the parts  
    def errorSetup(self, device):
        q = device.getOutputQueue(name="out")
        processingObject = imageProcessing(self.station)
        self.passref = [0]*len(self.parts)
        
        print("setting up pass references")
        for i in range(50):
            imgFrame = q.get().getCvFrame()
            processingObject.setTestImg(imgFrame)
            error = processingObject.compareImage()
            self.passref = getPassRef(error, self.passref)  
        return
    
    # this function should be called when the camera get turned on
    # it will adjust the camera to the brightness and lensPos 
    def adjustCamera(self, device):
        
        q = device.getOutputQueue(name="out")
        qControl = device.getInputQueue(name="control")
        
        print("Setting manual focus, lens position: ", self.lensPos)
        ctrl = dai.CameraControl()
        ctrl.setManualFocus(self.lensPos)
        qControl.send(ctrl)
        
        print("Brightness:", self.brightness)
        ctrl = dai.CameraControl()
        ctrl.setBrightness(self.brightness)
        qControl.send(ctrl)
        
        startTime = time.time()
        while ((time.time()-startTime) < 10):
            imgFrame = q.get().getCvFrame()
            imgFrame = cv.pyrDown(imgFrame)
            cv.imshow("adjusting the camera", imgFrame)
            cv.waitKey(1)
        
        # auto white balance lock
        print("auto white balance lock")
        ctrl = dai.CameraControl()
        ctrl.setAutoWhiteBalanceLock(True)
        qControl.send(ctrl)

        # auto exposure lock
        print("auto exposure lock")
        ctrl = dai.CameraControl()
        ctrl.setAutoExposureLock(True)
        qControl.send(ctrl)
        
        cv.destroyAllWindows()
        return
        
    # this function capture an image and return it    
    def capture(self, device):
        q = device.getOutputQueue(name="out")
        imgFrame = q.get().getCvFrame()
        return imgFrame

    # this function stream the frames until the user press c to capture an image
    def pressKeyCapture(self, device, path):
        q = device.getOutputQueue(name="out")
        
        while True:
            imgFrame = q.get().getCvFrame()
            key = cv.waitKey(1)
            if key == ord('c'):
                cv.imwrite(path, imgFrame)
                cv.destroyAllWindows()
                break
            
            imgFrame = cv.pyrDown(imgFrame)
            cv.imshow("results", imgFrame)
            