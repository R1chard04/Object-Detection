# This is a helper function that helps validate the users
from flask import Flask, session, redirect, url_for
from hashlib import sha256
import pdb
from datetime import datetime, timedelta

def validate_users(user_info, username) -> bool:
 # if the user's login fields are all validated (user's information is in the database)
 if user_info:
  session['username'] = username
  session['expiry_time'] = (datetime.now() + timedelta(minutes=15)).isoformat()
  return True
 # if the users failed to login, this might be the users are not authorized for this program or they didn't enter your username and password
 else:
  raise ValueError(f"This user is not authorized!")
 
# This is a helper function that helps validate the username to meet the requirements in the db before encrypted it
def validate_username(username) -> bool:
  if len(username) >= 8 and any(char in '@martinrea.com' for char in username) or any(char not in '@martinrea.com' for char in username):
    return True
  else:
    return False

# This is a helper function that helps validate the password to meet the requirements in the db before encrypted it
def validate_password(username, password) -> str:
 if password != username and len(password) >= 8 and any(char.isupper() for char in password) and any(char in '!@#$%^&*' for char in password):
  hashed_password = sha256(password.encode('utf-8')).hexdigest()
  return hashed_password
 else:
  print(f"Sorry! But this password doesn't meet the requirements")

# This is a helper function that pop out the user after 15 minutes of inactivity
def check_session_expiry() -> bool:
  # Check if user is logged in and session has not expired
  if 'username' in session and 'expiry_time' in session:
    expiry_time = datetime.fromisoformat(session['expiry_time'])
    if expiry_time < datetime.now():
      # Session has expired, log out the user
      session.pop('username', None)
      session.pop('expiry_time', None)
      return True
    else:
      # Update expiry time
      session['expiry_time'] = (datetime.now() + timedelta(minutes=15)).isoformat()
      return False