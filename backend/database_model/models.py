# this file is to create a model in the database using SQLALCHEMY
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import CheckConstraint
from datetime import datetime
from sqlalchemy import inspect

db = SQLAlchemy()

# Define a station model for station table
class Station(db.Model):
  __tablename__ = 'station'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  station_number = db.Column(db.Integer, nullable=False)
  station_focalLength = db.Column(db.Integer, nullable=False)
  station_brightness = db.Column(db.Integer, nullable=False)
  white_balance_lock = db.Column(db.Boolean, nullable=False)
  auto_exposure_lock = db.Column(db.Boolean, nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

  # adding arguments constraints for station table
  __table_args__ = (
    CheckConstraint('station_focalLength >= 0 AND station_focalLength <= 200', name='focalLengthCheck'),
    CheckConstraint('station_brightness >= -100 AND station_brightness <= 100', name='brightnessCheck')
  )

  def __repr__(self) -> str:
    return '<Setting for Station %r>' % self.station_number

# Define a users model for users table
class Users(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  username = db.Column(db.String(100), nullable=False, unique=True) # check constraint for username
  password = db.Column(db.String(100), nullable=False, unique=True) # check constraint for password
  is_admin = db.Column(db.Boolean, nullable=False) # check if the user is admin or not
  created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
  updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

  # adding arguments constraints for users table
  __table_args__ = (
      CheckConstraint("(LENGTH(username) >= 8 AND username NOT LIKE '%@martinrea.com') OR (username LIKE '%@martinrea.com')", name='username_check'),
      CheckConstraint("LENGTH(password) >= 8 AND password != username", name='password_check'),
      CheckConstraint("password REGEXP '[A-Z]' AND password REGEXP '[/|@|#|\$|\%|\^|\&|\*]' AND password REGEXP '[0-9]'", name='password_complexity_check'),
      {'sqlite_autoincrement': True}
  )

  def __repr__(self) -> str:
    return '<User %r>' % self.username


