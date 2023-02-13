import datetime
import numpy as np
from sklearn.linear_model import LinearRegression
import random
import time

#Records timing of fail/pass to help determine which station is over/under in producing parts.
#Requires completion of prediction classes array to become fully implemented. Works on made up arrays.

class Prediction:
    def __init__(self, errors, responses):
        self.errors = errors
        self.responses = responses
        self.timestamps = [datetime.datetime.now() for _ in range(len(errors))]
    
    def trend(self):
        # Create the linear regression model
        myRegr = LinearRegression()

        # Train the model using the training data
        myRegr.fit(np.array(self.errors).reshape(-1, 1), np.array(self.responses).reshape(-1, 1))
        
        return myRegr

    def prediction(self, new_errors, myRegr) -> list:
        # Make predictions for a new set of errors
        predictions = myRegr.predict(new_errors)

        # Convert the predictions to binary (pass/fail)
        predictions = np.round(predictions)
        
        # Create a list to store the prediction results along with the time elapsed
        results = []
        
        prev_timestamp = datetime.datetime.now()
        for i in range(len(predictions)):
            curr_timestamp = datetime.datetime.now()
            
            time_elapsed = (curr_timestamp - prev_timestamp).total_seconds()
            result = {
                "time_elapsed": time_elapsed,
                "prediction": "pass" if int(predictions[i]) == 1 else "fail"
            }

            results.append(result)
            prev_timestamp = curr_timestamp
        
        with open('prediction_results.txt', 'a') as f:
            for i in range(len(predictions)):
                f.write(str(self.timestamps[i]) + ',' + str(int(predictions[i])) + ',' + str(results[i]["time_elapsed"]) + '\n')
        
        return results

# Generate errors and responses data
np.random.seed(0)
errors = np.random.normal(0, 1, 10)
responses = np.round(errors + np.random.normal(0, 0.1, 10))
new_errors = np.array([1, 1, 0, 0, 1]).reshape(-1, 1)

# Create an instance of the Prediction class using the generated data
prediction_model = Prediction(errors, responses)

# Get the regression model from the trend method
myRegr = prediction_model.trend()

# Call the prediction method to make predictions and save the results to a file
results = []
for i in range(new_errors.shape[0]):
    # Wait for a random amount of time before making the prediction
    time.sleep(random.uniform(0, 5))
    result = prediction_model.prediction(new_errors[i].reshape(-1, 1), myRegr)
    results.append(result)
    print(results)