from flask import Flask, jsonify, render_template, redirect, url_for, request, send_from_directory, session, flash, abort, make_response, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, MetaData, inspect
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from sqlalchemy.orm import scoped_session, sessionmaker
import bcrypt
import jwt
from pyignite import Client
import os
import sys
import websocket
import logging
import traceback
from flask_socketio import SocketIO, emit
import pdb
from flask_migrate import Migrate
import secrets
import depthai as dai
import requests
import asyncio
import json
import subprocess
import keyboard
from datetime import datetime, timedelta
import pytz

# import files
from database_model.models import db, Station, Users
from helper_functions.validate_users import validate_username, validate_password
from helper_functions.middleware_function import validate_token
from imageCalibrationClass import Recalibration, createPipeline

# read in the params.json file
with open(r'params.json') as f:
  partList = json.load(f)

# connect flask to the database
app = Flask(__name__)
api = Api(app)
socketio = SocketIO(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/martinrea.db'
app.config['SERVER_NAME'] = '127.0.0.1:5000'
app.config['APPLICATION_ROOT'] = '/'
app.config['PREFERRED_URL_SCHEME'] = 'http'
app.config['CORS_HEADERS'] = 'Content-Type'

# secret key
app.config['SECRET_KEY'] = secrets.token_hex(16)
CORS(app)

# generate a 32-character hexadecimal secret key for users to login their session
app.secret_key = secrets.token_hex(16)
migrate = Migrate(app, db)

# This is the helper function to asynchronously render the template while connecting to the devices
async def render_template_async(template_name, **kwargs):
  with app.app_context():
    template_string = render_template(template_name, **kwargs)
  return template_string

# Create SQLALCHEMY database object
def create_tables():
  with app.app_context():
    db.init_app(app)
    # create all the tables based on the models if they didn't exist yet
    with app.app_context():
      inspector = inspect(db.engine)
      if not inspector.has_table('station') and not inspector.has_table('users') and not inspector.has_table('permission'):
        db.create_all()

create_tables()

# insert into users table
def insert_users() -> None:
  with app.app_context():
    # create a list of non-encoded username and passwords
    name = 'Kent'
    usernames = 'kent.tran@martinrea.com'
    passwords = 'Kenttran2302$'
    name1 = 'Leo'
    usernames1 = 'leo.you@martinrea.com'
    passwords1 = 'Leoyou1234$'
    name2 = 'Jamie'
    usernames2 = 'jamie.yen@martinrea.com'
    passwords2 = 'Jamieyen12345$'
    # validate the username and password constraints before hashing it and put it into the database
    if validate_username(usernames) and validate_username(usernames1) and validate_username(usernames2):
      decoded_salt1, hashed_password = validate_password(usernames, passwords)
      decoded_salt2, hashed_password1 = validate_password(usernames1, passwords1)
      decoded_salt3, hashed_password2 = validate_password(usernames2, passwords2)
      # create an instance to insert rows into user table
      new_users = [
        Users(id=1, name=name, username=usernames, password=hashed_password, password_salt=decoded_salt1, is_admin=True),
        Users(id=2, name=name1, username=usernames1, password=hashed_password1, password_salt=decoded_salt2, is_admin=True),
        Users(id=3, name=name2, username=usernames2, password=hashed_password2, password_salt=decoded_salt3, is_admin=True)
      ]

    # insert the new user into the session
    for user in new_users:
      try:
        db.session.add(user)
        # commit the changes to the database
        db.session.commit()
        print(f"User {user.username} added successfully!")
      except:
        db.session.rollback()
        print(f"User {user.username} already exists in the database!")

insert_users()

# function to run all the cameras at once
def run_all_cameras():
  subprocess.Popen(['C:/Users/kent.tran/AppData/Local/Programs/Python/Python311/python.exe', 'cam1.py'])
  subprocess.Popen(['C:/Users/kent.tran/AppData/Local/Programs/Python/Python311/python.exe', 'cam2.py'])
  # subprocess.Popen(['C:/Users/kent.tran/AppData/Local/Programs/Python/Python311/python.exe', 'cam3.py'])


@socketio.on('key_event')
def handle_key_event(data):
  print(f'Received key event: {data}')

# include the path to javascript files
@app.route('/static-js/<path:filename>')
# add the static files path towards the javascript files
def serve_static_js(filename):
  root_dir = os.path.dirname(os.getcwd())
  return send_from_directory(os.path.join(root_dir, 'backend/static-js'), filename)

# include the path to css static files
@app.route('/static-css/<path:filename>')
# add the static files path towards the css files
def serve_static_css(filename):
  root_dir = os.path.dirname(os.getcwd())
  return send_from_directory(os.path.join(root_dir, 'backend/static-css'), filename)

# include the path to the photos files
@app.route('/Logos/<path:filename>')
# add the photos files path towards the html
def serve_static_photos(filename):
  root_dir = os.path.dirname(os.getcwd())
  return send_from_directory(os.path.join(root_dir, 'backend/Logos'), filename)

####################### HOMEPAGE ##########################
# define the list of permissions to visit this homepage
permission_list = ['can_view_homepage']
# render the homepage
@app.route('/bt1xx/home/')
@validate_token(permissions_list=permission_list)
def homepage():
  # decode the token and get the name of the user
  token = request.cookies.get('token')
  name = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['name']
  return render_template('home.html', user_name=name)
 

####################### STATION DETAILS #####################
# render the station details depends on the click event 
@app.route('/bt1xx/station/<int:station_number>/')
def station_detail(station_number):
  return render_template("station_details.html", station_number=station_number)

###################### STATION SETTINGS ######################
# render the station settings
@app.route('/bt1xx/station/<int:station_number>/settings/')
def station_settings(station_number):
  try:
    # enable the websockets to be ready to listen for events on the client side
    # establish_websocket(station_number=station_number)
    return render_template('station_settings.html', station_number=station_number)
  
  except Exception as e:
    print(f"Error:" + str(e))
    # catch the error of cannot perform a connection to the server
    return redirect(url_for('station_detail', station_number=station_number))

key_event = None  
###################### HANDLE POST REQUEST OF KEY EVENTS FROM OPENCV ###################
@app.route('/bt1xx/update-ui/', methods=['POST'])
def update_event():
    global key_event
    data = request.get_json()
    key_event = data.get('key')
    return jsonify({'success': True})

# register the endpoint
# update_key_event = GetKeyEvent()
@app.route('/bt1xx/get-updates/', methods=['GET'])
def get_key():
  global key_event
  return jsonify({'key': key_event})

###################### STATION SHOW FRAME ######################
@app.route('/bt1xx/paramSetup/showframe/station/<int:station_number>/', methods=['GET'])
def show_frame_params(station_number):
  # get the IP address of the connected device depends on the station number by calling the helper function
  # loop through the stations list to find the associate IP Address
  IP = partList['station' + str(station_number)]["IP"]
  name = partList['station' + str(station_number)]["name"]
  
  try:
    pipeline = createPipeline()
    print("here")
    device_info = dai.DeviceInfo(IP)
    device_info.state = dai.XLinkDeviceState.X_LINK_BOOTLOADER
    device_info.protocol = dai.XLinkProtocol.X_LINK_TCP_IP

    for device in dai.Device.getAllAvailableDevices():
      print(f"{device.getMxId()} {device.state}")

    with dai.Device(pipeline, device_info) as device:
      print(f"Ayoo! What's up!")
      global key_event
      recalibration = Recalibration(station='station' + str(station_number))
      
      
      # import paramSetup function to set the focal length and the brightness of the camera (camera settings)
      # brightness, lensPos = paramsSetup(station_number, captureObject, recalibrate=True, name=IP)
      recalibration.paramSetup(device)

      # overwrite the params.json
      this_station = 'station' + str(station_number)
      recalibration.updateJson(station=this_station)
    
    return redirect(url_for('setUpSuccessful', station_number=station_number))

  except:
    print(f"There is an error connecting to the device!")
  
  return redirect(url_for('station_detail', station_number=station_number))

###################### STATION CHANGE SETTINGS #################
# retrieve the data from the form
@app.route('/bt1xx/station/<int:station_number>/changeSettings', methods=['POST'])
def change_settings(station_number):
  # get the IP address of the connected device depends on the station number by calling the helper function
  IP = partList['station' + str(station_number)]["IP"]
  name = partList['station' + str(station_number)]["name"]

  if request.method == 'POST':
    try:
      # insert into the station detail table
      station_selected = station_number
      focal_length_settings = request.form['focal_length_setting_input']
      brightness_setting = request.form['brightness_setting_input']
      white_balance_lock_data = bool(request.form['white_balance_lock_input'])
      auto_exposure_lock_data = bool(request.form['auto_exposure_lock'])

      # create a list of new setting instance
      new_settings = [
        Station(name=name, IP_address = IP, station_number=station_selected, station_focalLength=focal_length_settings,station_brightness=brightness_setting,white_balance_lock=white_balance_lock_data, auto_exposure_lock = auto_exposure_lock_data)
      ]

      # add new setting into the station model
      for setting in new_settings:
        try:
          db.session.add(setting)
          # commit the change to the database
          db.session.commit()
          print(f"Setings for station {setting.station_number} added successfully!")
        except:
          db.session.rollback()
          print(f"Settings for station {setting.station_number} already existed!")

      result = Station.query.filter_by(station_number=station_selected, IP_address=IP, name=name).first()

      if result:
        print(f"Data has been inserted successfully!")
        
        return redirect(url_for('station_detail', station_number = station_number))
      
      else:
        print(f"Error inserting data into the database")
        pass

    # catch the error if the requirements are not met by the database
    except:
      db.session.rollback()
      print(f"There is an error while inserting the data into the database!")
      return redirect(url_for('station_settings', station_number=station_selected))
  
  # return render_template("successful.html", station_number=station_number)

click_event = False
###################### SENDING CLICK EVENT FOR MASK SETUP #######################
@app.route('/bt1xx/handle-click/', methods=['POST'])
def handle_click():
  global click_event
  data = request.get_json()
  click_event = data.get('btnClick')
  return jsonify({'success' : True})

##################### GETTING CLICK EVENT FOR MASK SETUP #######################
@app.route('/bt1xx/getclickevent/', methods=['GET'])
def get_click():
  global click_event
  return jsonify(
    {
      'btnClick' : click_event
    }
  )

####################### STATION MASKS SETTINGS ###############
# render the url for station mask setup instructions
@app.route('/bt1xx/station/<int:station_number>/masksetup')
def station_mask_setup(station_number):
  return render_template("station_masksetup.html", station_number=station_number)

# render the url for setting up the mask action
@app.route('/bt1xx/createmask/showframe/station/<int:station_number>/')
def create_mask(station_number):
  # call the function for connecting to the devices
  IP = partList['station' + str(station_number)]["IP"]
  name = partList['station' + str(station_number)]["name"]

  try:
    pipeline = createPipeline()

    device_info = dai.DeviceInfo(IP)
    device_info.state = dai.XLinkDeviceState.X_LINK_BOOTLOADER
    device_info.protocol = dai.XLinkProtocol.X_LINK_TCP_IP

    for device in dai.Device.getAllAvailableDevices():
      print(f"{device.getMxId()} {device.state}")

    with dai.Device(pipeline, device_info) as device:
      recalibration = Recalibration(station='station' + str(station_number))
      recalibration.upDateParams(station='station' + str(station_number))
      recalibration.maskSetup(device=device)

    return redirect(url_for('setUpSuccessful', station_number=station_number))

  except:
    print(f"Error connecting to the device!")
    return redirect(url_for('station_detail', station_number=station_number))

part = ['--select--']
# read in params.json file for the parts
with open('params.json', 'r') as f:
  partList = json.load(f)

################ REDO MASK URL ################
# this function will render the redo mask url
@app.route('/bt1xx/redo-mask/<int:station_number>')
def redo_mask(station_number):
  params = partList['station' + str(station_number)]
  # append the part list
  for i in params['parts']:
    part.append(i)

  return render_template('redo-mask.html', station_number=station_number, errors={}, mask_options=part)

############### HANDLE REDO MASK REQUEST ###########
# this function will handle the post request to redo the mask
@app.route('/bt1xx/handle-redo-mask/<int:station_number>/', methods=['POST'])
def handle_redo_mask(station_number):
  if request.method == 'POST':
    # call the function for connecting to the devices
    IP = partList['station' + str(station_number)]["IP"]
    name = partList['station' + str(station_number)]["name"]

    # get the form input
    part_chosen = request.form['mask_options_id']
    errors = {}

    # validate the form input
    if (part_chosen == '--select--'):
      errors['mask_options_id'] = f'You have to choose the part you want to redo the mask!'
      return render_template('redo-mask.html', station_number = station_number, errors=errors, mask_options=part)

    # get the index of the chosen part
    for i in range(len(part)):
      if(part_chosen == part[i]):
        part_chosen_index = i
        break
    part_chosen_index -= 2

  try:
    pipeline = createPipeline()

    device_info = dai.DeviceInfo(IP)
    device_info.state = dai.XLinkDeviceState.X_LINK_BOOTLOADER
    device_info.protocol = dai.XLinkProtocol.X_LINK_TCP_IP

    for device in dai.Device.getAllAvailableDevices():
      print(f"{device.getMxId()} {device.state}")

    with dai.Device(pipeline, device_info) as device:
      recalibration = Recalibration(station='station' + str(station_number))
      recalibration.upDateParams(station='station' + str(station_number))
      recalibration.redo_mask(device, part_chosen_index, part_chosen)
  
    return redirect(url_for('setUpSuccessful', station_number=station_number))

  except:
    print(f"Error connecting to the device!")
    return redirect(url_for('station_mask_setup', station_number=station_number))
    

############################### STATION ERRORS SETUP PAGE ######################
@app.route('/bt1xx/station/<int:station_number>/errorsetup')
def station_errors_setup(station_number):
  return render_template("station_errorsetup.html", station_number=station_number)

# render the url for setting up errors actions
@app.route('/bt1xx/errors/showframe/station/<int:station_number>')
def create_errors(station_number):
  # call the function to connect to a device
  IP = partList['station' + str(station_number)]["IP"]
  name = partList['station' + str(station_number)]["name"]

  try:
    pipeline = createPipeline()

    device_info = dai.DeviceInfo(IP)
    device_info.state = dai.XLinkDeviceState.X_LINK_BOOTLOADER
    device_info.protocol = dai.XLinkProtocol.X_LINK_TCP_IP

    for device in dai.Device.getAllAvailableDevices():
      print(f"{device.getMxId()} {device.state}")

    with dai.Device(pipeline, device_info) as device:
      # call a function to set up the errors
      recalibration = Recalibration(station='station' + str(station_number))
      recalibration.upDateParams(station='station' + str(station_number))
      recalibration.adjustCamera(device=device)
      recalibration.pressKeyCapture(device=device, path=recalibration.standardPath)
      recalibration.errorSetup(device=device)
      recalibration.updateJson(station='station' + str(station_number))

    return redirect(url_for('setUpSuccessful', station_number=station_number))

  except:
    print(f"Error connecting to the device!")
    return redirect(url_for('station_detail', station_number=station_number))

################ SUCCESSFUL PAGE AFTER SETTING UP #################
@app.route('/bt1xx/station_settings/<int:station_number>/successful/')
def setUpSuccessful(station_number):
  return render_template('successful.html', station_number=station_number)

################################# LOG IN PAGE #############################
# render the login page
@app.route('/bt1xx/login/')
def login():
  return render_template('login.html')

# authenticate the users login
@app.route('/bt1xx/authentication/', methods=['POST'])
def authentication():
  # if the user is not in session then abort the users to not authorized url
  if request.method == 'POST':
    try:
      username = request.form['username']
      password = request.form['password']
      # initiate an error dictionary to catch any error
      errors = {}

      # validate the user's input before sending as a POST request
      if len(username) == 0:
        errors['username'] = f"Please enter your username!"

      if len(password) == 0:
        errors['password'] = f"Please enter your password!"

      # query the user record from the database
      user = Users.query.filter_by(username=username, password=password).first()

      # validate the user credentials
      if user:
        # if the username and password are found in the database
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
          # User credentials are valid
          # Generate JWT token and store it in cookies
          # query the permissions list in the user table with the user id
          permissions = [permissions.name for permission in user.permissions]
          token = jwt.encode({'id' : user.id, 'name' : user.name,  'username' : user.username, 'exp': datetime.now(pytz.timezone('EST')) + timedelta(minutes=60), 'permissions' : permissions}, app.config['SECRET_KEY'], algorithm='HS256')

          # Store the token in a cookie
          response = make_response(redirect(url_for('homepage')))
          response.set_cookie('token', value=token, expires=datetime.now(pytz.timezone('EST')) + timedelta(minutes=60), httponly=True)

          # Redirect the user to the homepage and some restricted resources
          return response

    except ValueError:
      errors['username'] = f"Sorry! You are not authorized for this program!"
      return render_template('login.html', errors=errors)

# If the user chooses to log out the program
@app.route('/bt1xx/logout/')
def logout():
  session.pop('username', None)
  return redirect(url_for('login'))
  
############################## RUNNING ALL THE PROGRAMS ##############################
@app.route('/bt1xx/startallprograms/', methods=['GET'])
def startPrograms():
  # run all the cameras files
  run_all_cameras()
  return render_template('view.html')

if __name__ == '__main__':
 # connect to the websocket server to listening for events sent from localhost:5000
 app.run(debug=True)








