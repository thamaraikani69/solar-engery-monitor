# SWAMI KARUPPASWAMI THUNNAI
import jwt
import hashlib
import datetime
dates=datetime.datetime.now()
date=dates.date()
import requests
import json

from database.get_connection import get_connection

from flask import session,request,flash

salt='jeeva$kani*vichu&69'  
salt=hashlib.sha512(salt.encode("utf-8")).hexdigest()

def rights():
    token=None
    if 'x-access-token' in request.headers:
        token=request.headers['x-access-token']
        session['inventory_token']=token

    if ("inventory_token" in session):
        token=session['inventory_token']
    if not token:
        return None
    else:
        token=session["inventory_token"]
        decoded_token=jwt.decode(token,verify=False)
        if ("inventory_id" not in decoded_token) | ("token_user" not in decoded_token) | ("access" not in decoded_token):
            return None
        # print('decoded_token',decoded_token)
        admin_id=decoded_token["inventory_id"]
        token_user=decoded_token["token_user"]
        access= decoded_token['access']

        username_hash=token_user
        
        connection=get_connection()
        cursor=connection.cursor()

        if access=="admin":
            cursor.execute("SELECT id,username from admin where admin.id=%s",admin_id)
            right=cursor.fetchone()
        elif access=="admin_group":
            cursor.execute("SELECT id,username from admin_group where admin_group.id=%s",admin_id)
            right=cursor.fetchone()
        elif access=="super_admin":
            cursor.execute("SELECT id,username from super_admin where super_admin.id=%s",admin_id)
            right=cursor.fetchone()
        elif access=="controller":
            cursor.execute("SELECT id,username from controller where controller.id=%s",admin_id)
            right=cursor.fetchone()
        elif access=="users":
            cursor.execute("SELECT id,username from users where users.id=%s",admin_id)
            right=cursor.fetchone()
        else:
            return None

        if right['username']==username_hash:
            return {'admin_id':admin_id,'access':access}
        else:
            return None


def password_encryption(password):
    
    password=password+salt
    password_hash = hashlib.sha512(password.encode("utf-8")).hexdigest()
    password_hash=salt+password_hash+salt
    password_hash=  hashlib.sha512(password_hash.encode("utf-8")).hexdigest()
    # print(password_hash)
    return password_hash


def username_check(username):
    try:
        connection=get_connection()
        cursor=connection.cursor()

        cursor.execute("SELECT * from controller where username=%s",(username))
        user_check=cursor.fetchone()
        if user_check==None:
            cursor.execute("SELECT * from super_admin where username=%s",(username))
            user_check=cursor.fetchone()
            if user_check==None:
                cursor.execute("SELECT * from admin where username=%s",(username))
                user_check=cursor.fetchone()
                if user_check==None:
                    cursor.execute("SELECT * from admin_group where username=%s",(username))
                    user_check=cursor.fetchone()
                    if user_check==None:
                        cursor.execute("SELECT * from users where username=%s",(username))
                        user_check=cursor.fetchone()
                        if user_check==None:
                            return {"message":True}
                        else:
                            return{"message":" username Already Exists"}
                    else:
                        return {"message":" username Already Exists"}
                else:
                    return{"message":" username Already Exists"}
            else:
                return{"message":" username Already Exists"}
        else:
            return{"message":" username Already Exists"}
    # except Exception as e:
    #     raise e
    finally:
        cursor.close()
        connection.close()

def sms(message,Template_id):
    
    message=message
    # to_number=[9952716727,9941606715,9944087546]
    to_number=[9952716727,9789301757]
    for i in to_number:
        url="http://sms.ourcampus.in/sendsms?uname=alliance20&pwd=allian234&senderid=SECSMS&to="+str(i)+"&msg="+message+"&route=T&peid=1701158038234467676&tempid="+str(Template_id)
        data_api=requests.post(url)
    
    result=data_api.json()
    print("Messagge Send Succesfull ",result ,"status:",status,"description",description)

def sms(message,Template_id):
    
    message=message
    # to_number=[9952716727,9941606715,9944087546]
    to_number=[9952716727,9789301757,9944087546]
    # to_number=[9789301757]
    # 
    for i in to_number:
        url="http://sms.ourcampus.in/sendsms?uname=alliance20&pwd=allian234&senderid=SECSMS&to="+str(i)+"&msg="+message+"&route=T&peid=1701158038234467676&tempid="+str(Template_id)
        data_api=requests.post(url)
    
    result=data_api.json()
    print("Messagge Send Succesfull ",result ,"status:",message,"Template_id",Template_id)
    return{"Messagge Send Succesfull ",result ,"status:",message,"Template_id",Template_id}


def sms_switch(name,status,sms_status):
    # sms_status=open("/var/www/solar_panel/inventory/power/sms/sms_status.py",'r')
    # sms_status=json.load(sms_status)
    print(sms_status,status,name,type(status))
    for i in sms_status:
        print('input name:',i)
        if i==name:
            print('name pass and sms_status: ',sms_status[i])
            if status==0 and sms_status[i]==1:
                print("message")
                sms_status[i]=0
                # with open("/var/www/solar_panel/inventory/power/sms/sms_status.py",'w') as f:
                #     f.write(json.dumps(sms_status))
                print(sms_status)
                return True
            elif(status==1 and sms_status[i]==0):
                print("message alert on")
                sms_status[i]=1
                # with open("/var/www/solar_panel/inventory/power/sms/sms_status.py",'w') as f:
                #     f.write(json.dumps(sms_status))
                print(sms_status)
                return False
            else:
                print("Not Allowed")
                return False
            

