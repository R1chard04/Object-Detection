# This is a helper function that helps validate the users
from flask import Flask, session, redirect, url_for
import bcrypt
import pdb
from datetime import datetime, timedelta
 
# This is a helper function that helps validate the username to meet the requirements in the db before encrypted it
def validate_username(username) -> bool:
  if len(username) >= 8 and any(char in '@martinrea.com' for char in username) or any(char not in '@martinrea.com' for char in username):
    return True
  else:
    return False

# This is a helper function that helps validate the password to meet the requirements in the db before encrypted it
def validate_password(username, password, users_table) -> str:
 if password != username and len(password) >= 8 and any(char.isupper() for char in password) and any(char in '!@#$%^&*' for char in password):
  # generate the salt for hashed_password
  salt = bcrypt.gensalt()
  # hash the password using bcrypt hashing algorithm
  hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

  decoded_salt = salt.decode('utf-8')
  decoded_hashed_password = hashed_password.decode('utf-8')

  # query the password in database to make sure the password is unique
  password_taken = users_table.query.filter(
    users_table.password == decoded_hashed_password
  ).first() is not None

  # check if the password already in the database
  if password_taken:
    print(f'Sorry! This password already exist!')
    return 
  else:
    return hashed_password
 else:
  print(f"Sorry! But this password doesn't meet the requirements")

