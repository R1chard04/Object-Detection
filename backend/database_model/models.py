# this file is to create a model in the database using SQLALCHEMY
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import CheckConstraint
from datetime import datetime
from sqlalchemy import inspect
import pdb
import pytz

db = SQLAlchemy()

# Define a station model for station table
class Station(db.Model):
  __tablename__ = 'stations_settings'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(100), nullable=False)
  IP_address = db.Column(db.Integer, nullable=False)
  station_number = db.Column(db.Integer, nullable=False)
  station_focalLength = db.Column(db.Integer, nullable=False)
  station_brightness = db.Column(db.Integer, nullable=False)
  white_balance_lock = db.Column(db.Boolean, nullable=False)
  auto_exposure_lock = db.Column(db.Boolean, nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('EST')), nullable=False)
  updated_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('EST')), onupdate=datetime.utcnow, nullable=False)
  # adding arguments constraints for station table
  __table_args__ = (
    CheckConstraint('station_focalLength >= 0 AND station_focalLength <= 200', name='focalLengthCheck'),
    CheckConstraint('station_brightness >= -100 AND station_brightness <= 100', name='brightnessCheck')
  )

  def __repr__(self) -> str:
    return '<Setting for Station %r>' % self.station_number

# Define a users model for users table
class Users(db.Model):
  __tablename__ = 'admin_users'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(50), nullable=False, unique=True)
  username = db.Column(db.String(100), nullable=False, unique=True) # check constraint for username
  password = db.Column(db.String(100), nullable=False, unique=True) # check constraint for password
  password_salt = db.Column(db.String(100), nullable=False, unique=True) # salt password for bcrypt hashing 
  is_admin = db.Column(db.Boolean, nullable=False) # check if the user is admin or not
  created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('EST')), nullable=False)
  updated_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('EST')), onupdate=datetime.utcnow, nullable=False)
  permissions = db.relationship('Permission', backref='users', lazy=True)

  # adding arguments constraints for users table
  __table_args__ = (
  #   pdb.set_trace(),
   CheckConstraint("(LENGTH(username) >= 8 AND username NOT LIKE '%@martinrea.com') OR (username LIKE '%@martinrea.com')", name='username_check'),
    # CheckConstraint("LENGTH(password) >= 8 AND password != username", name='password_check'),
    # CheckConstraint("password REGEXP '[A-Z]' AND password REGEXP '[/|@|#|\$|\%|\^|\&|\*]' AND password REGEXP '[0-9]'", name='password_complexity_check'),
    # {'sqlite_autoincrement': True}
  )

  def __repr__(self) -> str:
    return '<User %r>' % self.username % self.name
  
# Define a permission table to have one-to-many relationship to the user table
class Permission(db.Model):
  __tablename__ = 'admin_permissions'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
  name = db.Column(db.String(1000), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('admin_users.id'), nullable=False)

  def __repr__(self) -> str:
    return '<Permission %r>' % self.id % self.name

# create one model for storing timestamp
class TimingStation100(db.Model):
  __tablename__ = 'Station100_timing'

  id = db.Column(db.Integer,nullable=False, primary_key=True, autoincrement=True)
  TopPart = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
  LeftPart = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
  BottomPart = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
  RightPart = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
  ClampState = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('EST')), nullable=False)
  updated_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('EST')), onupdate=datetime.utcnow, nullable=False)
  
  def __repr__(self) -> str:
    return '<Station100_timing %r>' % self.updated_at

class TimingStation120(db.Model):
  __tablename__ = 'Station120_timing'

  id = db.Column(db.Integer,nullable=False, primary_key=True, autoincrement=True)
  TopRightPart = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
  TopLeftPart = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
  LeftPart = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
  BottomLeftPart = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
  BottomRightPart = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
  RightPart = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
  clampState = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('EST')), nullable=False)
  updated_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('EST')), onupdate=datetime.utcnow, nullable=False)

  def __repr__(self) -> str:
    return '<Station120_timing %r>' % self.updated_at
  

  

