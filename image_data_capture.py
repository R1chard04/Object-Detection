import depthai as dai
import cv2 as cv
import time
import contextlib
import threading
import os
from queue import Queue

def createPipeline():
    # Create pipeline
    pipeline = dai.Pipeline()

    # Define sources and output
    camRgb = pipeline.create(dai.node.ColorCamera)
    
    xoutVid = pipeline.create(dai.node.XLinkOut)
    xoutVid.setStreamName('vid')

    # Properties
    camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
    camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)

    # Linking
    camRgb.video.link(xoutVid.input)

    return pipeline

def captureImage(videoQueue):
    try:
        vidQueueRetrieval = videoQueue.get()
        frame = vidQueueRetrieval.getCvFrame()

        assert frame is not None 

        return frame
    
    except Exception as err:
        print('error:', err)

        return None

run = True

def worker(deviceInfo, stack, queue):
    openVinoVer = dai.OpenVINO.Version.VERSION_2022_1
    device: dai.Device = stack.enter_context(dai.Device(openVinoVer, deviceInfo, False))
    
    device.startPipeline(createPipeline())
    q = device.getOutputQueue(name="vid", maxSize=1, blocking=False)

    while run:
        frame = captureImage(q)
        queue.put(frame)
    
    print("closing thread")

def main():
    global run

    # modify this dict to manipulate which camera(s) to collect data from
    deviceInfos = {
        'station100': dai.DeviceInfo('14442C1021C7E7D600'),
        'station120': dai.DeviceInfo('14442C100132E7D600')
    }

    if not os.path.exists('raw_data'):
        os.makedirs('raw_data')

    with contextlib.ExitStack() as stack:
        threads = []
        imageQueues = {}

        for stationName, device in deviceInfos.items():
            time.sleep(1)

            q = Queue(1)
            thread = threading.Thread(target = worker, args = (device, stack, q))
            thread.start()
            threads.append(thread)
            imageQueues[stationName] = q

            print("thread created for device", stationName)

            if not os.path.exists(f'raw_data/{stationName}'):
                os.makedirs(f'raw_data/{stationName}')

        index = 1

        while True:
            if not imageQueues.items():
                print("no items")

            for stationName, q in imageQueues.items():
                currFrame = q.get(block=True)
                cv.imshow(stationName, cv.pyrDown(currFrame))

                if cv.waitKey(1) == ord('q'):
                    run = False
                    break

                cv.imwrite(f'raw_data/{stationName}/{int(time.time() - 1688586167)}--{index}.jpg', currFrame)
                
            index += 1
            time.sleep(5)

        for thread in threads:
            thread.join()

    print("Devices closed")

if __name__ == "__main__":
    main()