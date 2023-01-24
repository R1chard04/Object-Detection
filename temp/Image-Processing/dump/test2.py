import datetime
import time

while True:       
    now = str(datetime.datetime.now())
    now = round(float(((now.replace("-","")).replace(" ","")).replace(":","")))

    time.sleep(1)
    print(now)
