import subprocess
import requests
import json
import pdb

# function to run all the cameras at once
def run_all_cameras():
  # run all the available files that triggered the cameras
  subprocess.Popen(['C:/Users/kent.tran/AppData/Local/Programs/Python/Python311/python.exe', 'cam1.py'])
  subprocess.Popen(['C:/Users/kent.tran/AppData/Local/Programs/Python/Python311/python.exe', 'cam2.py'])
