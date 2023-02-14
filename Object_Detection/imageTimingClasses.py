import datetime
import random
import time

class imageTiming:
    def __init__(self, responses):
        self.responses = responses
        self.timestamps = [datetime.datetime.now() for _ in range(len(responses))]

    def record(self):
        # Create a list to store the recording results along with the time elapsed
        results = []
        
        prev_timestamp = datetime.datetime.now()
        for i in range(len(self.responses)):
            wait = random.uniform(1, 5)
            time.sleep(wait)
            curr_timestamp = datetime.datetime.now()
            time_elapsed = (curr_timestamp - prev_timestamp).total_seconds()
            result = {
                "time_elapsed": time_elapsed,
                "response": "pass" if int(self.responses[i]) == 1 else "fail"
            }

            results.append(result)
            prev_timestamp = curr_timestamp
        
        with open('recording_results.txt', 'a') as f:
            for i in range(len(self.responses)):
                f.write(str(self.timestamps[i]) + ',' + str(int(self.responses[i])) + ',' + str(results[i]["time_elapsed"]) + '\n')
        
        return results
    
    
responses = [1, 1, 0]
# Create an instance of the class
timing = imageTiming(responses)
results = timing.record()
print(results)