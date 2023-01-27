import time
import threading
from functools import wraps
# # seconds passed since epoch
# seconds = 1672215379.5045543

# # convert the time in seconds since the epoch to a readable format
# local_time = time.ctime(seconds)

# print("Local time:", local_time)

# preTime = time.time() +1
# print(time.time())
# print(preTime)

while True:
    # preTime = time.time() +1
    # if time.time() > preTime:
    #     print("heyhey")
    print(time.time()%1//0.2)

# print(0.43243//0.1)

# def delay(delay=0.): 
#     """ 
#     Decorator delaying the execution of a function for a while. 
#     """ 
#     def wrap(f): 
#         @wraps(f) 
#         def delayed(*args, **kwargs): 
#             timer = threading.Timer(delay, f, args=args, kwargs=kwargs) 
#             timer.start() 
#         return delayed 
#     return wrap 

# from utils import delay 
 
# @delay(3.0) 
# def my_func(arg1, arg2): 
#     print arg1, arg2 
 
# if __name__ == '__main__': 
#     my_func('Hello', 'world') 