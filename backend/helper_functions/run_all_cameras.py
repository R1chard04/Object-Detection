import subprocess
import requests
import json

# function to run all the cameras at once
def run_all_cameras():
  # run all the available files that triggered the cameras
  try:
    subprocess.Popen(['C:/Users/kent.tran/AppData/Local/Programs/Python/Python311/python.exe', 'cam1.py'])
    subprocess.Popen(['C:/Users/kent.tran/AppData/Local/Programs/Python/Python311/python.exe', 'cam2.py'])

    # send a GET request to the server to send the number of cameras are running
    request_headers = ({
      'Content-Type' : 'application/json'
    })

    request_data = ({
      'cameras' : 2 
    })

    request_json = json.dumps(request_data)
    headers_json = json.dumps(request_headers)
    response = requests.get(url='http://127.0.0.1:5000/bt1xx/startallprograms/', headers=headers_json, data=request_json)

    if response.status_code == 200:
      print(f'Request has been sent to the server successfully')
  
  # catch the error
  except Exception as error:
    response_data = ({
      'message' : f'There is an error with running all the cameras: {error}',
      'status_code' : 500
    })
    response_json = json.dumps(response_data)
    # send the request along with the data to the server
    response = requests.get(url='http://127.0.0.1:5000/bt1xx/startallprograms/', data=response_json)
    return response