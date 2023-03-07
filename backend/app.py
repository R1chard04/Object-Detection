from flask import Flask, jsonify, render_template, redirect, url_for, request, send_from_directory, session, flash
from sqlalchemy import create_engine, MetaData, inspect
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from sqlalchemy.orm import scoped_session, sessionmaker
from hashlib import sha256
from pyignite import Client
import os
import sys
import websocket
import traceback
from flask_socketio import SocketIO, emit
import pdb
from flask_migrate import Migrate
import secrets
import depthai as dai
import requests
import asyncio
import json

# import files
from database_model.models import db, Station, Users
from helper_functions.validate_users import validate_users, validate_username, validate_password, check_session_expiry
from main.cameraInitialisationClass import initialise
from main.imageCaptureClasses import imageCapture
from main.calibrations import Recalibration, createPipeline

# read in the params.json file
with open(r'main/params.json') as f:
  partList = json.load(f)

# connect flask to the database
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///martinrea.db'
app.config['SERVER_NAME'] = '127.0.0.1:5000'
app.config['APPLICATION_ROOT'] = '/'
app.config['PREFERRED_URL_SCHEME'] = 'http'

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
      if not inspector.has_table('station') and not inspector.has_table('users'):
        db.create_all()

create_tables()

# insert into users table
def insert_users() -> None:
  with app.app_context():
    # create a list of non-encoded username and passwords
    usernames = 'kent.tran@martinrea.com'
    passwords = 'Kenttran2302$'
    # validate the username and password constraints before hashing it and put it into the database
    if validate_username(usernames):
      hashed_password = validate_password(usernames, passwords)
      # create an instance to insert rows into user table
      new_users = [
        Users(id=1, username=usernames, password=hashed_password, is_admin=True)
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

# an object contains functions that listen for events on the client side then send them to the server side

def on_message(ws, message):
  print(message)
  ws.send(message)

def on_error(ws, error):
  print(error)

def on_close(ws, close_status_code, close_msg):
  print(f"Connection closed")

def on_open(ws):
  print(f"Connection established")

def establish_websocket(station_number):
  pdb.set_trace()
  try:
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(f"ws://127.0.0.1/bt1xx/station/" + str(station_number) + "/settings", on_message=on_message, on_error=on_error, on_close=on_close)

    ws.on_open = on_open
    ws.run_forever()
  except Exception as e:
    print(f"Error:", e)
    traceback.print_exc()

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

# include the path to the templates files
# @app.route('/outside_template/<path:filename>')
# # add the templates files towards the directory path
# def serve_static_templates(filename):
#   root_dir = os.path.dirname(os.getcwd())
#   return send_from_directory(os.path.join(root_dir, 'backend/outside_template'), filename)

####################### HOMEPAGE ##########################
# render the homepage
@app.route('/bt1xx/home/')
def homepage():
  if 'username' in session:
    return render_template("home.html")
  else:
    return redirect(url_for('login'))
 

####################### STATION DETAILS #####################
# render the station details depends on the click event 
@app.route('/bt1xx/station/<int:station_number>/')
def station_detail(station_number):
  if 'username' in session:
    return render_template("station_details.html", station_number=station_number)
  else:
    return redirect(url_for('login'))
  

###################### STATION SETTINGS ######################
# render the station settings:
@app.route('/bt1xx/station/<int:station_number>/settings')
def station_settings(station_number):
  # enable the websockets to be ready to listen for events on the client side
  establish_websocket(station_number=station_number)
  return render_template('station_settings.html', station_number=station_number)

###################### STATION SHOW FRAME ######################
@app.route('/bt1xx/paramSetup/showframe/<int:station_number>/')
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
      recalibration = Recalibration(station='station' + str(station_number))
      
      # import paramSetup function to set the focal length and the brightness of the camera (camera settings)
      # brightness, lensPos = paramsSetup(station_number, captureObject, recalibrate=True, name=IP)
      brightness, lensPos = recalibration.paramSetup(device)


  except:
    print(f"There is an error connecting to the device!")
  
  return redirect(url_for('station_detail', station_number=station_number))

###################### STATION CHANGE SETTINGS #################
# retrieve the data from the form
@app.route('/bt1xx/station/<int:station_number>/changeSettings', methods=['POST', 'GET'])
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
        
        # overwrite the params.json
        this_station = 'station' + str(station_selected)
        changeJson = Recalibration(station=this_station)
        changeJson.updateJson(station=this_station, new_brightness=int(brightness_setting), new_lensPos=int(focal_length_settings))
        
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
      recalibration.maskSetup(device=device)
    
    return redirect(url_for('station_detail', station_number = station_number))

  except:
    print(f"Error connecting to the device!")
    return redirect(url_for('station_detail', station_number=station_number))

################################# LOG IN PAGE #############################
# render the login page
@app.route('/bt1xx/login/')
def login():
  return render_template('login.html')

# authenticate the users login
@app.route('/bt1xx/authentication/', methods=['POST', 'GET'])
def authentication():
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

      # encryted the password when the user send it as a POST request
      hashed_password = sha256(password.encode('utf-8')).hexdigest()

      # Query the database for the user with the specified username and password
      user = Users.query.filter_by(username=username, password=hashed_password).first()

      # validate the users using the helper function
      if(validate_users(user_info=user, username=username)):
        # handle the post request if all the fields are validated
        return redirect(url_for('homepage'))

    except ValueError:
      errors['username'] = f"Sorry! You are not authorized for this program!"
      return render_template('login.html', errors=errors)

# If the user chooses to log out the program
@app.route('/bt1xx/logout/')
def logout():
  session.pop('username', None)
  return redirect(url_for('login'))

# Check session expiration
@app.before_request
def checkExpiration():
  if(check_session_expiry()):
    return redirect(url_for('login'))

if __name__ == '__main__':
 app.run(debug=True)
 # connect to the websocket server to listening for events sent from localhost:5000
 








