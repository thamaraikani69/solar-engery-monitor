from database.get_connection import get_connection
import secrets
from datetime import date,datetime
import os

today=date.today()
timedate =datetime.now()

def image_(image_upload,account_id,server_path,type_):
    try: 
        connection=get_connection()
        cursor=connection.cursor()

        image_check=image_securty(image_upload)
        image_save=False 
        
        added_on=today
        lastchange=timedate

        if image_check == True:

            if type_=='account':
                cursor.execute("SELECT * from accounts ")
            elif type_=='admin_group':
                cursor.execute("SELECT * from admin_group ")
            hexa_check=cursor.fetchall()

            random_hex = secrets.token_hex(16)
            count=0
            while count<len(hexa_check):

                for i in hexa_check:
                    if type_=='account':
                        images=i['attachment']
                    elif type_=='admin_group':
                        images=i['logo']
                    f_ext = os.path.splitext(images)[0]

                    if f_ext==random_hex:
                        random_hex = secrets.token_hex(16)
                        count=0
                    else:
                        count+=1
            _, f_ext = os.path.splitext(image_upload.filename)
            picture_fn = random_hex +f_ext

            path=type_
            image_save= save_image(path,picture_fn,image_upload,server_path)
            print(image_save)
            if image_save==True:
                if type_=='account':
                    cursor.execute("UPDATE accounts set attachment=%s where id=%s",(picture_fn,account_id))
                elif type_=='admin_group':
                    cursor.execute("UPDATE admin_group set logo=%s where id=%s",(picture_fn,account_id))
                connection.commit()
                return {"message":"save successfully"}
            else:
                return{"message":"something wrong"}
        else:
            return{"message":image_check}
    # except Exception as e:
    #     return{"message":str(e)},400
    finally:
        cursor.close()
        connection.close()

import os 
from PIL import Image
from flask import jsonify,make_response


allowed_format = ["PNG","JPG","JPEG"]
allowed_size = 2050000*5

def image_securty(img_upload):

    if img_upload==None:
        return ("empty file")
    else:
        filesize=len(img_upload.read())
        if not image_size(filesize):
            return ("File less than 10mb")

        if img_upload.filename=="":
            return("image must have filename")

        if not allowed_image(img_upload.filename):
            return('image has extention not allowed')
        else:
            return True

def allowed_image(filename):

    if not "." in filename:
        return False

    ext=filename.rsplit(".",1)[1]
    
    # if ext.upper() == "MP4":
    #     return True
    # else:
    #     if ext.upper() in allowed_format:
    #         return True
    #     else:
    #         return False

    if ext.upper() in allowed_format:
            return True
    else:
        return False

def image_size(filesize):
    
    if int(filesize) < int(allowed_size):
        return True
    else:
        return False

def save_image(path,picture_fn,image_upload,server_path):
    try:
        picture_path = os.path.join(server_path, path, picture_fn)
        output_size = (250, 250)
        i = Image.open(image_upload)

        if i.mode in ("RGBA", "P"):
            i = i.convert("RGB")
            # i.thumbnail(output_size, Image.ANTIALIAS)

        i.save(picture_path,quality=100)

        return True
    except Exception as e:
        print(e)
        return False
    finally:
        print("kani")