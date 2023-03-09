import concurrent.futures
import time
from main import mainloop

# selected, recalibrate  = fromplc()
selected = [0,1]
IP = ["169.254.1.201","169.254.1.202"]

if __name__ == '__main__':    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(mainloop,IP, selected)
