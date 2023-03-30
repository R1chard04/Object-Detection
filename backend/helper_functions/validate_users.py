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
    return decoded_salt, hashed_password
 else:
  print(f"Sorry! But this password doesn't meet the requirements")

# this is a helper function that create a list of permissions for the users
def give_permission(permission_table, user_table, all_users_permission_name, admin_permission_name, db):
  # query to get all the users with no administration authorities
  all_users = user_table.query.filter_by(is_admin=False).all()

  # grant the access to view the homepage and start all the cameras
  for user in all_users:
    for all_users_permission in all_users_permission_name:
      permission = permission_table.query.filter_by(user_id=user.id, name=all_users_permission).first()
      if not permission:
        permission = permission_table(name=all_users_permission, user_id=user.id)
        db.session.add(permission)
  
  # query to get all the users with administration authorities
  admins = user_table.query.filter_by(is_admin=True).all()

  # grant the access to view the homepage, users_login_tracking, station_detail, station_settings, update_event, get_key, show_frame_params, change_settings, handle_click, get_click, station_mask_setup, create_mask, redo_mask, handle_redo_mask, station_errors_setup, create_errors, finish_setup, startPrograms
  for admin in admins:
    for admin_permission_list in admin_permission_name:
      admin_permission = permission_table.query.filter_by(user_id=admin.id, name=admin_permission_list).first()
      if not admin_permission:
        admin_permission = permission_table(name=admin_permission_list, user_id=admin.id)
        db.session.add(admin_permission)

  db.session.commit()