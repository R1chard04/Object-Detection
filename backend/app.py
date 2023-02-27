from flask import Flask, jsonify, render_template, redirect, url_for, request, send_from_directory
from sqlalchemy import create_engine, MetaData
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from pyignite import Client
from models import db
import os
import sys

# import the modules
# main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.append(main_directory)
# import main

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stations.db'
db.init_app(app)



# client = Client()
# client.connect('10.10.10.33', 8088)

# app.config['SQL_ALCHEMY_URI'] = 'ignite://10.10.10.33:8088/Hydroform'
# db = SQLAlchemy(app)

# # create the Ignite engine and connect to the server
# engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], module='sqlalchemy_ignite.pyignite')
# engine.connect()

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

####################### HOMEPAGE ##########################
# render the homepage
@app.route('/bt1xx/home/')
def homepage():
 return render_template("home.html")

####################### STATION DETAILS #####################
# render the station details depends on the click event 
@app.route('/bt1xx/station/<int:station_number>/')
def station_detail(station_number):
  return render_template("station_details.html", station_number=station_number)

###################### STATION SETTINGS ######################
# render the station settings:
@app.route('/bt1xx/station/<int:station_number>/settings')
def station_settings(station_number):
  return render_template("station_settings.html", station_number=station_number)

###################### STATION CHANGE SETTINGS #################
# retrieve the data from the form
@app.route('/bt1xx/station/<int:station_number>/changeSettings', methods=['POST'])
def change_settings(station_number):
  station_selected = station_number
  focal_length_settings = request.form['focal_length_setting_input']
  brightness_setting = request.form['brightness_setting_input']

  # # import capture function from imageCaptureClasses
  # captureObject = main.captureObject

  # # import paramSetup function to set the focal length and the brightness of the camera (camera settings)
  # result = main.paramsSetup(station_selected, captureObject, recalibrate=True)

  return redirect(url_for('station_detail', station_number = station_number))
  # return render_template("successful.html", station_number=station_number)

if __name__ == '__main__':
 app.run(debug=True)








