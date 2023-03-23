# middleware function to validate the token if the users will have the permission to visit the restricted resource
from functools import wraps
from flask import request, jsonify, current_app, redirect, url_for
import jwt
import pdb

def validate_token(permissions_list):
 def decorator(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
   # get the token from cookies
   token = request.cookies.get('token')
   if not token:
    # return the user to login page
    return redirect(url_for('login'))
   try:
    data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    for permission in permissions_list:
     if permission not in data['permissions']:
      return jsonify({'message' : 'Sorry! You are not authorized to view this page!'}), 403
   except:
    return jsonify({'message' : 'Token is invalid!'}), 401
   return f(*args, **kwargs)
  return decorated_function
 return decorator
