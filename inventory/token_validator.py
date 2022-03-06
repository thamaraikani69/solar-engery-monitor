# SWAMI KARUPPASWAMI THUNNAI

import time
import jwt
from functools import wraps
from flask import session, redirect,request,flash
from database.get_connection import get_connection


def get_inventory_token(inventory_id,token_user, password,access):
    inventory_secret = "jeeva$kani*vichu&69_7#%%^"
    expiry = time.time() + 259200
    token = {"inventory_id": inventory_id,"access":access,'token_user':token_user, "expiry": expiry}
    encoded_token = jwt.encode(token, key=password+inventory_secret)
    return encoded_token.decode("utf-8")


def inventory_token(_function):

  @wraps(_function)
  def wrapper_function(*args, **kwargs):

      token=None
      if 'x-access-token' in request.headers:
        token=request.headers['x-access-token']
        session['inventory_token']=token
      
      if "inventory_token" in session:
        token=session['inventory_token']

      if not token:
        flash('Token required')
        return redirect("/")
      
      token = session["inventory_token"]

      try:
          decoded_token = jwt.decode(token, verify=False)

      except jwt.DecodeError:
          flash('Invalid Token')
          return redirect("/")
      admin_id = decoded_token["inventory_id"]
      access = decoded_token["access"]

      expiry_time = decoded_token["expiry"]
      if time.time() > expiry_time:
        flash('Token timeout')
        return redirect("/")
      try:
          connection = get_connection()
          cursor = connection.cursor()
          if access=='admin':
            cursor.execute("SELECT password from admin where admin.id=%s limit 1", (admin_id ))
            result = cursor.fetchone()
          elif(access=='admin_group'):
            cursor.execute("SELECT password from admin_group where admin_group.id=%s limit 1", (admin_id ))
            result = cursor.fetchone()
          elif(access=='super_admin'):
            cursor.execute("SELECT password from super_admin where super_admin.id=%s limit 1", (admin_id ))
            result = cursor.fetchone()
          elif(access=='controller'):
            cursor.execute("SELECT password from controller where controller.id=%s limit 1", (admin_id ))
            result = cursor.fetchone()
          elif(access=='users'):
            cursor.execute("SELECT password from users where users.id=%s limit 1", (admin_id ))
            result = cursor.fetchone()
          else:
            result=None
          if result is None:
            flash('Invalid Token')
            return redirect("/")
          password_hash = result["password"]

      finally:
          cursor.close()
          connection.close()
      try:
          inventory_secret = "jeeva$kani*vichu&69_7#%%^"
          jwt.decode(token, key=password_hash+inventory_secret)
      except jwt.DecodeError:
          flash('Invalid Token')
          return redirect("/")
      
      return _function(*args, **kwargs)
  return wrapper_function

