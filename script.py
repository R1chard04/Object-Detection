import concurrent.futures
import time
from main import mainloop

# selected, recalibrate  = fromplc()
selected = [1]

if __name__ == '__main__':    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(mainloop, selected)
