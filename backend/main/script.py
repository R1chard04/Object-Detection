import concurrent.futures
import time
from main import mainloop
import multiprocessing
# selected, recalibrate  = fromplc()
selected = [0,1]

if __name__ == '__main__':    

    process1 = multiprocessing.Process(target=mainloop, args = (0,))
    process2 = multiprocessing.Process(target=mainloop, args = (1,))
    process3 = multiprocessing.Process(target=mainloop, args = (2,))

    # Start the processes
    process1.start()
    process2.start()
    process3.start()
    
    # Wait for the processes to finish
    process1.join()
    process2.join()
    process3.join()
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         executor.map(mainloop, selected)
