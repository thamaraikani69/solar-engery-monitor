from flask import request, redirect, url_for, session,flash,jsonify
from database.get_connection import get_connection
from inventory.token_validator import get_inventory_token, inventory_token
from datetime import date,datetime
import json
from flask import make_response
from werkzeug.utils import secure_filename
import os
import time
import csv
import dateparser

from pytz import timezone
# rights
from inventory.power.rights import rights,password_encryption,username_check,sms,sms_switch	

# api's
from flask_restful import Resource,Api

today=date.today()
the_today=date.today()
from datetime import datetime
timedate =datetime.now(timezone('Asia/Kolkata'))
timedate=timedate.replace(tzinfo=None)
the_timedate=timedate
today=timedate.date()


import datetime

def remove_duplicate_dicts(l):
    seen = set()
    new_l = []
    for d in l:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            new_l.append(d)
    return new_l

class login(Resource):
	"""docstring for test_api"""
	def post(self):
		

		try:

			# print('access',access)
			
			username=request.json['username']
			password=request.json['password']

			# user_encryption
			# password_encryption

			username_hash=(username)
			password_hash=password_encryption(password)
			
			connection = get_connection()
			cursor = connection.cursor()
			# print(username_hash,password_hash)
			cursor.execute("SELECT id,name from admin where admin.username=%s and admin.password=%s limit 1", (username_hash, password_hash))
			result = cursor.fetchone()
			if result==None:
				cursor.execute("SELECT id,name from admin_group where admin_group.username=%s and admin_group.password=%s limit 1", (username_hash, password_hash))
				result = cursor.fetchone()
				if result==None:
					cursor.execute("SELECT id,name from super_admin where super_admin.username=%s and super_admin.password=%s limit 1", (username_hash, password_hash))
					result = cursor.fetchone()
					if result==None:
						cursor.execute("SELECT id,name from controller where controller.username=%s and controller.password=%s limit 1", (username_hash, password_hash))
						result = cursor.fetchone()
						# print(result)
						if result==None:
							cursor.execute("SELECT id,name from users where users.username=%s and users.password=%s limit 1", (username_hash, password_hash))
							result = cursor.fetchone()
							if result==None:
								return {'message':'Invaild username and password'},400
							else:
								access='users'	
						else:
							access='controller'	
					else:
						access='super_admin'	
				else:
					access='admin_group'	
			else:
				access='admin'
			session["inventory_token"] = get_inventory_token(result["id"],username_hash, password_hash,access)
			# print(access,session)
			
			return make_response(jsonify({'message':'Login Successfull','user':result['name'],'access':access,'token':session["inventory_token"]}),200)
		except KeyError as e:
			return make_response(jsonify({'message':str(e)}),400)
		finally:
			cursor.close()
			connection.close()
			
class logout(Resource):
	"""docstring for logout"""

	def post(self):
		if 'inventory_token' in session:
			session.pop('inventory_token')
			return {'message':'Logout Successfully..'},200
		else:
			return{"message":'NO Session Loged In'},400

		# ======================================================================== create super admin ==========================

class create_super_admin(Resource):
	"""docstring for create_super_admin"""
	@inventory_token
	def post(self):

		if rights()!=None:
			access=rights()['access']

			if access=='controller':

				name=request.json['name']
				addedon=today
				username=request.json['username']
				password=request.json['password']
				location=request.json['location']
				status=request.json['status']
				lastchange=timedate
				
				password_hash=password_encryption(password)
				try:
					connection=get_connection()
					cursor=connection.cursor()
					check=username_check(username)
					# print(check)
					if check['message']==True:
						# print(check['message'])
						cursor.execute("INSERT into super_admin value(null,%s,%s,%s,%s,%s,%s,%s)",(name,addedon,username,password_hash,location,status,lastchange))
						connection.commit()

						return make_response(jsonify({'message':'Successfully Created'}),200)
					else:
						return make_response(jsonify({'message':check['message']}),400)

				except Exception as e:
					return{'Error Message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

		# ======================================================================== view super admin ==========================

class view_super_admin(Resource):
	"""docstring for view_super_admin"""
	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']

			if access=='controller':

				
				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from super_admin")
					result=cursor.fetchall()
					
					
					return make_response(jsonify({'message':'successfull','data':result}),200)
				except Exception as e:
					return make_response(jsonify({'Error Message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

	# ======================================================================== Edit super admin ==========================

class edit_super_admin(Resource):
	"""docstring for create_super_admin"""
	@inventory_token
	def put(self):

		if rights()!=None:
			access=rights()['access']

			if access=='controller':

				id=request.json['id']
				name=request.json['name']
				username=request.json['username']
				password=request.json['password']
				location=request.json['location']
				status=request.json['status']
				lastchange=timedate

				password_hash=password_encryption(password)
				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from super_admin where id=%s",(id))
					id_check=cursor.fetchone()

					if id_check!=None:

						check=username_check(username)
						# print("==================cntroller",check)
						if check['message']==True:

							if password=="":
								cursor.execute("UPDATE super_admin set name=%s,username=%s,location=%s,status=%s,lastchange=%s where id=%s",(name,username,location,status,lastchange,id))
								connection.commit()
								
							else:
								cursor.execute("UPDATE super_admin set name=%s,username=%s,password=%s,location=%s,status=%s,lastchange=%s where id=%s",(name,username,password_hash,location,status,lastchange,id))
								connection.commit()
							return make_response(jsonify({'message':'Successfully Updated'}),200)
						else:
							if password=="":
								cursor.execute("UPDATE super_admin set name=%s,location=%s,status=%s,lastchange=%s where id=%s",(name,location,status,lastchange,id))
								connection.commit()
								
							else:
								cursor.execute("UPDATE super_admin set name=%s,username=%s,password=%s,location=%s,status=%s,lastchange=%s where id=%s",(name,username,password_hash,location,status,lastchange,id))
								connection.commit()
							
							return make_response(jsonify({'message':check['message']+'\t Remaining data updated'}),400)

					else:
						return make_response(jsonify({'message':'id doesnot exit in database'}),400)

																	# except Exception as e:
				# 	return{'Error Message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return{"message":"Not authorized"},401
		else:
			return{"message":'Something Wrong Please Logout And Login Again'},400

	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']

			if access=='controller':

				id=request.json['id']
				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from super_admin where id=%s",(id))
					result=cursor.fetchone()
					data=[]

					if result!=None:
						id=result['id']
						name=result['name']
						username=result['username']
						password=result['password']
						location=result['location']
						status=result['status']
						lastchange=str(result['lastchange'])
						data.append({'id':id,'name':name,'username':username,'password':password,'location':location,'status':status,'lastchange':lastchange})
						
						return {'message':data}
					else:
						return{'Message':"ID Invalid"}

				except Exception as e:
					return{'Error Message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return{"message":"Not authorized"},401
		else:
			return{"message":'Something Wrong Please Logout And Login Again'},400


	# ======================================================================== status super admin ==========================

class status_super_admin(Resource):
	"""docstring for create_super_admin"""
	@inventory_token
	def put(self):

		if rights()!=None:
			access=rights()['access']

			if access=='controller':

				id=request.json['id']
				status=request.json['status']
				lastchange=timedate

				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from super_admin where id=%s",(id))
					id_check=cursor.fetchone()

					if id_check!=None:

						cursor.execute("UPDATE super_admin set status=%s,lastchange=%s where id=%s",(status,lastchange,id))
						connection.commit()

						return {'message':'Successfully Updated'},200

					else:
						return{'message':'id doesnot exit in database'},400

				except Exception as e:
					return{'Error Message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return{"message":"Not authorized"},401
		else:
			return{"message":'Something Wrong Please Logout And Login Again'},400
# ======================================================================== create users ==========================

class create_users(Resource):
	"""docstring for create_support"""
	@inventory_token
	def post(self):

		if rights()!=None:
			access=rights()['access']
			access_id=rights()['admin_id']

			if access=='super_admin':

				name=request.json['name']
				addedon=timedate
				username=request.json['username']
				password=request.json['password']
				view=request.json['view']
				edit=request.json['edit']
				approve=request.json['approve']
				admin_list=request.json['admin_list']
				lastchange=timedate
				
				password_hash=password_encryption(password)
				try:
					connection=get_connection()
					cursor=connection.cursor()
					
					check=username_check(username)
					# print(check)
					if admin_list==[]:
						return make_response(jsonify({'message':"Please Select admin name"}),400)

					if check['message']==True:
						cursor.execute("INSERT into users value(null,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(name,addedon,username,password,view,edit,approve,lastchange,access_id))
						connection.commit()
						user_id=cursor.lastrowid
						for admin_id in admin_list:
							cursor.execute("INSERT into user_admin_allote value(null,%s,%s,%s)",(addedon,user_id,admin_id))
							connection.commit()
						return make_response(jsonify({'message':'Successfully Created'}),200)

					else:
						return make_response(jsonify({'message':check['message']}),400)
				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

	@inventory_token
	def put(self):

		if rights()!=None:
			access=rights()['access']
			access_id=rights()['admin_id']

			if access=='super_admin':

				id=request.json['id']
				name=request.json['name']
				addedon=timedate
				username=request.json['username']
				password=request.json['password']
				view=request.json['view']
				edit=request.json['edit']
				approve=request.json['approve']
				admin_list=request.json['admin_list']
				lastchange=timedate
				
				password_hash=password_encryption(password)
				try:
					connection=get_connection()
					cursor=connection.cursor()
					
					check=username_check(username)
					# print(check)
					if admin_list==[]:
						return make_response(jsonify({'message':"Please Select admin name"}),400)

					if check['message']==True:
						cursor.execute("UPDATE users set name=%s,username=%s,view=%s,edit=%s,approve=%s,lastchange=%s where id=%s",(name,username,view,edit,approve,lastchange,id))
						connection.commit()
						if password!="":
							cursor.execute("UPDATE users set password=%s where id=%s",(password_hash,id))
							connection.commit()
						user_id=id
						cursor.execute("DELETE from user_admin_allote where user_id=%s",(id))
						connection.commit()

						for admin_id in admin_list:
							cursor.execute("INSERT into user_admin_allote value(null,%s,%s,%s)",(addedon,user_id,admin_id))
							connection.commit()
						return make_response(jsonify({'message':'Successfully Created'}),200)

					else:
						cursor.execute("UPDATE users set name=%s,view=%s,edit=%s,approve=%s,lastchange=%s where id=%s",(name,view,edit,approve,lastchange,id))
						connection.commit()
						if password!="":
							cursor.execute("UPDATE users set password=%s where id=%s",(password_hash,id))
							connection.commit()
						user_id=id
						cursor.execute("DELETE from user_admin_allote where user_id=%s",(id))
						connection.commit()

						for admin_id in admin_list:
							cursor.execute("INSERT into user_admin_allote value(null,%s,%s,%s)",(addedon,user_id,admin_id))
							connection.commit()
						
						return make_response(jsonify({'message':check['message']+'\t Remaining data updated'}),400)
				except KeyError as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

	@inventory_token
	def delete(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id=request.json['id']
				access_id=rights()['admin_id']
				
				try:
					connection=get_connection()
					cursor=connection.cursor()
					
					cursor.execute("DELETE from users where id=%s",(id))
					cursor.execute("DELETE from user_admin_allote where user_id=%s",(id))
					connection.commit()

					return make_response(jsonify({'message':'successfull'}),200)

				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)
# ========================================================================  users alloted admin ==========================

class user_admin(Resource):
	"""docstring for view_admin"""
	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']
			access_id=rights()['admin_id']

			if access=='super_admin':

				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from user_admin_allote")
					result=cursor.fetchall()
					return make_response(jsonify({'message':'successfull','data':result}),200)
				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)
# ======================================================================== view users ==========================

class view_users(Resource):
	"""docstring for view_admin"""
	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']
			access_id=rights()['admin_id']

			if access=='super_admin':

				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from users where super_id=%s",(access_id))
					result=cursor.fetchall()
					return make_response(jsonify({'message':'successfull','data':result}),200)
				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)
		# ======================================================================== create roll ==========================

class create_roll(Resource):
	"""docstring for create_super_admin"""
	@inventory_token
	def post(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				access_id=rights()['admin_id']

				roll_name=request.json['name']
				status=request.json['status']
				accounts_approver=request.json['accounts_approver']
				
				if status=='active':
					status='active'
				else:
					status='inactive'

				if accounts_approver=='yes':
					accounts_approver='yes'
				else:
					accounts_approver='no'

				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("INSERT into rolls value(null,%s,%s,%s,%s)",(roll_name,status,accounts_approver,access_id))
					connection.commit()

					return make_response(jsonify({'message':'Successfully Created'}),200)

				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)
		# ======================================================================== view roll ==========================

class view_roll(Resource):
	"""docstring for view_roll"""
	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']
			access_id=rights()['admin_id']
			if access=='super_admin':

				
				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from rolls where super_id=%s",(access_id))
					result=cursor.fetchall()

					return make_response(jsonify({'message':'successfull','data':result}),200)
				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)
	# ======================================================================== Edit roll ==========================

class edit_roll(Resource):
	"""docstring for create_roll"""
	@inventory_token
	def put(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id=request.json['id']
				access_id=rights()['admin_id']
				roll_name=request.json['roll_name']
				status=request.json['status']
				accounts_approver=request.json['accounts_approver']

				if status=='active':
					status='active'
				else:
					status='inactive'

				if accounts_approver=='yes':
					accounts_approver='yes'
				else:
					accounts_approver='no'

				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from rolls where id=%s and super_id=%s",(id,access_id))
					id_check=cursor.fetchone()

					if id_check!=None:
						cursor.execute("UPDATE rolls set roll_name=%s,status=%s,accounts_approver=%s where id=%s",(roll_name,status,accounts_approver,id))
						connection.commit()

						return {'message':'Successfully Updated'},200

					else:
						return{'message':'id doesnot exit in database'},400

				except Exception as e:
					return{'Error Message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return{"message":"Not authorized"},401
		else:
			return{"message":'Something Wrong Please Logout And Login Again'},400


	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id=request.json['id']
				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from rolls where id=%s",(id))
					result=cursor.fetchone()
					
					if result!=None:
						return {'message':result}
					else:
						return{'Message':"ID Invalid"}
				except Exception as e:
					return{'Error Message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return{"message":"Not authorized"},401
		else:
			return{"message":'Something Wrong Please Logout And Login Again'},400

	# ======================================================================== status roll ==========================

class status_roll(Resource):
	"""docstring for create_super_admin"""
	@inventory_token
	def put(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id=request.json['id']
				access_id=rights()['admin_id']
				status=request.json['status']

				if status=='active':
					status='active'
				else:
					status='inactive'

				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from rolls where id=%s and super_id=%s",(id,access_id))
					id_check=cursor.fetchone()

					if id_check!=None:

						cursor.execute("UPDATE rolls set status=%s where id=%s",(status,id))
						connection.commit()

						return {'message':'Successfully Updated'},200

					else:
						return{'message':'id doesnot exit in database'},400

				except Exception as e:
					return{'Error Message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return{"message":"Not authorized"},401
		else:
			return{"message":'Something Wrong Please Logout And Login Again'},400


		# ======================================================================== create admin ==========================

class create_admin(Resource):
	"""docstring for create_admin"""
	@inventory_token
	def post(self):

		
		if rights()!=None:
			
			access=rights()['access']
			
			if access=='super_admin':
				access_id=rights()['admin_id']
				name=request.json['name']
				addedon=today
				username=request.json['username']
				password=request.json['password']
				location=request.json['location']
				status=request.json['status']
				lastchange=timedate
				address=request.json['address']
				lat_lon=request.json['lat_lon']
				admin_grp_list=request.json['admin_grp_list']
				
				password_hash=password_encryption(password)
				try:
					connection=get_connection()
					cursor=connection.cursor()

					check=username_check(username)
					if admin_grp_list==[]:
						return make_response(jsonify({"message":'Please Select group admin'}),400)

					if check['message']==True:

						cursor.execute("INSERT into admin value(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(name,addedon,username,password_hash,location,status,lastchange,address,lat_lon,access_id))
						connection.commit()
						admin_id=cursor.lastrowid
						# print("admin_id",admin_id,"admin_grp_list",len(admin_grp_list))
						for i in admin_grp_list:
							if i == "ALL":
								pass
							else:
								# print("pass")
								cursor.execute("INSERT into alloted_admin value(null,%s,%s,%s)",(addedon,admin_id,i))
								connection.commit()
						return make_response(jsonify({'message':'Successfully Created'}),200)
					else:
						return make_response(jsonify({"message":check['message']}),400)

				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)


	@inventory_token
	def put(self):

		
		if rights()!=None:
			
			access=rights()['access']
			
			if access=='super_admin':
				access_id=rights()['admin_id']
				id=request.json['id']
				name=request.json['name']
				addedon=today
				username=request.json['username']
				password=request.json['password']
				location=request.json['location']
				status=request.json['status']
				lastchange=timedate
				address=request.json['address']
				lat_lon=request.json['lat_lon']
				admin_grp_list=request.json['admin_grp_list']
				
				password_hash=password_encryption(password)
				try:
					connection=get_connection()
					cursor=connection.cursor()

					check=username_check(username)
					if admin_grp_list==[]:
						return make_response(jsonify({"message":'Please Select group admin'}),400)

					if check['message']==True:

						cursor.execute("UPDATE admin set name=%s,username=%s,location=%s,status=%s,lastchange=%s,address=%s,lat_lon=%s where id=%s",(name,username,location,status,lastchange,address,lat_lon,id))
						connection.commit()
						if password!="":
							cursor.execute("UPDATE admin set password=%s where id=%s",(password_hash,id))
							connection.commit()
						admin_id=id
						cursor.execute("DELETE from alloted_admin where admin_id=%s",(admin_id))
						connection.commit()
						for i in admin_grp_list:
							if i == "ALL":
								pass
							else:
								cursor.execute("INSERT into alloted_admin value(null,%s,%s,%s)",(addedon,admin_id,i))
								connection.commit()
						return make_response(jsonify({'message':'Successfully Created'}),200)
					else:
						cursor.execute("UPDATE admin set name=%s,location=%s,status=%s,lastchange=%s,address=%s,lat_lon=%s where id=%s",(name,location,status,lastchange,address,lat_lon,id))
						connection.commit()
						admin_id=id
						cursor.execute("DELETE from alloted_admin where admin_id=%s",(admin_id))
						connection.commit()
						if password!="":
							cursor.execute("UPDATE admin set password=%s where id=%s",(password_hash,id))
							connection.commit()
						for i in admin_grp_list:
							if i == "ALL":
								pass
							else:
								cursor.execute("INSERT into alloted_admin value(null,%s,%s,%s)",(addedon,admin_id,i))
								connection.commit()
						return make_response(jsonify({"message":check['message']+'\tRemaing data updated'}),400)

				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

	@inventory_token
	def get(self):

		
		if rights()!=None:
			
			access=rights()['access']
			
			if access=='super_admin':
				access_id=rights()['admin_id']
				
				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT admin.name,admin.id,alloted_admin.admin_grp_id,alloted_admin.admin_id from alloted_admin,admin where admin.id=alloted_admin.admin_id")
					data=cursor.fetchall()
						
					return make_response(jsonify({'message':'Successfull','data':data}),200)
				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)


	@inventory_token
	def delete(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id=request.json['id']
				access_id=rights()['admin_id']
				
				try:
					connection=get_connection()
					cursor=connection.cursor()
					
					cursor.execute("DELETE from admin where id=%s",(id))
					cursor.execute("DELETE from alloted_admin where admin_id=%s",(id))
					connection.commit()

					return make_response(jsonify({'message':'successfull'}),200)

				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)
# ======================================================================== view admin ==========================

class view_admin(Resource):
	"""docstring for view_admin"""
	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']

			if (access=='super_admin')|(access=='admin'):

				try:
					connection=get_connection()
					cursor=connection.cursor()
					access_id=rights()['admin_id']
					cursor.execute("SELECT * from admin where super_id=%s",(access_id))
					# cursor.execute("SELECT * from admin")
					result=cursor.fetchall()
					cursor.execute("SELECT * from alloted_admin,admin_group where admin_group.id=alloted_admin.admin_grp_id ")
					admin_result=cursor.fetchall()
					# print(result)
					return make_response(jsonify({'message':"successfull","data":result,"admin_result":admin_result}),200)
				except Exception as e:
					return{'message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return{"message":"Not authorized"},401
		else:
			return{"message":'Something Wrong Please Logout And Login Again'},400

	# ======================================================================== Edit super admin ==========================

class edit_admin(Resource):
	

	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':
				id=request.json['id']
				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from admin where id=%s",(id))
					result=cursor.fetchone()
					if result!=None:
						data=[]

						id=result['id']
						name=result['name']
						addedon=str(result['addedon'])
						username=result['username']
						password=result['password']
						location=result['location']
						status=result['status']
						lastchange=str(result['lastchange'])
						address=result['address']
						lat_lon=result['lat_lon']
						data.append({'id':id,"addedon":addedon,'name':name,'username':username,'password':password,'location':location,'status':status,'lastchange':lastchange,"address":address,'lat_lon':lat_lon})
						
						return {'message':data}
					else:
						return{"message":"ID Invalid"}

				except Exception as e:
					return{'Error Message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return{"message":"Not authorized"},401
		else:
			return{"message":'Something Wrong Please Logout And Login Again'},400

	# ======================================================================== status super admin ==========================

class status_admin(Resource):
	"""docstring for create_admin"""
	@inventory_token
	def put(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id=request.json['id']
				status=request.json['status']
				lastchange=timedate
				access_id=rights()['admin_id']

				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from admin where id=%s and super_id=%s",(id,access_id))
					id_check=cursor.fetchone()

					if id_check!=None:

						cursor.execute("UPDATE admin set status=%s,lastchange=%s where id=%s",(status,lastchange,id))
						connection.commit()

						return {'message':'Successfully Updated'},200

					else:
						return{'message':'id doesnot exit in database'},400

				except Exception as e:
					return{'Error Message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return{"message":"Not authorized"},401
		else:
			return{"message":'Something Wrong Please Logout And Login Again'},400


		# ======================================================================== create inverter ==========================

class create_inverter(Resource):
	"""docstring for create_inverter"""
	@inventory_token
	def post(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				name=request.json['name']
				access_id=rights()['admin_id']
				addedon=today
				capacity=request.json['capacity']
				install_date=request.json['install_date']
				admin=request.json['admin']
				status=request.json['status']
				groupadmin=request.json['groupadmin']
				lastchange=timedate
				equipment_id=request.json['equipment_id']
				slave_id=request.json['slave_id']
				energy_meter=request.json['energy_meter']
				

				if status=='active':
					status='active'
				else:
					status='inactive'

				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("INSERT into inverter value(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(name,addedon,capacity,install_date,admin,status,lastchange,access_id,groupadmin,equipment_id,slave_id,energy_meter))
					connection.commit()

					return make_response(jsonify({'message':'Successfully Created'}),200)

				except KeyError as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)
	@inventory_token
	def put(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id=request.json['id']
				name=request.json['name']
				access_id=rights()['admin_id']
				addedon=today
				capacity=request.json['capacity']
				install_date=request.json['install_date']
				admin=request.json['admin']
				status=request.json['status']
				groupadmin=request.json['groupadmin']
				lastchange=timedate
				equipment_id=request.json['equipment_id']
				slave_id=request.json['slave_id']
				energy_meter=request.json['energy_meter']
				

				if status=='active':
					status='active'
				else:
					status='inactive'

				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("UPDATE inverter set name=%s,capacity=%s,install_date=%s,admin=%s,status=%s,lastchange=%s,groupadmin=%s,equipment_id=%s,slave_id=%s,energy_meter_id=%s where id=%s",(name,capacity,install_date,admin,status,lastchange,groupadmin,equipment_id,slave_id,energy_meter,id))
					connection.commit()

					return make_response(jsonify({'message':'Successfully Created'}),200)

				except KeyError as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

	@inventory_token
	def delete(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id=request.json['id']
				access_id=rights()['admin_id']
				
				try:
					connection=get_connection()
					cursor=connection.cursor()
					
					cursor.execute("DELETE from inverter where id=%s",(id))
					connection.commit()

					return make_response(jsonify({'message':'Successfull'}),200)

				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)
# ======================================================================== view admin ==========================

class view_inverter(Resource):
	"""docstring for view_admin"""
	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				try:
					connection=get_connection()
					cursor=connection.cursor()
					access_id=rights()['admin_id']
					cursor.execute("SELECT * from inverter,admin where admin.id=inverter.admin and inverter.admin_id=%s",(access_id))
					result=cursor.fetchall()
					
					return make_response(jsonify({'message':'successfull','data':result}),200)
				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)
class admin_view_inverter(Resource):
	"""docstring for view_admin"""
	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']

			if access=='admin':

				try:
					connection=get_connection()
					cursor=connection.cursor()
					access_id=rights()['admin_id']
					cursor.execute("SELECT * from inverter,admin where admin.id=inverter.admin and inverter.admin=%s",(access_id))
					result=cursor.fetchall()
					
					return make_response(jsonify({'message':'successfull','data':result}),200)
				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)
	# ======================================================================== Edit inverter ==========================

class edit_inverter(Resource):
	"""docstring for create_inverter"""
	@inventory_token
	def put(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id=request.json['id']
				access_id=rights()['admin_id']
				name=request.json['name']
				addedon=today
				capacity=request.json['capacity']
				install_date=request.json['install_date']
				admin=request.json['admin']
				status=request.json['status']
				groupadmin=request.json['groupadmin']
				lastchange=timedate
				

				if status=='active':
					status='active'
				else:
					status='inactive'

				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from inverter where id=%s and admin_id=%s",(id,access_id))
					id_check=cursor.fetchone()

					if id_check!=None:

						cursor.execute("UPDATE inverter set name=%s,capacity=%s,install_date=%s,admin=%s,status=%s,lastchange=%s,groupadmin=%s where id=%s",(name,capacity,install_date,admin,status,lastchange,groupadmin,id))
						connection.commit()

						return {'message':'Successfully Updated'},200
					else:
						return{'message':'id doesnot exit in database'},400

				except Exception as e:
					return{'Error Message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return{"message":"Not authorized"},401
		else:
			return{"message":'Something Wrong Please Logout And Login Again'},400

	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':
				access_id=rights()['admin_id']
				id=request.json['id']
				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from inverter where id=%s and admin_id=%s",(id,access_id))
					result=cursor.fetchone()
					
					if result!=None:
						data=[]
						id=result['id']
						name=result['name']
						addedon=str(result['addedon'])
						capacity=result['capacity']
						install_date=str(result['install_date'])
						admin=result['admin']
						status=result['status']
						lastchange=str(result['lastchange'])
						data.append({'id':id,"addedon":addedon,'name':name,'capacity':capacity,'install_date':install_date,'admin':admin,'status':status,'lastchange':lastchange})
					
						return {'message':data}
					else:
						return{"message":"ID Invalid"}

				except Exception as e:
					return{'Error Message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return{"message":"Not authorized"},401
		else:
			return{"message":'Something Wrong Please Logout And Login Again'},400

	# ======================================================================== status inverter ==========================

class status_inverter(Resource):
	"""docstring for create_inverter"""
	@inventory_token
	def put(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id=request.json['id']
				access_id=rights()['admin_id']
				status=request.json['status']
				lastchange=timedate

				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from inverter where id=%s and admin_id=%s",(id,access_id))
					id_check=cursor.fetchone()

					if id_check!=None:

						cursor.execute("UPDATE inverter set status=%s,lastchange=%s where id=%s",(status,lastchange,id))
						connection.commit()

						return {'message':'Successfully Updated'},200

					else:
						return{'message':'id doesnot exit in database'},400

				except Exception as e:
					return{'Error Message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return{"message":"Not authorized"},401
		else:
			return{"message":'Something Wrong Please Logout And Login Again'},400


# ======================================================================== create smb ==========================

class create_smb(Resource):
	"""docstring for create_smb"""
	@inventory_token
	def post(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				smb_id=request.json['smb_id']
				access_id=rights()['admin_id']
				addedon=today
				capacity=request.json['capacity']
				inverter=request.json['inverter']
				admin=request.json['admin']
				status=request.json['status']
				groupadmin=request.json['groupadmin']
				lastchange=timedate
				equipment_id=request.json['equipment_id']
				slave_id=request.json['slave_id']
				

				if status=='active':
					status='active'
				else:
					status='inactive'

				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("INSERT into smb value(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(smb_id,addedon,capacity,inverter,admin,status,lastchange,access_id,groupadmin,equipment_id,slave_id))
					connection.commit()

					return make_response(jsonify({'message':'Successfully Created'}),200)

				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

	@inventory_token
	def put(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':
				id=request.json['id']
				smb_id=request.json['smb_id']
				access_id=rights()['admin_id']
				addedon=today
				capacity=request.json['capacity']
				inverter=request.json['inverter']
				admin=request.json['admin']
				status=request.json['status']
				groupadmin=request.json['groupadmin']
				lastchange=timedate
				equipment_id=request.json['equipment_id']
				slave_id=request.json['slave_id']
				

				if status=='active':
					status='active'
				else:
					status='inactive'

				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("UPDATE smb set smb_id=%s,capacity=%s,inverter=%s,admin=%s,status=%s,lastchange=%s,groupadmin=%s,equipment_id=%s,slave_id=%s where id=%s",(smb_id,capacity,inverter,admin,status,lastchange,groupadmin,equipment_id,slave_id,id))
					connection.commit()

					return make_response(jsonify({'message':'Successfully Created'}),200)

				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

	@inventory_token
	def delete(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':
				id=request.json['id']

				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("DELETE from smb where id=%s",(id))
					connection.commit()

					return make_response(jsonify({'message':'Successfully Created'}),200)

				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)
# ======================================================================== view admin ==========================

class view_smb(Resource):
	"""docstring for view_admin"""
	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				try:
					connection=get_connection()
					cursor=connection.cursor()
					access_id=rights()['admin_id']

					cursor.execute("SELECT * from smb,inverter,admin where inverter.id=smb.inverter and admin.id=smb.admin and smb.admin_id=%s",(access_id))
					result=cursor.fetchall()
					
					return make_response(jsonify({'message':'successfull','data':result}),200)
				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

class admin_view_smb(Resource):
	"""docstring for view_admin"""
	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']

			if access=='admin':

				try:
					connection=get_connection()
					cursor=connection.cursor()
					access_id=rights()['admin_id']

					cursor.execute("SELECT * from smb,inverter,admin where inverter.id=smb.inverter and admin.id=smb.admin and smb.admin=%s",(access_id))
					result=cursor.fetchall()
					
					return make_response(jsonify({'message':'successfull','data':result}),200)
				# except Exception as e:
				# 	return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)
	# ======================================================================== Edit smb ==========================

class edit_smb(Resource):

	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id=request.json['id']
				access_id=rights()['admin_id']
				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from smb where id=%s and admin_id=%s",(id,access_id))
					result=cursor.fetchone()
					
					if result!=None:
						data=[]
						id=result['id']
						smb_id=result['smb_id']
						addedon=str(result['addedon'])
						capacity=result['capacity']
						inverter=result['inverter']
						admin=result['admin']
						status=result['status']
						lastchange=str(result['lastchange'])
						data.append({'id':id,"addedon":addedon,'smb_id':smb_id,'capacity':capacity,'inverter':inverter,'admin':admin,'status':status,'lastchange':lastchange})
					
						return {'message':data}
					else:
						return {"Message":"ID Invalid"}

				except Exception as e:
					return{'Error Message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return{"message":"Not authorized"},401
		else:
			return{"message":'Something Wrong Please Logout And Login Again'},400

	# ======================================================================== status smb ==========================

class status_smb(Resource):
	"""docstring for create_smb"""
	@inventory_token
	def put(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id=request.json['id']
				access_id=rights()['admin_id']
				status=request.json['status']
				lastchange=timedate

				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from smb where id=%s and admin_id=%s",(id,access_id))
					id_check=cursor.fetchone()

					if id_check!=None:

						cursor.execute("UPDATE smb set status=%s,lastchange=%s where id=%s",(status,lastchange,id))
						connection.commit()

						return {'message':'Successfully Updated'},200

					else:
						return{'message':'id doesnot exit in database'},400

				except Exception as e:
					return{'Error Message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return{"message":"Not authorized"},401
		else:
			return{"message":'Something Wrong Please Logout And Login Again'},400


# ======================================================================== create energy_meter ==========================

class create_energy_meter(Resource):
	"""docstring for create_energy_meter"""
	@inventory_token
	def post(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				EM_id=request.json['EM_id']
				access_id=rights()['admin_id']
				addedon=today
				capacity=request.json['capacity']
				admin=request.json['admin']
				status=request.json['status']
				groupadmin=request.json['groupadmin']
				lastchange=timedate
				equipment_id=request.json['equipment_id']
				slave_id=request.json['slave_id']
				

				if status=='active':
					status='active'
				else:
					status='inactive'

				try:
					connection=get_connection()
					cursor=connection.cursor()
					
					cursor.execute("INSERT into energy_meter value(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(EM_id,addedon,capacity,admin,status,lastchange,access_id,groupadmin,equipment_id,slave_id))
					connection.commit()

					return make_response(jsonify({'message':'Successfully Created'}),200)

				except KeyError as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

	@inventory_token
	def put(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id=request.json['id']
				EM_id=request.json['EM_id']
				access_id=rights()['admin_id']
				addedon=today
				capacity=request.json['capacity']
				admin=request.json['admin']
				status=request.json['status']
				groupadmin=request.json['groupadmin']
				lastchange=timedate
				equipment_id=request.json['equipment_id']
				slave_id=request.json['slave_id']
				

				if status=='active':
					status='active'
				else:
					status='inactive'

				try:
					connection=get_connection()
					cursor=connection.cursor()
					
					cursor.execute("UPDATE energy_meter set EM_id=%s,capacity=%s,admin=%s,status=%s,lastchange=%s,groupadmin=%s,equipment_id=%s,slave_id=%s where id=%s",(EM_id,capacity,admin,status,lastchange,groupadmin,equipment_id,slave_id,id))
					connection.commit()

					return make_response(jsonify({'message':'Successfully Created'}),200)

				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

	@inventory_token
	def delete(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id=request.json['id']
				access_id=rights()['admin_id']
				
				try:
					connection=get_connection()
					cursor=connection.cursor()
					
					cursor.execute("DELETE from energy_meter where id=%s",(id))
					connection.commit()

					return make_response(jsonify({'message':'Successfull'}),200)

				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)
# ======================================================================== view admin ==========================

class view_energy_meter(Resource):
	"""docstring for view_admin"""
	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				try:
					connection=get_connection()
					cursor=connection.cursor()
					access_id=rights()['admin_id']
					cursor.execute("SELECT * from energy_meter,admin where  admin.id=energy_meter.admin and energy_meter.admin_id=%s",(access_id))
					result=cursor.fetchall()
					
					return make_response(jsonify({'message':'successfull','data':result}),200)
				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)
class admin_view_energy_meter(Resource):
	"""docstring for view_admin"""
	@inventory_token
	def get(self):
		
		if rights()!=None:
			access=rights()['access']
			if access=='admin':

				try:
					connection=get_connection()
					cursor=connection.cursor()
					access_id=rights()['admin_id']
					cursor.execute("SELECT * from energy_meter,admin where admin.id=energy_meter.admin and energy_meter.admin=%s",(access_id))
					result=cursor.fetchall()
					
					return make_response(jsonify({'message':'successfull','data':result}),200)
				# except Exception as e:
				# 	return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			# else:
			# 	return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)
	# ======================================================================== Edit engergy meter ==========================

class edit_energy_meter(Resource):
	"""docstring for create_smb"""
	@inventory_token
	def put(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id=request.json['id']
				access_id=rights()['admin_id']
				EM_id=request.json['EM_id']
				addedon=today
				capacity=request.json['capacity']
				inverter=request.json['inverter']
				admin=request.json['admin']
				status=request.json['status']
				groupadmin=request.json['groupadmin']
				lastchange=timedate
				

				if status=='active':
					status='active'
				else:
					status='inactive'

				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from energy_meter where id=%s and admin_id=%s",(id,access_id))
					id_check=cursor.fetchone()

					if id_check!=None:

						cursor.execute("UPDATE energy_meter set EM_id=%s,capacity=%s,inverter=%s,admin=%s,status=%s,lastchange=%s,groupadmin=%s where id=%s",(EM_id,capacity,inverter,admin,status,lastchange,groupadmin,id))
						connection.commit()

						return {'message':'Successfully Updated'},200
					else:
						return{'message':'id doesnot exit in database'},400

				except Exception as e:
					return{'Error Message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return{"message":"Not authorized"},401
		else:
			return{"message":'Something Wrong Please Logout And Login Again'},400

	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id=request.json['id']
				try:
					connection=get_connection()
					cursor=connection.cursor()
					access_id=rights()['admin_id']

					cursor.execute("SELECT * from energy_meter where id=%s and admin_id=%s",(id,access_id))
					result=cursor.fetchone()
					data=[]

					if result!=None:

						id=result['id']
						EM_id=result['EM_id']
						addedon=str(result['addedon'])
						capacity=result['capacity']
						inverter=result['inverter']
						admin=result['admin']
						status=result['status']
						lastchange=str(result['lastchange'])
						data.append({'id':id,"addedon":addedon,'EM_id':EM_id,'capacity':capacity,'inverter':inverter,'admin':admin,'status':status,'lastchange':lastchange})
					
						return {'message':data}
					else:
						return{'message':"ID Invalid"}

				except Exception as e:
					return{'Error Message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return{"message":"Not authorized"},401
		else:
			return{"message":'Something Wrong Please Logout And Login Again'},400
	# ======================================================================== status energy meter ==========================

class status_energy_meter(Resource):
	"""docstring for create_energy_meter"""
	@inventory_token
	def put(self):

		if rights()!=None:
			access=rights()['access']
			
			if access=='super_admin':

				id=request.json['id']
				access_id=rights()['admin_id']
				status=request.json['status']
				lastchange=timedate

				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from energy_meter where id=%s and admin_id=%s",(id,access_id))
					id_check=cursor.fetchone()

					if id_check!=None:

						cursor.execute("UPDATE energy_meter set status=%s,lastchange=%s where id=%s",(status,lastchange,id))
						connection.commit()

						return {'message':'Successfully Updated'},200

					else:
						return{'message':'id doesnot exit in database'},400

				except Exception as e:
					return{'Error Message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return{"message":"Not authorized"},401
		else:
			return{"message":'Something Wrong Please Logout And Login Again'},400

# ======================================================================== create gateway ==========================

class create_gateway(Resource):
	"""docstring for create_gateway"""
	@inventory_token
	def post(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				meter_id=request.json['meter_id']
				addedon=today
				capacity=request.json['capacity']
				admin=request.json['admin']
				status=request.json['status']
				groupadmin=request.json['groupadmin']
				api_key=str(request.json['api_key'])
				lastchange=timedate
				access_id=rights()['admin_id']

				if status=='active':
					status='active'
				else:
					status='inactive'

				try:
					connection=get_connection()
					cursor=connection.cursor()
					
					cursor.execute("SELECT * from gateway where api_key=%s",(api_key))
					api_check=cursor.fetchone()
					api_check=None
					if api_check==None:
						# print("*********--------*****", admin)
						cursor.execute("INSERT into gateway value(null,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(meter_id,addedon,capacity,admin,status,lastchange,access_id,groupadmin,api_key))
						connection.commit()

						return make_response(jsonify({'message':'Successfully Created'}),200)
					else:
						return make_response(jsonify({"message":"api key exists"}),400)

				except KeyError as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)
	@inventory_token
	def put(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id=request.json['id']
				meter_id=request.json['meter_id']
				addedon=today
				capacity=request.json['capacity']
				admin=request.json['admin']
				status=request.json['status']
				groupadmin=request.json['groupadmin']
				api_key=str(request.json['api_key'])
				lastchange=timedate
				access_id=rights()['admin_id']

				if status=='active':
					status='active'
				else:
					status='inactive'

				try:
					connection=get_connection()
					cursor=connection.cursor()
					
					cursor.execute("SELECT * from gateway where api_key=%s",(api_key))
					api_check=cursor.fetchone()
					if api_check==None:
						cursor.execute("UPDATE gateway set Meter_id=%s,capacity=%s,admin=%s,status=%s,lastchange=%s,groupadmin=%s,api_key=%s where id=%s",(meter_id,capacity,admin,status,lastchange,groupadmin,api_key,id))
						connection.commit()

						return make_response(jsonify({'message':'Successfully Created'}),200)
					else:
						cursor.execute("UPDATE gateway set Meter_id=%s,capacity=%s,admin=%s,status=%s,lastchange=%s,groupadmin=%s where id=%s",(meter_id,capacity,admin,status,lastchange,groupadmin,id))
						connection.commit()
						return make_response(jsonify({"message":"api key exists ..Remaining data updated"}),400)

				except KeyError as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

	@inventory_token
	def delete(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id=request.json['id']
				access_id=rights()['admin_id']
				
				try:
					connection=get_connection()
					cursor=connection.cursor()
					
					cursor.execute("DELETE from gateway where id=%s",(id))
					connection.commit()

					return make_response(jsonify({'message':'Successfull'}),200)

				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)
# ======================================================================== view admin ==========================

class view_gateway(Resource):
	"""docstring for view_admin"""
	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				try:
					connection=get_connection()
					cursor=connection.cursor()
					access_id=rights()['admin_id']
					cursor.execute("SELECT * from gateway,admin where admin.id=gateway.admin and gateway.admin_id=%s",(access_id))
					result=cursor.fetchall()
					
					return make_response(jsonify({'message':"successfull","data":result}),200)
				except Exception as e:
					return make_response(jsonify({'Error Message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)
class admin_view_gateway(Resource):
	"""docstring for view_admin"""
	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']

			if access=='admin':

				try:
					connection=get_connection()
					cursor=connection.cursor()
					access_id=rights()['admin_id']
					cursor.execute("SELECT * from gateway,admin where admin.id=gateway.admin and gateway.admin=%s",(access_id))
					result=cursor.fetchall()
					
					return make_response(jsonify({'message':"successfull","data":result}),200)
				except Exception as e:
					return make_response(jsonify({'Error Message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)
	# ======================================================================== Edit gateway ==========================

class edit_gateway(Resource):
	"""docstring for create_smb"""
	@inventory_token
	def put(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id=request.json['id']
				access_id=rights()['admin_id']
				meter_id=request.json['meter_id']
				addedon=today
				capacity=request.json['capacity']
				admin=request.json['admin']
				status=request.json['status']
				groupadmin=request.json['groupadmin']
				api_key=request.json['api_key']
				lastchange=timedate
				

				if status=='active':
					status='active'
				else:
					status='inactive'

				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from gateway where id=%s and admin_id=%s",(id,access_id))
					id_check=cursor.fetchone()

					if id_check!=None:
						cursor.execute("SELECT * from gateway where api_key=%s",(api_key))
						api_check=cursor.fetchone()
						if api_check==None:
							cursor.execute("UPDATE gateway set meter_id=%s,capacity=%s,admin=%s,status=%s,lastchange=%s,groupadmin=%s,api_key=%s where id=%s",(meter_id,capacity,admin,status,lastchange,groupadmin,api_key,id))
							connection.commit()

							return {'message':'Successfully Updated'},200
						else:
							return make_response(jsonify({"message":"api key exists"}),400)
					else:
						return{'message':'id doesnot exit in database'},400

				except Exception as e:
					return{'Error Message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return{"message":"Not authorized"},401
		else:
			return{"message":'Something Wrong Please Logout And Login Again'},400

	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id=request.json['id']
				access_id=rights()['admin_id']
				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from gateway where id=%s and admin_id=%s",(id,access_id))
					result=cursor.fetchone()
					data=[]

					if result!=None:

						id=result['id']
						meter_id=result['Meter_id']
						addedon=str(result['addedon'])
						capacity=result['capacity']
						admin=result['admin']
						status=result['status']
						lastchange=str(result['lastchange'])
						data.append({'id':id,"addedon":addedon,'meter_id':meter_id,'capacity':capacity,'admin':admin,'status':status,'lastchange':lastchange})
					
						return {'message':data}
					else:
						return{'message':"ID Invalid"}
				except Exception as e:
					return{'Error Message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return{"message":"Not authorized"},401
		else:
			return{"message":'Something Wrong Please Logout And Login Again'},400

	# ======================================================================== status gateway ==========================

class status_gateway(Resource):
	"""docstring for create_gateway"""
	@inventory_token
	def put(self):

		if rights()!=None:
			access=rights()['access']
			
			if access=='super_admin':

				id=request.json['id']
				access_id=rights()['admin_id']
				status=request.json['status']
				lastchange=timedate

				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from gateway where id=%s and admin_id=%s",(id,access_id))
					id_check=cursor.fetchone()

					if id_check!=None:

						cursor.execute("UPDATE gateway set status=%s,lastchange=%s where id=%s",(status,lastchange,id))
						connection.commit()

						return {'message':'Successfully Updated'},200

					else:
						return{'message':'id doesnot exit in database'},400

				except Exception as e:
					return{'Error Message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return{"message":"Not authorized"},401
		else:
			return{"message":'Something Wrong Please Logout And Login Again'},400


# ======================================================================== create wind and weather ==========================

class create_w_w(Resource):
	"""docstring for create_w_w"""
	@inventory_token
	def post(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				w_w=request.json['w_w']
				addedon=today
				capacity=request.json['capacity']
				admin=request.json['admin']
				status=request.json['status']
				groupadmin=request.json['groupadmin']
				equipment_id=request.json['equipment_id']
				slave_id=request.json['slave_id']
				# adminid=request.json['adminid']
				lastchange=timedate
				access_id=rights()['admin_id']

				if status=='active':
					status='active'
				else:
					status='inactive'

				try:
					connection=get_connection()
					cursor=connection.cursor()
					
					cursor.execute("INSERT into w_w value(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(w_w,addedon,capacity,admin,status,lastchange,access_id,groupadmin,equipment_id,slave_id))
					connection.commit()

					return make_response(jsonify({'message':'Successfully Created'}),200)

				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

	@inventory_token
	def put(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id=request.json['id']
				w_w=request.json['w_w']
				addedon=today
				capacity=request.json['capacity']
				admin=request.json['admin']
				status=request.json['status']
				groupadmin=request.json['groupadmin']
				equipment_id=request.json['equipment_id']
				slave_id=request.json['slave_id']
				# adminid=request.json['adminid']
				lastchange=timedate
				access_id=rights()['admin_id']

				if status=='active':
					status='active'
				else:
					status='inactive'

				try:
					connection=get_connection()
					cursor=connection.cursor()
					
					cursor.execute("UPDATE w_w set w_W=%s,capacity=%s,admin=%s,status=%s,lastchange=%s,groupadmin=%s,equipment_id=%s,slave_id=%s where id=%s",(w_w,capacity,admin,status,lastchange,groupadmin,equipment_id,slave_id,id))
					connection.commit()

					return make_response(jsonify({'message':'Successfully Created'}),200)

				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)
	
	@inventory_token
	def delete(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id=request.json['id']
				access_id=rights()['admin_id']

				try:
					connection=get_connection()
					cursor=connection.cursor()
					
					cursor.execute("DELETE from w_w where id=%s",(id))
					connection.commit()

					return make_response(jsonify({'message':'Successfull'}),200)

				# except Exception as e:
				# 	return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)
# ======================================================================== view admin ==========================

class view_w_w(Resource):
	"""docstring for view_admin"""
	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']
			# print(access)
			if (access=='super_admin') :

				try:
					connection=get_connection()
					cursor=connection.cursor()
					access_id=rights()['admin_id']

					cursor.execute("SELECT * from w_w,admin where admin.id=w_w.admin and w_w.admin_id=%s",(access_id))
					result=cursor.fetchall()
					
					# print(result,access_id)
					return make_response(jsonify({'message':"successfull",'data':result}),200)
				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

class admin_view_w_w(Resource):

	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']
			
			if (access=='admin') :

				try:
					connection=get_connection()
					cursor=connection.cursor()
					access_id=rights()['admin_id']

					cursor.execute("SELECT * from w_w,admin where admin.id=w_w.admin and w_w.admin=%s",(access_id))
					result=cursor.fetchall()
					
					cursor.execute("SELECT * from alloted_admin,admin_group where admin_group.id=alloted_admin.admin_grp_id and alloted_admin.admin_id=%s",(access_id))
					college_details=cursor.fetchone()
					# print('==================++++++++++++++++++===============',college_details)
					return make_response(jsonify({'message':"successfull",'data':result,'college_details':college_details}),200)
				# except Exception as e:
				# 	return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

class super_admin_view_w_w(Resource):

	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']
			
			if (access=='super_admin') :

				try:
					connection=get_connection()
					cursor=connection.cursor()
					my_data=request.json['my_data']
					access_id=rights()['admin_id']
					
					result=[]
					college_details=[]
					inv_data=[]
					# inv_sl_data_=[]
					inv_sl_data=[]
					w_w_sl_data=[]
					poa_data=[]
					for i in my_data:
						if access_id == i['super_id']:
							cursor.execute("SELECT * from w_w,admin where admin.id=w_w.admin and w_w.admin=%s",(i['id']))
							result_=cursor.fetchall()
							
							cursor.execute("SELECT * from alloted_admin,admin_group where admin_group.id=alloted_admin.admin_grp_id and alloted_admin.admin_id=%s",(i['id']))
							college_details_=cursor.fetchone()

							result.append(result_)
							college_details.append(college_details_)

							cursor.execute("SELECT * from inverter,admin where admin.id=inverter.admin and inverter.admin=%s",(i['id']))
							inv_data_=cursor.fetchall()
							inv_data.append(inv_data_)
							
							# ================================= inv data 
							data=inv_data_
							# api_key="c8DrAnUs"
							
							cursor.execute("SELECT * from gateway where admin=%s",(i['id']))
							api_key=cursor.fetchone()
							if api_key!=None:
								api_key=api_key['api_key']

							if api_key!=None:
								# ================================poa data 
								
								for r in result_:
									
									cursor.execute("SELECT * from solar_panel_data where EID=%s and ID=%s and api_key=%s ORDER by my_id desc limit 1",(r['equipment_id'],r['slave_id'],api_key))
									w_W_data1=cursor.fetchone()

									cursor.execute("SELECT sum(solar_panel_data.FIELD15) as poa_value from solar_panel_data where EID=%s and ID=%s and api_key=%s",(r['equipment_id'],r['slave_id'],api_key))
									poa_data_=cursor.fetchone()

									poa_data.append({'poa_value':poa_data_['poa_value'],'EID':r['equipment_id'],'ID':r['slave_id'],'admin_id':r['admin']})

									w_w_sl_data.append(w_W_data1)
								# print("poa_data",poa_data)

								# today = datetime.datetime(2020, 11, 10)
								# endtoday = datetime.datetime(2020, 12, 12)
								mytime = datetime.datetime.strptime('0500','%H%M').time()
								start_time = datetime.datetime.combine(today, mytime)
								# start_time='20201010050000'
								mytime = datetime.datetime.strptime('1800','%H%M').time()
								end_time = datetime.datetime.combine(today, mytime)
								
								seconds_=(end_time-start_time).seconds

								today_gen=[]
								# inv_sl_data=[]
								

								for inv_ in data:
									
									cursor.execute("SELECT * from solar_panel_data,gateway where gateway.api_key=%s and gateway.admin_id=%s and solar_panel_data.EID=%s and solar_panel_data.DID=1 and solar_panel_data.ID=%s and solar_panel_data.api_key=%s ORDER by solar_panel_data.my_id desc limit 1",(api_key,access_id,inv_['equipment_id'],inv_['slave_id'],api_key))
									inv_data1=cursor.fetchone()

									cursor.execute("SELECT * from solar_panel_data,gateway where gateway.api_key=%s and gateway.admin_id=%s and solar_panel_data.EID=%s and solar_panel_data.DID=2 and solar_panel_data.ID=%s and solar_panel_data.api_key=%s and solar_panel_data.TIME_STAMP>=%s ORDER by solar_panel_data.my_id desc limit 1",(api_key,access_id,inv_['equipment_id'],inv_['slave_id'],api_key,inv_data1['TIME_STAMP']))
									inv_data2=cursor.fetchone()
									# print('inv_data1',inv_data1,'inv_data2',inv_data2)

									if( inv_data2!=None)&( inv_data1!=None) :
										time_diff=timedate-inv_data1['lastchange']

										start_time=datetime.datetime.now() +datetime.timedelta(days=1)
										start_time = start_time.replace(hour=5, minute=0, second=0, microsecond=0)
										end_time= timedate.replace(hour=20, minute=0, second=0, microsecond=0)

										if (time_diff)>(datetime.timedelta(minutes=10)) or ((timedate>=end_time)&(timedate<=start_time)):
											inv_data1={'ID':inv_['slave_id'],'EID':inv_['equipment_id'],'connect_status':'offline'}
											inv_data2={'ID':inv_['slave_id'],'EID':inv_['equipment_id'],'connect_status':'offline'}
											eng_list = [inv_data1,inv_data2]
											merge_inv = {}
											for k in inv_data1.keys():
											  merge_inv[k] = tuple(merge_inv[k] for merge_inv in eng_list)

											# print(merge_inv)
											inv_sl_data.append(merge_inv)
										else:
											con_status={'connect_status':'online'}
											inv_data1_=inv_data1.update(con_status)
											inv_data2_=inv_data2.update(con_status)
											
											eng_list = [inv_data1,inv_data2]
											merge_inv = {}
											for k in inv_data1.keys():
											  merge_inv[k] = tuple(merge_inv[k] for merge_inv in eng_list)

											# print(merge_inv)
											inv_sl_data.append(merge_inv)
									else:
										# print('inv_data1',inv_data1,'inv_data2',inv_data2)
										inv_data1={'ID':inv_['slave_id'],'EID':inv_['equipment_id'],'connect_status':'offline'}
										inv_data2={'ID':inv_['slave_id'],'EID':inv_['equipment_id'],'connect_status':'offline'}
										eng_list = [inv_data1,inv_data2]
										merge_inv = {}
										for k in inv_data1.keys():
										  merge_inv[k] = tuple(merge_inv[k] for merge_inv in eng_list)

										# print(merge_inv)
										inv_sl_data.append(merge_inv)
							
					return make_response(jsonify({'message':"successfull",'poa_data':poa_data,'inv_sl_data':inv_sl_data,'inv_data':inv_data,'data':result,'college_details':college_details}),200)
				# except Exception as e:
				# 	return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)
	# ======================================================================== Edit wind and weather ==========================

class edit_w_w(Resource):
	"""docstring for create_smb"""
	@inventory_token
	def put(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id=request.json['id']
				access_id=rights()['admin_id']
				w_w=request.json['w_w']
				addedon=today
				capacity=request.json['capacity']
				admin=request.json['admin']
				status=request.json['status']
				groupadmin=request.json['groupadmin']
				adminid=request.json['adminid']
				lastchange=timedate
				

				if status=='active':
					status='active'
				else:
					status='inactive'

				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from w_w where id=%s and admin_id=%s",(id,access_id))
					id_check=cursor.fetchone()

					if id_check!=None:

						cursor.execute("UPDATE w_w set w_w=%s,capacity=%s,admin=%s,status=%s,lastchange=%s,groupadmin=%s where id=%s",(w_w,capacity,admin,status,lastchange,groupadmin,id))
						connection.commit()

						return {'message':'Successfully Updated'},200
					else:
						return{'message':'id doesnot exit in database'},400

				except Exception as e:
					return{'Error Message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return{"message":"Not authorized"},401
		else:
			return{"message":'Something Wrong Please Logout And Login Again'},400

	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id=request.json['id']
				access_id=rights()['admin_id']
				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from w_w where id=%s and admin_id=%s",(id,access_id))
					result=cursor.fetchone()
					data=[]

					if result!=None:

						id=result['id']
						w_w=result['w_w']
						addedon=str(result['addedon'])
						capacity=result['capacity']
						admin=result['admin']
						status=result['status']
						lastchange=str(result['lastchange'])
						data.append({'id':id,"addedon":addedon,'w_w':w_w,'capacity':capacity,'admin':admin,'status':status,'lastchange':lastchange})
					
						return {'message':data}
					else:
						return{'message':'ID Invalid'}
				except Exception as e:
					return{'Error Message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return{"message":"Not authorized"},401
		else:
			return{"message":'Something Wrong Please Logout And Login Again'},400
	# ======================================================================== status wind and weather ==========================

class status_w_w(Resource):
	"""docstring for create_w_w"""
	@inventory_token
	def put(self):

		if rights()!=None:
			access=rights()['access']
			
			if access=='super_admin':

				id=request.json['id']
				access_id=rights()['admin_id']
				status=request.json['status']
				lastchange=timedate

				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from w_w where id=%s and admin_id=%s",(id,access_id))
					id_check=cursor.fetchone()

					if id_check!=None:

						cursor.execute("UPDATE w_w set status=%s,lastchange=%s where id=%s",(status,lastchange,id))
						connection.commit()

						return {'message':'Successfully Updated'},200

					else:
						return{'message':'id doesnot exit in database'},400

				except Exception as e:
					return{'Error Message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return{"message":"Not authorized"},401
		else:
			return{"message":'Something Wrong Please Logout And Login Again'},400


# ======================================================================== create admin_group ==========================

class create_admin_group(Resource):
	"""docstring for create_admin_group"""
	@inventory_token
	def post(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':
				access_id=rights()['admin_id']
				name=request.json['name']
				addedon=today
				username=request.json['username']
				password=request.json['password']
				logo='null'
				address=request.json['address']
				dc_capacity=request.json['dc_capacity']
				# role=request.json['role']
				# allot_admin=request.json['allot_admin']
				# notification=request.json['notification']
				status=request.json['status']
				lastchange=timedate
				
				password_hash=password_encryption(password)

				if status=='active':
					status='active'
				else:
					status='inactive'


				try:
					connection=get_connection()
					cursor=connection.cursor()
					
					check=username_check(username)
					
					if check['message']==True:
						cursor.execute("INSERT into admin_group value(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(name,addedon,username,password,status,lastchange,access_id,address,logo,dc_capacity))
						connection.commit()
						account_id=cursor.lastrowid
						return make_response(jsonify({'message':'Successfully Created','account_id':account_id}),200)
					else:
						return make_response(jsonify({"message":check['message']}),400)

				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

	# ======================================================================== Edit admin group ==========================
	@inventory_token
	def put(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':
				access_id=rights()['admin_id']
				id=request.json['id']
				name=request.json['name']
				addedon=today
				username=request.json['username']
				password=request.json['password']
				address=request.json['address']
				dc_capacity=request.json['dc_capacity']
				# role=request.json['role']
				# allot_admin=request.json['allot_admin']
				# notification=request.json['notification']
				status=request.json['status']
				lastchange=timedate
				
				password_hash=password_encryption(password)

				if status=='active':
					status='active'
				else:
					status='inactive'


				try:
					connection=get_connection()
					cursor=connection.cursor()
					
					check=username_check(username)
					
					if check['message']==True:
						cursor.execute("UPDATE admin_group set name=%s,username=%s,status=%s,lastchange=%s,address=%s,dc_capacity=%s where id=%s",(name,username,status,lastchange,address,dc_capacity,id))
						connection.commit()
						if password!="":
							cursor.execute("UPDATE admin_group set password=%s where id=%s",(password_hash,id))
							connection.commit()
						return make_response(jsonify({'message':'Successfully Updated'}),200)
					else:
						cursor.execute("UPDATE admin_group set name=%s,status=%s,lastchange=%s,address=%s,dc_capacity=%s where id=%s",(name,status,lastchange,address,dc_capacity,id))
						connection.commit()
						if password!="":
							cursor.execute("UPDATE admin_group set password=%s where id=%s",(password_hash,id))
							connection.commit()
						return make_response(jsonify({"message":'Successfully Updated'}),400)

				# except Exception as e:
				# 	return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

	@inventory_token
	def delete(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id=request.json['id']
				access_id=rights()['admin_id']
				
				try:
					connection=get_connection()
					cursor=connection.cursor()
					
					cursor.execute("DELETE from admin_group where id=%s",(id))
					connection.commit()

					return make_response(jsonify({'message':'successfull'}),200)

				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)
		# ======================================================================== view admin group ==========================

class view_admin_group(Resource):
	"""docstring for view_admin"""
	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				
				try:
					connection=get_connection()
					cursor=connection.cursor()
					access_id=rights()['admin_id']
					cursor.execute("SELECT * from admin_group where  admin_group.super_id=%s",(access_id))
					result=cursor.fetchall()

					return make_response(jsonify({'message':'successfull',"data":result}),200)
				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

	# ======================================================================== Edit admin group ==========================

class edit_admin_group(Resource):
	
	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id =request.json['id']
				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from admin_group where id=%s",(id))
					result=cursor.fetchone()
					data=[]

					if result!=None:

						id=result['id']
						name=result['name']
						addedon=str(result['addedon'])
						username=result['username']
						password=result['password']
						status=result['status']
						lastchange=str(result['lastchange'])
						notification=result['notification']
						allot_admin=result['allot_admin']
						role=result['role']

						data.append({'id':id,"addedon":addedon,'name':name,'username':username,'password':password,'status':status,'lastchange':lastchange,"notification":notification,'allot_admin':allot_admin,'role':role})
					
					return {'message':data}
				except Exception as e:
					return{'Error Message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return{"message":"Not authorized"},401
		else:
			return{"message":'Something Wrong Please Logout And Login Again'},400

	# ======================================================================== status admin group ==========================

class status_admin_group(Resource):
	"""docstring for create_admin_group"""
	@inventory_token
	def put(self):

		if rights()!=None:
			access=rights()['access']
			
			if access=='super_admin':
				access_id=rights()['admin_id']
				id=request.json['id']
				status=request.json['status']
				lastchange=timedate

				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from admin_group where id=%s and super_id=%s",(id,access_id))
					id_check=cursor.fetchone()

					if id_check!=None:

						cursor.execute("UPDATE admin_group set status=%s,lastchange=%s where id=%s",(status,lastchange,id))
						connection.commit()

						return {'message':'Successfully Updated'},200

					else:
						return{'message':'id doesnot exit in database'},400

				except Exception as e:
					return{'Error Message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return{"message":"Not authorized"},401
		else:
			return{"message":'Something Wrong Please Logout And Login Again'},400



# ======================================================================== create support ==========================

class create_support(Resource):
	"""docstring for create_support"""
	@inventory_token
	def post(self):

		if rights()!=None:
			access=rights()['access']
			access_id=rights()['admin_id']

			if access=='super_admin':

				name=request.json['name']
				admin=request.json['admin']
				title=request.json['title']
				description=request.json['description']
				# alloted_to=','.join(map(str, request.json['alloted_to']))
				user_list=request.json['user_list']
				status=request.json['status']
				remarks=request.json['remarks']
				periority=request.json['type']
				due_date=request.json['due_date']
				allotted_time=timedate
				
				# if status=='open':
				# 	status='open'
				# elif status=='close':
				# 	status='close'
				# elif status=='process':
				# 	status='process'
				# else:
				# 	return {"message":"Invalid status"},400

				# if periority=='high':
				# 	periority='high'
				# elif periority=='low':
				# 	periority='low'
				# elif periority=='medium':
				# 	periority='medium'
				# else:
				# 	return {"message":"Invalid periority"},400

				try:
					connection=get_connection()
					cursor=connection.cursor()
					
					cursor.execute("INSERT into support value(null,%s,%s,%s,%s,%s,null,%s,%s,%s,%s,%s)",(admin,name,title,description,status,allotted_time,remarks,periority,due_date,access_id))
					connection.commit()
					support_id=cursor.lastrowid
					for account_id in user_list:
						cursor.execute("INSERT into alloted_to value(null,%s,%s)",(support_id,account_id))
						connection.commit()
					return make_response(jsonify({'message':'Successfully Created'}),200)

				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

	@inventory_token
	def put(self):

		if rights()!=None:
			access=rights()['access']
			access_id=rights()['admin_id']

			if access=='super_admin':

				id=request.json['id']
				name=request.json['name']
				admin=request.json['admin']
				title=request.json['title']
				description=request.json['description']
				# alloted_to=','.join(map(str, request.json['alloted_to']))
				user_list=request.json['user_list']
				status=request.json['status']
				remarks=request.json['remarks']
				periority=request.json['type']
				due_date=request.json['due_date']
				allotted_time=timedate
				
				# if status=='open':
				# 	status='open'
				# elif status=='close':
				# 	status='close'
				# elif status=='process':
				# 	status='process'
				# else:
				# 	return {"message":"Invalid status"},400

				# if periority=='high':
				# 	periority='high'
				# elif periority=='low':
				# 	periority='low'
				# elif periority=='medium':
				# 	periority='medium'
				# else:
				# 	return {"message":"Invalid periority"},400

				try:
					connection=get_connection()
					cursor=connection.cursor()
					
					cursor.execute("UPDATE support set admin=%s,name=%s,title=%s,description=%s,status=%s,remarks=%s,periority=%s,due_date=%s where id=%s",(admin,name,title,description,status,remarks,periority,due_date,id))
					cursor.execute("DELETE from alloted_to where support_id=%s",(id))
					connection.commit()
					support_id=id
					for account_id in user_list:
						cursor.execute("INSERT into alloted_to value(null,%s,%s)",(support_id,account_id))
						connection.commit()
					return make_response(jsonify({'message':'Successfully Created'}),200)

				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

	@inventory_token
	def delete(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id=request.json['id']
				access_id=rights()['admin_id']
				
				try:
					connection=get_connection()
					cursor=connection.cursor()
					
					cursor.execute("DELETE from support where id=%s",(id))
					cursor.execute("DELETE from alloted_to where support_id=%s",(id))
					connection.commit()

					return make_response(jsonify({'message':'successfull'}),200)

				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)
# ======================================================================== view support ==========================

class view_support(Resource):
	"""docstring for view_admin"""
	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']
			access_id=rights()['admin_id']

			if access=='super_admin':

				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from support where admin_id=%s",(access_id))
					result=cursor.fetchall()
					
					return make_response(jsonify({'message':'successfull','data':result}),200)
				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)
# ======================================================================== view alloted_to ==========================

class view_alloted_to(Resource):
	"""docstring for view_admin"""
	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from alloted_to")
					result=cursor.fetchall()
					
					return make_response(jsonify({'message':'successfull','data':result}),200)
				# except Exception as e:
				# 	return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

	# ======================================================================== Edit support ==========================

class edit_support(Resource):
	"""docstring for create_smb"""
	@inventory_token
	def put(self):

		if rights()!=None:
			access=rights()['access']
			access_id=rights()['admin_id']

			if access=='super_admin':

				id=request.json['id']
				admin=request.json['admin']
				description=request.json['description']
				# alloted_to=str(request.json['alloted_to'])
				allotedList=request.json['alloted_to']
				status=request.json['status']
				# allotted_time=request.json['allotted_time']
				completed_on=request.json['completed_on']
				remarks=request.json['remarks']
				periority=request.json['periority']
				due_date=request.json['due_date']
				

				if status=='open':
					status='open'
				elif status=='close':
					status='close'
				elif status=='process':
					status='process'
				else:
					return {"message":"Invalid status"},400

				if periority=='high':
					periority='high'
				elif periority=='low':
					periority='low'
				elif periority=='medium':
					periority='medium'
				else:
					return {"message":"Invalid periority"},400

				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from support where id=%s and admin_id=%s",(id,access_id))
					id_check=cursor.fetchone()

					if id_check!=None:

						cursor.execute("UPDATE support set admin=%s,description=%s,status=%s,completed_on=%s,remarks=%s,periority=%s,due_date=%s where id=%s",(admin,description,status,completed_on,remarks,periority,due_date,id))
						connection.commit()
						# print(allotedList)
						# print(id)
						cursor.execute("delete from alloted_to where support_id=%s",(id))
						for account_id in allotedList:
							# print(account_id)
							cursor.execute("INSERT into alloted_to value(null,%s,%s)",(id,account_id))
							connection.commit()
						return {'message':'Successfully Updated'},200
					else:
						return{'message':'id doesnot exit in database'},400

				except Exception as e:
					return{'Error Message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return{"message":"Not authorized"},401
		else:
			return{"message":'Something Wrong Please Logout And Login Again'},400

	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id=request.json['id']
				access_id=rights()['admin_id']
				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from support where id=%s and admin_id=%s",(id,access_id))
					result=cursor.fetchone()
					data=[]

					if result!=None:

						id=result['id']
						admin=result['admin']
						description=result['description']
						alloted_to=result['alloted_to']
						allotted_time=str(result['allotted_time'])
						completed_on=str(result['completed_on'])
						remarks=result['remarks']
						periority=result['periority']
						due_date=str(result['due_date'])
						status=result['status']
						
						data.append({'id':id,"admin":admin,'description':description,'alloted_to':alloted_to,'allotted_time':allotted_time,'completed_on':completed_on,'status':status,'remarks':remarks,'periority':periority,'due_date':due_date})
					
						return {'message':data}
					else:
						return{"message":'ID Invalid'}

				except Exception as e:
					return{'Error Message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return{"message":"Not authorized"},401
		else:
			return{"message":'Something Wrong Please Logout And Login Again'},400
# ======================================================================== create accounts ==========================

class create_accounts(Resource):
	"""docstring for create_accounts"""
	@inventory_token
	def post(self):

		if rights()!=None:
			access=rights()['access']
			access_id=rights()['admin_id']

			if access=='super_admin':
				
				name = request.json['name']
				description=request.json['description']
				account_cat=request.json['account_cat']
				date_added=timedate
				admin=(request.json['admin'])
				status=request.json['status']
				remarks=request.json['remarks']
				amount=request.json['amount']
				fileName = request.json['fileName']
			   
				# print(name)
				if status=='Submitted':
					status='Submitted'
				else:
					return {"message":"Invalid status"},400

				try:
					connection=get_connection()
					cursor=connection.cursor()
					attachment=fileName
					cursor.execute("INSERT into accounts value(null,%s,%s,%s,%s,%s,%s,null,null,%s,%s,%s,%s)",(name,admin,description,account_cat,date_added,status,attachment,remarks,access_id,amount))
					connection.commit()
					account_id=cursor.lastrowid

					return make_response(jsonify({'message':'Successfully Created','account_id':account_id}),200)

				# except Exception as e:
				# 	return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

	@inventory_token
	def put(self):

		if rights()!=None:
			access=rights()['access']
			access_id=rights()['admin_id']

			if access=='super_admin':
				
				id = request.json['id']
				name = request.json['name']
				description=request.json['description']
				account_cat=request.json['account_cat']
				date_added=timedate
				admin=(request.json['admin'])
				status=request.json['status']
				remarks=request.json['remarks']
				amount=request.json['amount']
				
			   
				if status=='Hold':
					status='Hold'
				elif status=='Approved':
					status='Approved'
				elif status=='Rejected':
					status='Rejected'
				else:
					status='Submitted'
					
				try:
					connection=get_connection()
					cursor=connection.cursor()
					cursor.execute("UPDATE accounts set name=%s,admin=%s,description=%s,account_cat=%s,status=%s,remarks=%s,amount=%s where id=%s",(name,admin,description,account_cat,status,remarks,amount,id))
					connection.commit()
					account_id=id

					return make_response(jsonify({'message':'Successfully Created','account_id':account_id}),200)

				# except Exception as e:
				# 	return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

	@inventory_token
	def delete(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id=request.json['id']
				access_id=rights()['admin_id']
				
				try:
					connection=get_connection()
					cursor=connection.cursor()
					
					cursor.execute("DELETE from accounts where id=%s",(id))
					connection.commit()

					return make_response(jsonify({'message':'successfull'}),200)

				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)
# ======================================================================== view admin ==========================

class view_accounts(Resource):
	"""docstring for view_admin"""
	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']
			access_id=rights()['admin_id']

			if access=='super_admin':

				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from accounts,account_catagory,admin where admin.id=accounts.admin and  account_catagory.id=accounts.account_cat and accounts.admin_id=%s",(access_id))
					result=cursor.fetchall()
					
					return make_response(jsonify({'message':'successfull','data':result}),200)
				except Exception as e:
					return make_response(jsonify({'Error Message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)
	# ======================================================================== Edit accounts ==========================

class edit_accounts(Resource):
	"""docstring for create_smb"""
	@inventory_token
	def put(self):

		if rights()!=None:
			access=rights()['access']
			access_id=rights()['admin_id']

			if access=='super_admin':

				
				file = request.files.get('file')
				id=request.form.get('id')
				name = request.form.get('name')
				description=request.form.get('description')
				account_head=request.form.get('account_head')
				edited_on=timedate
				approved_by=request.form.get('approved_by')
				admin=request.form.get('admin')
				status=request.form.get('status')
				remarks=request.form.get('remarks')
				fileName = request.form.get('fileName')
				

				if status=='submitted':
					status='submitted'
				elif status=='approved':
					status='approved'
				elif status=='reject':
					status='reject'
				else:
					return {"message":"Invalid status"},400

				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from accounts where id=%s and admin_id=%s",(id,access_id))
					id_check=cursor.fetchone()

					if id_check!=None:
						attachment = 'upload/{}'.format(fileName)
						file.save(os.path.join('upload', fileName))
						cursor.execute("UPDATE accounts set name=%s,admin=%s,description=%s,account_cat=%s,status=%s,edited_on=%s,approved_by=%s,attachment=%s,remarks=%s where id=%s",(name,admin,description,account_head,status,edited_on,approved_by,attachment,remarks,id))
						connection.commit()
						return {'message':'Successfully Updated'},200
					else:
						return{'message':'id doesnot exit in database'},400

				except Exception as e:
					return{'Error Message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return{"message":"Not authorized"},401
		else:
			return{"message":'Something Wrong Please Logout And Login Again'},400

	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id=request.json['id']
				access_id=rights()['admin_id']
				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from accounts where id=%s and admin_id=%s",(id,access_id))
					result=cursor.fetchone()
					data=[]

					if result!=None:

						id=result['id']
						name=result['name']
						admin=result['admin']
						description=result['description']
						date_added=str(result['date_added'])
						edited_on=str(result['edited_on'])
						account_head=result['account_head']
						approved_by=result['approved_by']
						attachment=str(result['attachment'])
						status=result['status']
						remarks=result['remarks']
						
						data.append({'id':id,"admin":admin,'name':name,'description':description,'date_added':date_added,'edited_on':edited_on,'status':status,'account_head':account_head,'approved_by':approved_by,'attachment':attachment,'remarks':remarks})
					
						return {'message':data}
					else:
						return{'message':"ID Invalid"}

				except Exception as e:
					return{'Error Message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return{"message":"Not authorized"},401
		else:
			return{"message":'Something Wrong Please Logout And Login Again'},400
	# ======================================================================== status accounts ==========================

class status_accounts(Resource):
	"""docstring for create_smb"""
	@inventory_token
	def put(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id=request.json['id']
				access_id=rights()['admin_id']
				status=request.json['status']
				edited_on=request.json['edited_on']
				approved_by=request.json['approved_by']
				remarks=request.json['remarks']
				

				if status=='submitted':
					status='submitted'
				elif status=='approved':
					status='approved'
				elif status=='reject':
					status='reject'
				else:
					return {"message":"Invalid status"},400

				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from accounts where id=%s and admin_id=%s",(id,access_id))
					id_check=cursor.fetchone()

					if id_check!=None:

						
						cursor.execute("UPDATE accounts set status=%s,edited_on=%s,approved_by=%s,remarks=%s where id=%s",(status,edited_on,approved_by,remarks,id))
						connection.commit()

						return {'message':'Successfully Updated'},200
					else:
						return{'message':'id doesnot exit in database'},400

				except Exception as e:
					return{'Error Message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return{"message":"Not authorized"},401
		else:
			return{"message":'Something Wrong Please Logout And Login Again'},400

# ======================================================================== solar_panel data ==========================
sms_status_={"Gateway": 1, "Inverter": 1, "vcb": 1}
class solar_panel_data(Resource):
	"""docstring for create_smb"""
	# @inventory_token
	def post(self):

		
		
		api_key=request.json['api_key']
		S_NO=request.json['S_NO']
		IP=request.json['IP']
		DID=request.json['DID']
		EID=request.json['EID']
		ID=request.json['ID']
		FC=request.json['FC']
		ADDRESS=request.json['ADDRESS']
		QUANTITY=request.json['QUANTITY']
		TIME_STAMP=request.json['TIME_STAMP']
		FIELD0=request.json['FIELD0']
		FIELD1=request.json['FIELD1']
		FIELD2=request.json['FIELD2']
		FIELD3=request.json['FIELD3']
		FIELD4=request.json['FIELD4']
		FIELD5=request.json['FIELD5']
		FIELD6=request.json['FIELD6']
		FIELD7=request.json['FIELD7']
		FIELD8=request.json['FIELD8']
		FIELD9=request.json['FIELD9']
		FIELD10=request.json['FIELD10']
		FIELD11=request.json['FIELD11']
		FIELD12=request.json['FIELD12']
		FIELD13=request.json['FIELD13']
		FIELD14=request.json['FIELD14']
		FIELD15=request.json['FIELD15']
		FIELD16=request.json['FIELD16']
		FIELD17=request.json['FIELD17']
		FIELD18=request.json['FIELD18']
		FIELD19=request.json['FIELD19']
		FIELD20=request.json['FIELD20']
		FIELD21=request.json['FIELD21']
		FIELD22=request.json['FIELD22']
		FIELD23=request.json['FIELD23']
		FIELD24=request.json['FIELD24']
		FIELD25=request.json['FIELD25']
		FIELD26=request.json['FIELD26']
		FIELD27=request.json['FIELD27']
		FIELD28=request.json['FIELD28']
		FIELD29=request.json['FIELD29']
		FIELD30=request.json['FIELD30']
		FIELD31=request.json['FIELD31']
		FIELD32=request.json['FIELD32']
		FIELD33=request.json['FIELD33']
		FIELD34=request.json['FIELD34']
		FIELD35=request.json['FIELD35']
		FIELD36=request.json['FIELD36']
		FIELD37=request.json['FIELD37']
		FIELD38=request.json['FIELD38']
		FIELD39=request.json['FIELD39']
		lastchange=timedate
		

		try:
			connection=get_connection()
			cursor=connection.cursor()

			cursor.execute("SELECT * from gateway where api_key=%s ",(api_key))
			api_check=cursor.fetchone()

			if api_check!=None:
				cursor.execute("INSERT into solar_panel_data value(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(api_key,S_NO,IP,DID,EID,ID,FC,ADDRESS,QUANTITY,TIME_STAMP,FIELD0,FIELD1,FIELD2,FIELD3,FIELD4,FIELD5,FIELD6,FIELD7,FIELD8,FIELD9,FIELD10,FIELD11,FIELD12,FIELD13,FIELD14,FIELD15,FIELD16,FIELD17,FIELD18,FIELD19,FIELD20,FIELD21,FIELD22,FIELD23,FIELD24,FIELD25,FIELD26,FIELD27,FIELD28,FIELD29,FIELD30,FIELD31,FIELD32,FIELD33,FIELD34,FIELD35,FIELD36,FIELD37,FIELD38,FIELD39,lastchange))
				connection.commit()
				lastrowid=cursor.lastrowid
				# print("API Added Successfully :",lastrowid)
				# ====================== Live Data DEtection =================
				start_time=datetime.datetime.now() +datetime.timedelta(days=1)
				start_time = start_time.replace(hour=5, minute=0, second=0, microsecond=0)
				end_time= timedate.replace(hour=19, minute=0, second=0, microsecond=0)
							
				# print('api timing',timedate,end_time,start_time)
				# if (time_diff)>(datetime.timedelta(minutes=10)) or ((timedate>=end_time)&(timedate<=start_time)):
				if ((timedate>=end_time)&(timedate<=start_time)):
					pass
				else:
					# print("API Checking line enter ")
					
					#============================ ABB Inverter ==========================================
					if ((int(float(EID)==1)) & (int(float(DID)==1)) & (int(float(FIELD0)==0)) & (int(float(FIELD1)==0)) & (int(float(FIELD2)==0)) & (int(float(FIELD3)==0)) & (int(float(FIELD4)==0)) & (int(float(FIELD5)==0)) & (int(float(FIELD6)==0)) & (int(float(FIELD7)==0)) & (int(float(FIELD8)==0)) & (int(float(FIELD9)==0)) & (int(float(FIELD10)==0)) & (int(float(FIELD11)==0)) & (int(float(FIELD12)==0)) & (int(float(FIELD13)==0)) & (int(float(FIELD14)==0)) & (int(float(FIELD15)==0)) & (int(float(FIELD16)==0)) & (int(float(FIELD17)==0)) & (int(float(FIELD18)==0)) & (int(float(FIELD19)==0)) & (int(float(FIELD20)==0)) & (int(float(FIELD21)==0)) & (int(float(FIELD22)==0)) & (int(float(FIELD23)==0)) & (int(float(FIELD24)==0)) & (int(float(FIELD25)==0)) & (int(float(FIELD26)==0)) & (int(float(FIELD27)==0)) & (int(float(FIELD28)==0)) & (int(float(FIELD29)==0)) & (int(float(FIELD30)==0)) & (int(float(FIELD31)==0)) & (int(float(FIELD32)==0)) & (int(float(FIELD33)==0)) & (int(float(FIELD34)==0)) & (int(float(FIELD35)==0)) & (int(float(FIELD36)==0)) & (int(float(FIELD37)==0)) & (int(float(FIELD38)==0)) & (int(float(FIELD39)==0) )):
						
						# print("API Checking line enter Inverter")

						if (int(ID)==81):
							Status="ABB Inverter 01 Trip or Data Loss"
						elif (int(ID)==82):
							Status="ABB Inverter 02 Trip or Data Loss"
						elif (int(ID)==83):
							Status="ABB Inverter 03 Trip or Data Loss"
						elif (int(ID)==84):
							Status="ABB Inverter 04 Trip or Data Loss"
						elif (int(ID)==85):
							Status="ABB Inverter 05 Trip or Data Loss"
						elif (int(ID)==86):
							Status="ABB Inverter 06 Trip or Data Loss"

						# message="Service Alert: VET PV Date: "+str(today)+" Time:"+str(timedate)+" Status: ABB Inverter 01- 06 Trip or Data loss Description: Please check inverter or SCADA connectivity -SECSMS"
						message="Service Alert: VET PV Date:"+str(today)+" Time:"+str(timedate)+" Status:"+Status+"Description: Please check inverter or SCADA connectivity -SECSMS"
						# Template_id=1707162411054704156
						Template_id=1707162411081473392

						switch_status=sms_switch('Inverter',0,sms_status_)
						# print(switch_status)
						if switch_status==True:
							# print("Posses to message delivery")
							sms_status=sms(message,Template_id)
							# print("sms status",sms_status)
					else:
						# print("API Checking else line enter Inverter")
						sms_switch('Inverter',1,sms_status_)
					#============================ VCB Connection ==========================================
					# print(type(EID),type(DID),type(FIELD0))

					if ((int(float(EID)==20)) & (int(float(DID)==1)) & (int(float(FIELD0)==0)) & (int(float(FIELD1)==0)) & (int(float(FIELD2)==0)) & (int(float(FIELD3)==0)) & (int(float(FIELD4)==0)) & (int(float(FIELD5)==0)) & (int(float(FIELD6)==0)) & (int(float(FIELD7)==0)) & (int(float(FIELD8)==0)) & (int(float(FIELD9)==0)) & (int(float(FIELD10)==0)) & (int(float(FIELD11)==0)) & (int(float(FIELD12)==1)) & (int(float(FIELD13)==0)) & (int(float(FIELD14)==0)) & (int(float(FIELD15)==0)) & (int(float(FIELD16)==0)) & (int(float(FIELD17)==0)) & (int(float(FIELD18)==0)) & (int(float(FIELD19)==0)) & (int(float(FIELD20)==0)) & (int(float(FIELD21)==0)) & (int(float(FIELD22)==0)) & (int(float(FIELD23)==0)) & (int(float(FIELD24)==0)) & (int(float(FIELD25)==0)) & (int(float(FIELD26)==0)) & (int(float(FIELD27)==0)) & (int(float(FIELD28)==0)) & (int(float(FIELD29)==0)) & (int(float(FIELD30)==0)) & (int(float(FIELD31)==0)) & (int(float(FIELD32)==0)) & (int(float(FIELD33)==0)) & (int(float(FIELD34)==0)) & (int(float(FIELD35)==0)) & (int(float(FIELD36)==0)) & (int(float(FIELD37)==0)) & (int(float(FIELD38)==0)) & (int(float(FIELD39)==0) )):
						# print("============================ vcb connection =================",ID)
						if (int(ID)==111):
							# print("pass1")
							Status="HT Breaker VCB ICR 01 Trip "
						elif (int(ID)==112):
							# print("psss2")
							Status="HT Breaker VCB ICR 02 Trip "
						elif (int(ID)==113):
							# print("psss3")
							Status="HT Breaker VCB  MCR Trip "
						# else:
						# 	Status="empty"
						# message="Service Alert: VET PV Date: "+str(today)+" Time:"+str(timedate)+" Status: HT Breaker VCB / ICR 01 / ICR 02 /MCR Trip Description: Please check HT Incomer –SECSMS"
						message="Service Alert: VET PV Date:"+str(today)+" Time:"+str(timedate)+" Status:"+Status+' Description: Please check HT Incomer –SECSMS'
						# print("========================message===================",message)
						# Template_id=1707162411061920618
						Template_id=1707162411081473392
						
						switch_status=sms_switch('vcb',0,sms_status_)
						# print(switch_status)
						if switch_status==True:
							# print("Posses to message delivery")
							sms_status=sms(message,Template_id)
							# print("sms status",sms_status)
					else:
						# print("API Checking else line enter vcp")
						sms_switch('vcb',1,sms_status_)
						# =========================== Empty Data Error ========================================

					if ((int(float(FIELD0)==0)) & (int(float(FIELD1)==0)) & (int(float(FIELD2)==0)) & (int(float(FIELD3)==0)) & (int(float(FIELD4)==0)) & (int(float(FIELD5)==0)) & (int(float(FIELD6)==0)) & (int(float(FIELD7)==0)) & (int(float(FIELD8)==0)) & (int(float(FIELD9)==0)) & (int(float(FIELD10)==0)) & (int(float(FIELD11)==0)) & (int(float(FIELD12)==0)) & (int(float(FIELD13)==0)) & (int(float(FIELD14)==0)) & (int(float(FIELD15)==0)) & (int(float(FIELD16)==0)) & (int(float(FIELD17)==0)) & (int(float(FIELD18)==0)) & (int(float(FIELD19)==0)) & (int(float(FIELD20)==0)) & (int(float(FIELD21)==0)) & (int(float(FIELD22)==0)) & (int(float(FIELD23)==0)) & (int(float(FIELD24)==0)) & (int(float(FIELD25)==0)) & (int(float(FIELD26)==0)) & (int(float(FIELD27)==0)) & (int(float(FIELD28)==0)) & (int(float(FIELD29)==0)) & (int(float(FIELD30)==0)) & (int(float(FIELD31)==0)) & (int(float(FIELD32)==0)) & (int(float(FIELD33)==0)) & (int(float(FIELD34)==0)) & (int(float(FIELD35)==0)) & (int(float(FIELD36)==0)) & (int(float(FIELD37)==0)) & (int(float(FIELD38)==0)) & (int(float(FIELD39)==0) )):
						
						# print("API Checking line enter Gateway")

						message="Service Alert: VET PV Date: "+str(today)+" Time: "+str(timedate)+" Status: Gateway disconnected or down Description: Please check the availability of power or internet – SECSMS"
						# message="Service Alert: VET PV Date: "+str(today)+" Time:"+str(timedate)+" Status: Gateway disconnected or down Description: Please check the availability of power or internet – SECSMS"
						Template_id=1707162411044570002

						switch_status=sms_switch('Gateway',0,sms_status_)
						# print(switch_status)
						if switch_status==True:
							# print("Posses to message delivery")
							sms_status=sms(message,Template_id)
							# print("sms status",sms_status)
					else:

						# print("API Checking else line enter Gateway")
						sms_switch('Gateway',1,sms_status_)

				return make_response(jsonify({'message':'Successful', 'id': lastrowid}),200)
			else:
				return make_response(jsonify({'message':'api key doesnot exit in database'}),400)


		except Exception as e:
			
			cursor.execute("INSERT into solar_panel_error_data value(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(api_key,S_NO,IP,DID,EID,ID,FC,ADDRESS,QUANTITY,TIME_STAMP,FIELD0,FIELD1,FIELD2,FIELD3,FIELD4,FIELD5,FIELD6,FIELD7,FIELD8,FIELD9,FIELD10,FIELD11,FIELD12,FIELD13,FIELD14,FIELD15,FIELD16,FIELD17,FIELD18,FIELD19,FIELD20,FIELD21,FIELD22,FIELD23,FIELD24,FIELD25,FIELD26,FIELD27,FIELD28,FIELD29,FIELD30,FIELD31,FIELD32,FIELD33,FIELD34,FIELD35,FIELD36,FIELD37,FIELD38,FIELD39,lastchange))
			connection.commit()
			return make_response(jsonify({'message':str(e)+'sl_error_data registerd'}),400)

		finally:
			cursor.close()
			connection.close()
	def get(self):
		try:
			connection=get_connection()
			cursor=connection.cursor()

			# cursor.execute("SELECT * from solar_panel_data where EID=2 or EID=3 or EID=4 ORDER by my_id DESC limit 1000")
			cursor.execute("SELECT * from solar_panel_data ORDER by my_id DESC limit 1000")
			# cursor.execute("SELECT * from solar_panel_data where DID=%s and EID=%s and ID=%s and lastchange>=%s",(101,21,91,20201125))
			sl_data=cursor.fetchall()

			csv_columns=['my_id','api_key','S_NO','IP','DID','EID','ID','FC','ADDRESS','QUANTITY','TIME_STAMP','FIELD0','FIELD1','FIELD2','FIELD3','FIELD4','FIELD5','FIELD6','FIELD7','FIELD8','FIELD9','FIELD10','FIELD11','FIELD12','FIELD13','FIELD14','FIELD15','FIELD16','FIELD17','FIELD18','FIELD19','FIELD20','FIELD21','FIELD22','FIELD23','FIELD24','FIELD25','FIELD26','FIELD27','FIELD28','FIELD29','FIELD30','FIELD31','FIELD32','FIELD33','FIELD34','FIELD35','FIELD36','FIELD37','FIELD38','FIELD39','lastchange']
			# with open("sl_data.csv", 'w') as csvfile:
			# 	writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
			# 	writer.writeheader()
			# 	for data in sl_data:
			# 		writer.writerow(data)


			if sl_data!=():
				return make_response(jsonify({'message':'Successfull',"data":sl_data}),200)
			else:
				return make_response(jsonify({'message':'data doesnot exit in database'}),400)

		except Exception as e:
			return make_response(jsonify({'message':str(e)}),400)

		finally:
			cursor.close()
			connection.close()


# ======================================================================== create catagory ==========================

class create_catagory(Resource):
	"""docstring for create_admin_group"""
	@inventory_token
	def post(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':
				access_id=rights()['admin_id']
				name=request.json['name']
				addedon=today
				type_=request.json['type']

				try:
					connection=get_connection()
					cursor=connection.cursor()
					
					cursor.execute("INSERT into account_catagory value(null,%s,%s,%s,%s)",(name,addedon,type_,access_id))
					connection.commit()

					return make_response(jsonify({'message':'Successfully Created'}),200)
					

				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

	@inventory_token
	def put(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':
				access_id=rights()['admin_id']
				id=request.json['id']
				name=request.json['name']
				addedon=today
				type_=request.json['type']

				try:
					connection=get_connection()
					cursor=connection.cursor()
					
					cursor.execute("UPDATE account_catagory set name=%s,type=%s where id=%s",(name,type_,id))
					connection.commit()

					return make_response(jsonify({'message':'Successfully Created'}),200)
					

				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

	@inventory_token
	def delete(self):

		if rights()!=None:
			access=rights()['access']

			if access=='super_admin':

				id=request.json['id']
				access_id=rights()['admin_id']
				
				try:
					connection=get_connection()
					cursor=connection.cursor()
					
					cursor.execute("DELETE from account_catagory where id=%s",(id))
					connection.commit()

					return make_response(jsonify({'message':'successfull'}),200)

				except Exception as e:
					return make_response(jsonify({'message':str(e)}),400)

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

class view_catagory(Resource):
	"""docstring for view_admin"""
	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']
			access_id=rights()['admin_id']

			if access=='super_admin':

				try:
					connection=get_connection()
					cursor=connection.cursor()

					cursor.execute("SELECT * from account_catagory where super_id=%s",(access_id))
					result=cursor.fetchall()
					
					
					return make_response(jsonify({'message':"successfull",'data':result}))
				except Exception as e:
					return{'Error Message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

class abj_solar_panel_data(Resource):
	"""docstring for view_admin"""
	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']
			access_id=rights()['admin_id']

			if access=='admin':

				try:
					connection=get_connection()
					cursor=connection.cursor()
					data=request.json['smb_data']
					ajb_sl_data=[]

					for i in data:
						# print("===========================",i['slave_id'],i['equipment_id'])
						cursor.execute("SELECT * from solar_panel_data where ID=%s and EID=%s ORDER BY my_id DESC LIMIT 1 ",(int(i['slave_id']),float(i['equipment_id'])))
						sl_data=cursor.fetchone()
						
						if sl_data!=None:
							# ------------------------------------------------ off -------------------------------------------
							today = datetime.datetime(2021, 6, 27)
							endtoday = datetime.datetime(2021, 6, 26)
							mytime = datetime.datetime.strptime('0500','%H%M').time()
							start_time = datetime.datetime.combine(today, mytime)
							mytime = datetime.datetime.strptime('2300','%H%M').time()
							end_time = datetime.datetime.combine(endtoday, mytime)
							date_time = datetime.datetime.strptime('1000','%H%M').time()
							timedate_ = datetime.datetime.combine(today, date_time)
							# ------------------------------------------------------ -------------------------------------------
					
							time_diff=timedate_-sl_data['lastchange']

							start_time=datetime.datetime.now() +datetime.timedelta(days=1)
							start_time = start_time.replace(hour=5, minute=0, second=0, microsecond=0)
							end_time= timedate.replace(hour=20, minute=0, second=0, microsecond=0)
							
							
							# print(timedate.time())
							# print(time_diff,'time diff',datetime.timedelta(minutes=10),'timedate',timedate_,'end time',end_time,'start time',start_time)
							if (time_diff)>(datetime.timedelta(minutes=10)) or ((timedate_>=end_time)&(timedate_<=start_time)):
								
								offline_data={'ID':i['slave_id'],'connect_status':'offline','TIME_STAMP':sl_data['TIME_STAMP']}
								ajb_sl_data.append(offline_data)
							else:
								add_dict={'connect_status':'online'}
								sl_datas=sl_data.update(add_dict)
								ajb_sl_data.append(sl_data)
						else:
							offline_data={'ID':i['slave_id'],'connect_status':'offline'}
							ajb_sl_data.append(offline_data)
					
					if ajb_sl_data!=[]:
						return make_response(jsonify({'message':'Successfull',"data":ajb_sl_data}),200)
					else:
						return make_response(jsonify({'message':'data doesnot exit in database'}),400)

				# except Exception as e:
				# 	return{'message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

# ============================================= current graph 
class current_solar_panel_data(Resource):
	"""docstring for view_admin"""
	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']
			access_id=rights()['admin_id']

			if access=='admin':

				try:
					connection=get_connection()
					cursor=connection.cursor()
					data=request.json['inv_data']
					data2=request.json['w_w_data']
					type_=request.json['type_']
					from_date=request.json['from_date']
					to_date=request.json['to_date']
					# api_key="c8DrAnUs"
					
					cursor.execute("SELECT * from gateway where admin=%s",(access_id))
					api_key=cursor.fetchone()['api_key']

					# mytime = datetime.datetime.strptime('0500','%H%M').time()
					# start_time = datetime.datetime.combine(today, mytime)

					# ------------------------------------------------ off -------------------------------------------
					today = datetime.datetime(2021, 6, 27)
					endtoday = datetime.datetime(2021, 6, 27)
					mytime = datetime.datetime.strptime('0500','%H%M').time()
					start_time = datetime.datetime.combine(today, mytime)
					mytime = datetime.datetime.strptime('2300','%H%M').time()
					end_time = datetime.datetime.combine(endtoday, mytime)
					# ------------------------------------------------------ -------------------------------------------

					cursor.execute("SELECT * from solar_panel_data where api_key=%s ORDER by my_id desc limit 1",(api_key))
					last_data=cursor.fetchone()

					current_graph_data=dict()
					
					
					for i in data:
						if type_=='ALL':
							
							cursor.execute("SELECT * from solar_panel_data where EID=%s and DID=1 and ID=%s and api_key=%s and TIME_STAMP>=%s and TIME_STAMP<=%s ",(i['equipment_id'],i['slave_id'],api_key,from_date,to_date))
							inv_data2=cursor.fetchall()
						else:
							cursor.execute("SELECT * from solar_panel_data where EID=%s and DID=1 and ID=%s and api_key=%s and TIME_STAMP>=%s and TIME_STAMP<=%s ",(i['equipment_id'],i['slave_id'],api_key,start_time,end_time))
							inv_data2=cursor.fetchall()
							# print(type_,i['equipment_id'],i['slave_id'],"------------------- Start time -----------------",start_time,end_time,the_timedate)
							# print(from_date,to_date)
							# print(inv_data2)
							# print(__kani)

						for j in inv_data2:
							current=j['FIELD2']
							date=str(j['TIME_STAMP'])
							# print(current)
							# print(__kani)
							if current <= 60000.0:
								if date not in current_graph_data:
									current_graph_data[date]={'value':0}
									current_graph_data[date]['value']=current
								else:
									# print(date,'===============',current)
									current_graph_data[date]['value']+=current

					poa_graph_data=dict()
					for i in data2:
						if type_=='ALL':
							cursor.execute("SELECT * from solar_panel_data where EID=%s and ID=%s and api_key=%s and TIME_STAMP>=%s and TIME_STAMP<=%s",(i['equipment_id'],i['slave_id'],api_key,from_date,to_date))
							poa_data_=cursor.fetchall()
						else:
							cursor.execute("SELECT * from solar_panel_data where EID=%s and ID=%s and api_key=%s and TIME_STAMP>=%s and TIME_STAMP<=%s",(i['equipment_id'],i['slave_id'],api_key,start_time,end_time))
							poa_data_=cursor.fetchall()

						for j in poa_data_:
							poa_=j['FIELD14']
							date=str(j['TIME_STAMP'])
							if date not in poa_graph_data:
								poa_graph_data[date]={'value':0}
								poa_graph_data[date]['value']=poa_
							else:
								poa_graph_data[date]['value']+=poa_

					# print('graph_datas',current_graph_data)
					# print('poa_graph_datas',poa_graph_data)
					
					cursor.execute("SELECT * from solar_panel_data where EID=%s and ID=%s and api_key=%s ORDER by my_id desc limit 1",(i['equipment_id'],i['slave_id'],api_key))
					irradiation=cursor.fetchone()['FIELD14']

					return make_response(jsonify({'message':'Successfull','last_data':last_data,"current_graph_data":current_graph_data,"poa_graph_data":poa_graph_data,'irradiation':irradiation}),200)
					

				# except Exception as e:
				# 	return{'message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)


class inverter_solar_panel_data(Resource):
	"""docstring for view_admin"""
	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']
			access_id=rights()['admin_id']

			if access=='admin':

				try:
					connection=get_connection()
					cursor=connection.cursor()
					data=request.json['inv_data']
					# api_key="c8DrAnUs"
					# print("********************************************************************")
					
					cursor.execute("SELECT * from gateway where admin=%s",(access_id))
					api_key=cursor.fetchone()['api_key']
					# ------------------------------------------------ off -------------------------------------------
					today = datetime.datetime(2021, 6, 27)
					endtoday = datetime.datetime(2021, 6, 26)
					# ------------------------------------------------------------------------------------------------
					mytime = datetime.datetime.strptime('0500','%H%M').time()
					start_time = datetime.datetime.combine(today, mytime)
					date_time = datetime.datetime.strptime('1000','%H%M').time()
					timedate = datetime.datetime.combine(today, date_time)
					# start_time='20210620050000'
					# end_time='20210630050000'
					# ------------------------------------------------ on -------------------------------------------
					# mytime = datetime.datetime.strptime('1800','%H%M').time()
					# end_time = datetime.datetime.combine(today, mytime)
					# ------------------------------------------------ off -------------------------------------------
					mytime = datetime.datetime.strptime('2300','%H%M').time()
					end_time = datetime.datetime.combine(endtoday, mytime)
					# ------------------------------------------------------ -------------------------------------------
					
					seconds_=(end_time-start_time).seconds

					today_gen=[]
					inv_sl_data=[]
					

					for i in data:
						
						cursor.execute("SELECT * from solar_panel_data where EID=%s and DID=1 and ID=%s and api_key=%s ORDER by my_id desc limit 1",(i['equipment_id'],i['slave_id'],api_key))
						inv_data1=cursor.fetchone()

						cursor.execute("SELECT * from solar_panel_data where EID=%s and DID=2 and ID=%s and api_key=%s and TIME_STAMP>=%s ORDER by my_id desc limit 1",(i['equipment_id'],i['slave_id'],api_key,inv_data1['TIME_STAMP']))
						inv_data2=cursor.fetchone()
						# print('******************************* inv_data1',inv_data1,'inv_data2',inv_data2)

						# ------------------------ inv_data1 data -----------------------
						# print("SELECT * from solar_panel_data where EID={} and DID=1 and ID={} and api_key='{}'  ORDER by my_id desc limit 1".format(i['equipment_id'],i['slave_id'],api_key))
						# ------------------------ inv_data2 data -----------------------
						# print("SELECT * from solar_panel_data where EID={} and DID=2 and ID={} and api_key='{}' and TIME_STAMP>='{}' ORDER by my_id desc limit 1".format(i['equipment_id'],i['slave_id'],api_key,inv_data1['TIME_STAMP']))
						# print("time differnce",timedate,inv_data1['lastchange'])
						if( inv_data2!=None)&( inv_data1!=None) :
							time_diff=timedate-inv_data1['lastchange']

							start_time=datetime.datetime.now() +datetime.timedelta(days=1)
							start_time = start_time.replace(hour=5, minute=0, second=0, microsecond=0)
							end_time= timedate.replace(hour=20, minute=0, second=0, microsecond=0)
                            
                            # ------------------------------------------------ off -------------------------------------------
							today = datetime.datetime(2021, 6, 27)
							endtoday = datetime.datetime(2021, 6, 26)
							mytime = datetime.datetime.strptime('0500','%H%M').time()
							start_time = datetime.datetime.combine(today, mytime)
							mytime = datetime.datetime.strptime('2300','%H%M').time()
							end_time = datetime.datetime.combine(endtoday, mytime)
							# ------------------------------------------------------ -------------------------------------------
					

							# print("time differnce",time_diff,"time delta",datetime.timedelta(minutes=10),"timedate",timedate,"start_time",start_time,"end_time",end_time)
							if (time_diff)>(datetime.timedelta(minutes=10)) or ((timedate>=end_time)&(timedate<=start_time)):
								# print("kani")
								inv_data1={'ID':i['slave_id'],'EID':i['equipment_id'],'connect_status':'offline'}
								inv_data2={'ID':i['slave_id'],'EID':i['equipment_id'],'connect_status':'offline'}
								eng_list = [inv_data1,inv_data2]
								merge_inv = {}
								for k in inv_data1.keys():
								  merge_inv[k] = tuple(merge_inv[k] for merge_inv in eng_list)

								# print(merge_inv)
								inv_sl_data.append(merge_inv)
							else:
								con_status={'connect_status':'online'}
								inv_data1_=inv_data1.update(con_status)
								inv_data2_=inv_data2.update(con_status)
								
								eng_list = [inv_data1,inv_data2]
								merge_inv = {}
								for k in inv_data1.keys():
								  merge_inv[k] = tuple(merge_inv[k] for merge_inv in eng_list)

								# print(merge_inv)
								inv_sl_data.append(merge_inv)
						else:
							# print('inv_data1',inv_data1,'inv_data2',inv_data2)
							inv_data1={'ID':i['slave_id'],'EID':i['equipment_id'],'connect_status':'offline'}
							inv_data2={'ID':i['slave_id'],'EID':i['equipment_id'],'connect_status':'offline'}
							eng_list = [inv_data1,inv_data2]
							merge_inv = {}
							for k in inv_data1.keys():
							  merge_inv[k] = tuple(merge_inv[k] for merge_inv in eng_list)

							# print(merge_inv)
							inv_sl_data.append(merge_inv)

					if inv_sl_data!=[]:
						return make_response(jsonify({'message':'Successfull',"data":inv_sl_data,'tdy_gen':today_gen}),200)
					else:
						return make_response(jsonify({'message':'data doesnot exit in database'}),400)

				# except Exception as e:
				# 	return{'message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

class inverter_solar_panel_data_(Resource):
	"""docstring for view_admin"""
	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']
			access_id=rights()['admin_id']

			if access=='admin':

				try:
					connection=get_connection()
					cursor=connection.cursor()
					data=request.json['inv_data']
					to_date=request.json['to_date']
					# api_key="c8DrAnUs"
					
					cursor.execute("SELECT * from gateway where admin=%s",(access_id))
					api_key=cursor.fetchone()['api_key']

					# today = datetime.datetime(2020, 11, 10)
					# endtoday = datetime.datetime(2020, 12, 12)
					mytime = datetime.datetime.strptime('0500','%H%M').time()
					start_time = datetime.datetime.combine(today, mytime)
					# start_time='20201010050000'
					mytime = datetime.datetime.strptime('1800','%H%M').time()
					end_time = datetime.datetime.combine(today, mytime)
					
					seconds_=(end_time-start_time).seconds

					today_gen=[]
					inv_sl_data=[]
					
					for i in data:
						
						cursor.execute("SELECT * from solar_panel_data where EID=%s and DID=1 and ID=%s and api_key=%s and TIME_STAMP<=%s ORDER by my_id desc limit 1",(i['equipment_id'],i['slave_id'],api_key,to_date))
						inv_data1=cursor.fetchone()

						cursor.execute("SELECT * from solar_panel_data where EID=%s and DID=2 and ID=%s and api_key=%s and TIME_STAMP>=%s ORDER by my_id desc limit 1",(i['equipment_id'],i['slave_id'],api_key,inv_data1['TIME_STAMP']))
						inv_data2=cursor.fetchone()
						# print('inv_data1',inv_data1,'inv_data2',inv_data2)

						if( inv_data2!=None)&( inv_data1!=None) :
							time_diff=timedate-inv_data1['lastchange']

							con_status={'connect_status':'online'}
							inv_data1_=inv_data1.update(con_status)
							inv_data2_=inv_data2.update(con_status)
							
							eng_list = [inv_data1,inv_data2]
							merge_inv = {}
							for k in inv_data1.keys():
							  merge_inv[k] = tuple(merge_inv[k] for merge_inv in eng_list)

							# print(merge_inv)
							inv_sl_data.append(merge_inv)
						

					if inv_sl_data!=[]:
						return make_response(jsonify({'message':'Successfull',"data":inv_sl_data,'tdy_gen':today_gen}),200)
					else:
						return make_response(jsonify({'message':'data doesnot exit in database'}),400)

				# except Exception as e:
				# 	return{'message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

class engerymeter_solar_panel_data(Resource):
	"""docstring for view_admin"""
	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']
			access_id=rights()['admin_id']

			if access=='admin':

				try:
					connection=get_connection()
					cursor=connection.cursor()
					data=request.json['eng_data']
					# api_key="c8DrAnUs"
					
					cursor.execute("SELECT * from gateway where admin=%s",(access_id))
					api_key=cursor.fetchone()['api_key']

					eng_sl_data=[]
					
					for i in data:
						
						cursor.execute("SELECT * from solar_panel_data where EID=%s and DID=1 and ID=%s and api_key=%s ORDER by my_id desc limit 1",(i['equipment_id'],i['slave_id'],api_key))
						eng_data1=cursor.fetchone()

						cursor.execute("SELECT * from solar_panel_data where EID=%s and DID=2 and ID=%s and api_key=%s and TIME_STAMP>=%s ORDER by my_id desc limit 1",(i['equipment_id'],i['slave_id'],api_key,eng_data1['TIME_STAMP']))
						eng_data2=cursor.fetchone()

						cursor.execute("SELECT * from solar_panel_data where EID=%s and DID=3 and ID=%s and api_key=%s ORDER by my_id desc limit 1",(i['equipment_id'],i['slave_id'],api_key))
						eng_data3=cursor.fetchone()

						# print('eng_data1',eng_data1,'eng_data2',eng_data2)
						
						if( eng_data2!=None)&( eng_data1!=None)&(eng_data3!=None) :

							# ------------------------------------------------ off -------------------------------------------
							today = datetime.datetime(2021, 6, 27)
							endtoday = datetime.datetime(2021, 6, 26)
							mytime = datetime.datetime.strptime('0500','%H%M').time()
							start_time = datetime.datetime.combine(today, mytime)
							mytime = datetime.datetime.strptime('2300','%H%M').time()
							end_time = datetime.datetime.combine(endtoday, mytime)
							date_time = datetime.datetime.strptime('1000','%H%M').time()
							timedate = datetime.datetime.combine(today, date_time)
							# ------------------------------------------------------ -------------------------------------------
					
							time_diff=timedate-eng_data1['lastchange']
							# start_time=datetime.datetime.now() +datetime.timedelta(days=1)
							# start_time = start_time.replace(hour=5, minute=0, second=0, microsecond=0)
							# end_time= timedate.replace(hour=20, minute=0, second=0, microsecond=0)
							
							# print(timedate.time())
							if (time_diff)>(datetime.timedelta(minutes=10)) or ((timedate>=end_time)&(timedate<=start_time)):
								eng_data1={'ID':i['slave_id'],'EID':i['equipment_id'],'connect_status':'offline'}
								eng_data2={'ID':i['slave_id'],'EID':i['equipment_id'],'connect_status':'offline'}
								eng_data3={'ID':i['slave_id'],'EID':i['equipment_id'],'connect_status':'offline'}
								eng_list = [eng_data1,eng_data2,eng_data3]
								merge_eng = {}
								for k in eng_data1.keys():
								  merge_eng[k] = tuple(merge_eng[k] for merge_eng in eng_list)

								# print(merge_eng)
								eng_sl_data.append(merge_eng)
							else:
								con_status={'connect_status':'online'}
								eng_data1_=eng_data1.update(con_status)
								eng_data2_=eng_data2.update(con_status)
								eng_data3_=eng_data3.update(con_status)
								
								eng_list = [eng_data1,eng_data2,eng_data3]
								merge_eng = {}
								for k in eng_data1.keys():
								  merge_eng[k] = tuple(merge_eng[k] for merge_eng in eng_list)

								# print(merge_eng)
								eng_sl_data.append(merge_eng)
						else:
							# print('eng_data1',eng_data1,'eng_data2',eng_data2)
							eng_data1={'ID':i['slave_id'],'EID':i['equipment_id'],'connect_status':'offline'}
							eng_data2={'ID':i['slave_id'],'EID':i['equipment_id'],'connect_status':'offline'}
							eng_data3={'ID':i['slave_id'],'EID':i['equipment_id'],'connect_status':'offline'}
							eng_list = [eng_data1,eng_data2,eng_data3]
							merge_eng = {}
							for k in eng_data1.keys():
							  merge_eng[k] = tuple(merge_eng[k] for merge_eng in eng_list)

							# print(merge_eng)
							eng_sl_data.append(merge_eng)
						# print(eng_sl_data)
					vcb_slave_id=[111,112,113]
					vcb_check_data=[]

					for i in vcb_slave_id:
						# print(i,api_key)
						cursor.execute("SELECT * from solar_panel_data where EID=20 and DID=1 and ID=%s and api_key=%s ORDER by my_id desc limit 1",(i,api_key))
						vcb_check=cursor.fetchone()
						# print ("============================ vc checkkk",vcb_check)
						if i==111:
							if vcb_check!=None:
								if vcb_check['FIELD11']==1:
									vcb_check_data.append({'vcb':'VCB 1 - ICR 1','switch':'ON'})
									vcb1='ON'
								else:
									vcb1='OFF'
									vcb_check_data.append({'vcb':'VCB 1 - ICR 1','switch':'OFF'})
							else:	
									vcb1='OFF'
									vcb_check_data.append({'vcb':'VCB 1 - ICR 1','switch':'OFF'})

						if i==112:
							if vcb_check!=None:
								if vcb_check['FIELD11']==1:
									vcb2='ON'
									vcb_check_data.append({'vcb':'VCB 2 - ICR 2','switch':'ON'})
								else:
									vcb2='OFF'
									vcb_check_data.append({'vcb':'VCB 2 - ICR 2','switch':'OFF'})
							else:	
									vcb2='OFF'
									vcb_check_data.append({'vcb':'VCB 2 - ICR 2','switch':'OFF'})

						if i==113:
							if vcb1=="OFF" and vcb2=="OFF":
								vcb_check_data.append({'vcb':'GCB - MCR','switch':'OFF'})
							else:
								vcb_check_data.append({'vcb':'GCB - MCR','switch':'ON'})
							# if vcb_check!=None:
							# 	if vcb_check['FIELD11']==1:
							# 		vcb_check_data.append({'vcb':'GCB - MCR','switch':'ON'})
							# 	else:
							# 		vcb_check_data.append({'vcb':'GCB - MCR','switch':'OFF'})
							# else:
							# 		vcb_check_data.append({'vcb':'GCB - MCR','switch':'OFF'})
							


					# print("VCB Check DATA",vcb_check_data)
					if eng_sl_data!=[]:
						return make_response(jsonify({'message':'Successfull',"data":eng_sl_data,"vcb_check_data":vcb_check_data}),200)
					else:
						return make_response(jsonify({'message':'data doesnot exit in database'}),400)

				# except Exception as e:
				# 	return{'message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

class w_w_solar_panel_data(Resource):
	"""docstring for view_admin"""
	@inventory_token
	def get(self):

		if rights()!=None:
			access=rights()['access']
			access_id=rights()['admin_id']
			
			if access=='admin':

				try:
					connection=get_connection()
					cursor=connection.cursor()
					data=request.json['w_w_data']
					# api_key="c8DrAnUs"
					
					cursor.execute("SELECT * from gateway where admin=%s",(access_id))
					api_key=cursor.fetchone()['api_key']

					w_w_sl_data=[]
					poa_data=[]
					# print("data",data)
					for i in data:
						
						cursor.execute("SELECT * from solar_panel_data where EID=%s and ID=%s and api_key=%s ORDER by my_id desc limit 1",(i['equipment_id'],i['slave_id'],api_key))
						w_W_data1=cursor.fetchone()

						cursor.execute("SELECT sum(solar_panel_data.FIELD15) as poa_value from solar_panel_data where EID=%s and ID=%s and api_key=%s and lastchange>=%s",(i['equipment_id'],i['slave_id'],api_key,today))
						poa_data_=cursor.fetchone()
						if poa_data_['poa_value']==None:
							poa_data_['poa_value']=0
						# print('poa_data_',poa_data_)
						poa_data.append({'poa_value':poa_data_['poa_value'],'EID':i['equipment_id'],'ID':i['slave_id']})

						w_w_sl_data.append(w_W_data1)
					# print("poa_data",poa_data)
					if w_w_sl_data!=[]:
						return make_response(jsonify({'message':'Successfull',"data":w_w_sl_data,"poa_data":poa_data}),200)
					else:
						return make_response(jsonify({'message':'data doesnot exit in database'}),400)

				# except Exception as e:
				# 	return{'message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)


class data_visual(Resource):
	"""docstring for view_admin"""
	@inventory_token
	def post(self):

		if rights()!=None:
			access=rights()['access']
			access_id=rights()['admin_id']
			
			if access=='admin':

				try:
					connection=get_connection()
					cursor=connection.cursor()
					
					from_date=request.json['from_date']
					to_date=request.json['to_date']
					ajb=request.json['ajb']
					ajb_para=request.json['ajb_para']
					inv=request.json['inv']
					inv_para=request.json['inv_para']
					eng=request.json['eng']
					eng_para=request.json['eng_para']
					w_w=request.json['w_w']
					w_w_para=request.json['w_w_para']
					w_w_d=request.json['w_w_d']
					w_w_d_para=request.json['w_w_d_para']

					# print('result',eng,eng_para,from_date,to_date,type(from_date),type(to_date))
					cursor.execute("SELECT * from gateway where admin=%s",(access_id))
					api_key=cursor.fetchone()['api_key']
					
					ajb_data=dict()
					w_w_d_data=dict()
					inv_data_1=dict()
					inv_data_2=dict()
					eng_data_1=dict()
					eng_data_2=dict()
					eng_data_3=dict()
					

					report_ajb_data=[]
					for i in ajb:
						if i!='AJBS Option':
							cursor.execute("SELECT * from solar_panel_data,smb where solar_panel_data.api_key=%s and solar_panel_data.ID=smb.slave_id and solar_panel_data.EID=smb.equipment_id and smb.id=%s and TIME_STAMP>=%s and TIME_STAMP<=%s",(api_key,int(i),from_date,to_date))
							ajb=cursor.fetchall()
							ajb_data[i]={'data':ajb}

					for i in w_w_d:
						if i!='None':
							cursor.execute("SELECT * from solar_panel_data,w_w where solar_panel_data.api_key=%s and solar_panel_data.ID=w_w.slave_id and solar_panel_data.EID=w_w.equipment_id and w_w.id=%s and TIME_STAMP>=%s and TIME_STAMP<=%s",(api_key,int(i),from_date,to_date))
							w_w_d=cursor.fetchall()
							w_w_d_data[i]={'data':w_w_d}

					w_w_sl_data=[]
					poa_data=[]
					for i in w_w:
						if i!='None':
							cursor.execute("SELECT * from solar_panel_data,w_w where solar_panel_data.EID=w_w.equipment_id and solar_panel_data.ID=w_w.slave_id and solar_panel_data.api_key=%s and w_w.id=%s and solar_panel_data.TIME_STAMP<=%s ORDER by solar_panel_data.my_id desc limit 1",(api_key,i,to_date))
							w_W_data1=cursor.fetchone()

							cursor.execute("SELECT sum(solar_panel_data.FIELD15) as poa_value from solar_panel_data,w_w where solar_panel_data.EID=w_w.equipment_id and solar_panel_data.ID=w_w.slave_id and solar_panel_data.api_key=%s and w_w.id=%s and solar_panel_data.TIME_STAMP<=%s",(api_key,i,to_date))
							poa_data_=cursor.fetchone()

							poa_data.append({'poa_value':poa_data_['poa_value'],'EID':w_W_data1['equipment_id'],'ID':w_W_data1['slave_id']})

							w_w_sl_data.append(w_W_data1)

					for i in inv:
						if i!='Inverter Devices':
							cursor.execute("SELECT * from inverter where id =%s",(i))
							inv_r=cursor.fetchone()
							# print(inv_r)
							cursor.execute("SELECT * from solar_panel_data,inverter where solar_panel_data.api_key=%s and solar_panel_data.DID=1 and solar_panel_data.ID=inverter.slave_id and solar_panel_data.EID=inverter.equipment_id and inverter.id=%s and TIME_STAMP>=%s and TIME_STAMP<=%s",(api_key,int(i),from_date,to_date))
							inv1=cursor.fetchall()
							# print(inv1)
							inv_data_1[i]={'data':inv1}

							cursor.execute("SELECT * from solar_panel_data,inverter where solar_panel_data.api_key=%s and solar_panel_data.DID=2 and solar_panel_data.ID=inverter.slave_id and solar_panel_data.EID=inverter.equipment_id and inverter.id=%s and TIME_STAMP>=%s and TIME_STAMP<=%s",(api_key,int(i),from_date,to_date))
							inv2=cursor.fetchall()
							inv_data_2[i]={'data':inv2}
					# print(inv_data_2)

					remodified_inv_data=dict()
					
					if inv_data_1!={}:
						for i in inv_data_1:
							inv_data_list=[]
							for j in inv_data_1[i]['data']:
									inv_list=[]
									inv_list=j

									for ii in inv_data_2:
										for jj in inv_data_2[ii]['data']:
											# print(str(j['TIME_STAMP'])[:-3],"___________________",jj['FIELD1'],"________________",str(jj['TIME_STAMP'])[:-3])
											if (str(j['TIME_STAMP'])[:-3]== str(jj['TIME_STAMP'])[:-3]) and (i==ii):
												# print("safddsfdsafdsadfasdfdsafsdafdsafdsafdsadfas",ii)
												for kk in jj:
													if 'FIELD4' ==kk:
														# print("===================kk",kk)
														# print("-----------------",jj['FIELD4'])
														# print('-------------',inv_list)
														add_dict={'FIELD104':jj['FIELD4']}
														inv_list.update(add_dict)
														# print(']]]]]]]]]]]',inv_list)
														# print('[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]',jj)
														
													if 'FIELD1' ==kk:
														
														# print("===================kk2",kk)
														# print("===================================",jj['FIELD1'])
														add_dict={'FIELD101':jj['FIELD1']}
														inv_list.update(add_dict)
														# print(']]]]]]]]]]]2',inv_list)
														# print('[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]',jj)
														

													if 'FIELD2' ==kk:
														
														# print('-------------',inv_list)
														add_dict={'FIELD102':jj['FIELD2']}
														inv_list.update(add_dict)
														# print(']]]]]]]]]]]',remodified_inv_data)
														# print('[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]',jj)
														

													if 'FIELD3' ==kk:
														
														# print('-------------',inv_list)
														add_dict={'FIELD103':jj['FIELD3']}
														inv_list.update(add_dict)
														# print(']]]]]]]]]]]',remodified_inv_data)
														# print('[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]',jj)
														
													if 'FIELD7' ==kk:
														
														# print('-------------',inv_list)
														add_dict={'FIELD107':jj['FIELD7']}
														inv_list.update(add_dict)
														# print(']]]]]]]]]]]',remodified_inv_data)
														# print('[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]',jj)
														
													if 'FIELD5' ==kk:
														
														# print('-------------',inv_list)
														add_dict={'FIELD105':jj['FIELD5']}
														inv_list.update(add_dict)
														# print(']]]]]]]]]]]',remodified_inv_data)
														# print('[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]',jj)
														
													if 'FIELD10' ==kk:
														
														# print('-------------',inv_list)
														add_dict={'FIELD1010':jj['FIELD10']}
														inv_list.update(add_dict)
														# print(']]]]]]]]]]]',remodified_inv_data)
														# print('[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]',jj)
														
													if 'FIELD15' ==kk:
														
														# print('-------------',inv_list)
														add_dict={'FIELD115':jj['FIELD15']}
														inv_list.update(add_dict)
														# print(']]]]]]]]]]]',remodified_inv_data)
														# print('[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]',jj)
														
													if 'FIELD31' ==kk:
														
														# print('-------------',inv_list)
														add_dict={'FIELD131':jj['FIELD31']}
														inv_list.update(add_dict)
														# print(']]]]]]]]]]]',remodified_inv_data)
														# print('[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]',jj)
														
													if 'FIELD32' ==kk:
														
														# print('-------------',inv_list)
														add_dict={'FIELD132':jj['FIELD32']}
														inv_list.update(add_dict)
														# print(']]]]]]]]]]]',remodified_inv_data)
														# print('[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]',jj)
														
												inv_data_list.append(inv_list)
												# print('555555555555555555555555555555555555555555555',jj)
							# print(inv_data_list)
							remodified_inv_data[i]=dict()
							remodified_inv_data[i]['data']=inv_data_list	
							# print(remodified_inv_data)

					for i in eng:
						if i!='Energy Meter Options':
							# print(i)
							cursor.execute("SELECT * from solar_panel_data,energy_meter where solar_panel_data.api_key=%s and solar_panel_data.ID=energy_meter.slave_id and solar_panel_data.EID=energy_meter.equipment_id and energy_meter.id=%s and TIME_STAMP>=%s and TIME_STAMP<=%s",(api_key,int(i),from_date,to_date))
							eng1=cursor.fetchall()
							eng_data_1[i]={'data':eng1}

							cursor.execute("SELECT * from solar_panel_data,energy_meter where solar_panel_data.api_key=%s and solar_panel_data.ID=energy_meter.slave_id and solar_panel_data.EID=energy_meter.equipment_id and energy_meter.id=%s and TIME_STAMP>=%s and TIME_STAMP<=%s",(api_key,int(i),from_date,to_date))
							eng2=cursor.fetchall()
							eng_data_2[i]={'data':eng2}

							cursor.execute("SELECT * from solar_panel_data,energy_meter where solar_panel_data.api_key=%s and solar_panel_data.ID=energy_meter.slave_id and solar_panel_data.EID=energy_meter.equipment_id and energy_meter.id=%s and TIME_STAMP>=%s and TIME_STAMP<=%s",(api_key,int(i),from_date,to_date))
							eng3=cursor.fetchall()
							eng_data_3[i]={'data':eng3}

					remodified_eng_data=dict()
					if eng_data_1!={}:
						for i in eng_data_1:
							eng_data_list=[]
							for j in eng_data_1[i]['data']:
									eng_list=[]
									eng_list=j
									for ii in eng_data_2:
										for jj in eng_data_2[ii]['data']:
											if int(jj['DID'])==2:
												# print(i"safddsfdsafdsadfasdfdsafsdafdsafdsafdsadfas___________________",ii)
												if str(j['TIME_STAMP'])[:-3]== str(jj['TIME_STAMP'])[:-3] and (i==ii):
													# print(i,"safddsfdsafdsadfasdfdsafsdafdsafdsafdsadfas",i)
													for kk in jj:
														if 'FIELD32' ==kk:
															# print("===================kk",kk)
															# print("-----------------",jj['FIELD4'])
															# print('-------------',inv_list)
															add_dict={'FIELD132':jj['FIELD32']}
															eng_list.update(add_dict)
															# print(']]]]]]]]]]]',eng_list)
															# print('[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]',jj)
															
														if 'FIELD0' ==kk:
															
															# print("===================kk2",kk)
															# print("-----------------2",jj['FIELD4'])
															add_dict={'FIELD100':jj['FIELD0']}
															eng_list.update(add_dict)
															# print(']]]]]]]]]]]2',eng_list)
															# print('[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]',jj)
															

														if 'FIELD14' ==kk:
															
															# print('-------------',eng_list)
															add_dict={'FIELD114':jj['FIELD14']}

															# print(j['DID'],'=============================',jj['FIELD14'])
															eng_list.update(add_dict)
															# print(']]]]]]]]]]]',remodified_eng_data)
															# print('[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]',jj)
															

														if 'FIELD10' ==kk:
															
															# print('-------------',eng_list)
															add_dict={'FIELD110':jj['FIELD10']}
															eng_list.update(add_dict)
															# print(']]]]]]]]]]]',remodified_eng_data)
															# print('[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]',jj)
															
														if 'FIELD12' ==kk:
															
															# print('-------------',eng_list)
															add_dict={'FIELD112':jj['FIELD12']}
															eng_list.update(add_dict)
															# print(']]]]]]]]]]]',remodified_eng_data)
															# print('[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]',jj)
															
														if 'FIELD24' ==kk:
															
															# print('-------------',eng_list)
															add_dict={'FIELD124':jj['FIELD24']}
															eng_list.update(add_dict)
															# print(']]]]]]]]]]]',remodified_eng_data)
															# print('[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]',jj)
															
														if 'FIELD22' ==kk:
															
															# print('-------------',eng_list)
															add_dict={'FIELD122':jj['FIELD22']}
															eng_list.update(add_dict)
															# print(']]]]]]]]]]]',remodified_eng_data)
															# print('[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]',jj)
															
														if 'FIELD18' ==kk:
															
															# print(j['TIME_STAMP'],'-------------',jj['FIELD18'])
															add_dict={'FIELD118':jj['FIELD18']}
															eng_list.update(add_dict)
															# print(']]]]]]]]]]]',remodified_eng_data)
															# print('[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]',jj)
															
														if 'FIELD20' ==kk:
															
															# print('-------------',eng_list)
															add_dict={'FIELD120':jj['FIELD20']}
															eng_list.update(add_dict)
															# print(']]]]]]]]]]]',remodified_eng_data)
															# print('[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]',jj)
															
														if 'FIELD16' ==kk:
															
															# print('-------------',eng_list)
															add_dict={'FIELD116':jj['FIELD16']}
															eng_list.update(add_dict)
															# print(']]]]]]]]]]]',remodified_eng_data)
															# print('[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]',jj)
														if 'FIELD8' ==kk:
															
															# print('-------------',eng_list)
															add_dict={'FIELD108':jj['FIELD8']}
															eng_list.update(add_dict)
															# print(']]]]]]]]]]]',remodified_eng_data)
															# print('[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]',jj)
															
														if 'FIELD6' ==kk:
															
															# print('-------------',eng_list)
															add_dict={'FIELD106':jj['FIELD6']}
															eng_list.update(add_dict)
															# print(']]]]]]]]]]]',remodified_eng_data)
															# print('[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]',jj)
															
														if 'FIELD2' ==kk:
															
															# print('-------------',eng_list)
															add_dict={'FIELD102':jj['FIELD2']}
															eng_list.update(add_dict)
															# print(']]]]]]]]]]]',remodified_eng_data)
															# print('[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]',jj)
															
														if 'FIELD4' ==kk:
															
															# print('-------------',eng_list)
															add_dict={'FIELD104':jj['FIELD4']}
															eng_list.update(add_dict)
															# print(']]]]]]]]]]]',remodified_eng_data)
															# print('[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]',jj)
													eng_data_list.append(eng_list)

									for ii in eng_data_3:
										for jj in eng_data_3[ii]['data']:
											# print(str(j['TIME_STAMP']))
											if int(jj['DID'])==3:
												if str(j['TIME_STAMP'])[:-3]== str(jj['TIME_STAMP'])[:-3] and (i==ii):
													# print(i,"safddsfdsafdsadfasdfdsafsdafdsafdsafdsadfas",i)
													for kk in jj:
														if 'FIELD0' ==kk:
															# print("===================kk",kk)
															# print("-----------------",jj['FIELD4'])
															# print('-------------',eng_list)
															add_dict={'FIELD200':jj['FIELD0']}
															eng_list.update(add_dict)
															# print(']]]]]]]]]]]',eng_list)
															# print('[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]',jj)
														if 'FIELD2' ==kk:
															# print("===================kk",kk)
															# print("-----------------",jj['FIELD4'])
															# print('-------------',eng_list)
															add_dict={'FIELD202':jj['FIELD2']}
															eng_list.update(add_dict)
															# print(']]]]]]]]]]]',eng_list)
															# print('[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]',jj)
															
														
													eng_data_list.append(eng_list)

							# print(inv_data_list)
							remodified_eng_data[i]=dict()
							remodified_eng_data[i]['data']=remove_duplicate_dicts(eng_data_list)

					

					return make_response(jsonify({'message':'Successfull',"w_w_sl_data":w_w_sl_data,"poa_data":poa_data,"remodified_eng_data":remodified_eng_data,"remodified_inv_data":remodified_inv_data,"report_w_w_d_data":w_w_d_data,"report_ajb_data":ajb_data,"report_inv_data_1":inv_data_1,"report_inv_data_2":inv_data_2,"report_eng_data_1":eng_data_1,"report_eng_data_2":eng_data_2,"report_eng_data_3":eng_data_3}),200)
					# else:
					# 	return make_response(jsonify({'message':'data doesnot exit in database'}),400)

				# except Exception as e:
				# 	return{'message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)

class data_visual_graph(Resource):
	"""docstring for view_admin"""
	@inventory_token
	def post(self):

		if rights()!=None:
			access=rights()['access']
			access_id=rights()['admin_id']
			
			if access=='admin':

				try:
					connection=get_connection()
					cursor=connection.cursor()
					
					from_date=request.json['from_date']
					to_date=request.json['to_date']
					ajb=request.json['ajb']
					ajb_para=request.json['ajb_para']
					inv=request.json['inv']
					inv_para=request.json['inv_para']
					eng=request.json['eng']
					eng_para=request.json['eng_para']
					w_w=request.json['w_w']
					w_w_para=request.json['w_w_para']
					w_w_d=request.json['w_w_d']
					w_w_d_para=request.json['w_w_d_para']

					# print('result',eng,eng_para,from_date,to_date,type(from_date),type(to_date))
					cursor.execute("SELECT * from gateway where admin=%s",(access_id))
					api_key=cursor.fetchone()['api_key']
					
					ajb_data=dict()
					w_w_d_data=dict()
					inv_data_1=dict()
					inv_data_2=dict()
					eng_data_1=dict()
					eng_data_2=dict()
					eng_data_3=dict()

					final_ajb_data = []
					final_w_w_d_data = []
					final_inv_data = []
					final_eng_data = []

					for i in ajb:
						if i!='AJBS Option':
							cursor.execute("SELECT * from solar_panel_data,smb where solar_panel_data.api_key=%s and solar_panel_data.ID=smb.slave_id and solar_panel_data.EID=smb.equipment_id and smb.id=%s and TIME_STAMP>=%s and TIME_STAMP<=%s",(api_key,int(i),from_date,to_date))
							ajb=cursor.fetchall()
							ajb_data[i]={'data':ajb}

					for i in w_w_d:
						if i!='None':
							cursor.execute("SELECT * from solar_panel_data,w_w where solar_panel_data.api_key=%s and solar_panel_data.ID=w_w.slave_id and solar_panel_data.EID=w_w.equipment_id and w_w.id=%s and TIME_STAMP>=%s and TIME_STAMP<=%s",(api_key,int(i),from_date,to_date))
							w_w_d=cursor.fetchall()
							w_w_d_data[i]={'data':w_w_d}

					w_w_sl_data=[]
					poa_data=[]
					for i in w_w:
						if i!='None':
							cursor.execute("SELECT * from solar_panel_data,w_w where solar_panel_data.EID=w_w.equipment_id and solar_panel_data.ID=w_w.slave_id and solar_panel_data.api_key=%s and w_w.id=%s and solar_panel_data.TIME_STAMP<=%s ORDER by solar_panel_data.my_id desc limit 1",(api_key,i,to_date))
							w_W_data1=cursor.fetchone()

							cursor.execute("SELECT sum(solar_panel_data.FIELD15) as poa_value from solar_panel_data,w_w where solar_panel_data.EID=w_w.equipment_id and solar_panel_data.ID=w_w.slave_id and solar_panel_data.api_key=%s and w_w.id=%s and solar_panel_data.TIME_STAMP<=%s",(api_key,i,to_date))
							poa_data_=cursor.fetchone()

							poa_data.append({'poa_value':poa_data_['poa_value'],'EID':w_W_data1['equipment_id'],'ID':w_W_data1['slave_id']})

							w_w_sl_data.append(w_W_data1)

					for i in inv:
						if i!='Inverter Devices':
							cursor.execute("SELECT * from inverter where id =%s",(i))
							inv_r=cursor.fetchone()
							# print(inv_r)
							cursor.execute("SELECT * from solar_panel_data,inverter where solar_panel_data.api_key=%s and solar_panel_data.DID=1 and solar_panel_data.ID=inverter.slave_id and solar_panel_data.EID=inverter.equipment_id and inverter.id=%s and TIME_STAMP>=%s and TIME_STAMP<=%s",(api_key,int(i),from_date,to_date))
							inv1=cursor.fetchall()
							# print(inv1)
							inv_data_1[i]={'data':inv1}

							cursor.execute("SELECT * from solar_panel_data,inverter where solar_panel_data.api_key=%s and solar_panel_data.DID=2 and solar_panel_data.ID=inverter.slave_id and solar_panel_data.EID=inverter.equipment_id and inverter.id=%s and TIME_STAMP>=%s and TIME_STAMP<=%s",(api_key,int(i),from_date,to_date))
							inv2=cursor.fetchall()
							inv_data_2[i]={'data':inv2}
					# print(inv_data_2)

					

					for i in eng:
						if i!='Energy Meter Options':
							# print(i)
							cursor.execute("SELECT * from solar_panel_data,energy_meter where solar_panel_data.api_key=%s and solar_panel_data.ID=energy_meter.slave_id and solar_panel_data.EID=energy_meter.equipment_id and energy_meter.id=%s and TIME_STAMP>=%s and TIME_STAMP<=%s",(api_key,int(i),from_date,to_date))
							eng1=cursor.fetchall()
							eng_data_1[i]={'data':eng1}

							cursor.execute("SELECT * from solar_panel_data,energy_meter where solar_panel_data.api_key=%s and solar_panel_data.ID=energy_meter.slave_id and solar_panel_data.EID=energy_meter.equipment_id and energy_meter.id=%s and TIME_STAMP>=%s and TIME_STAMP<=%s",(api_key,int(i),from_date,to_date))
							eng2=cursor.fetchall()
							eng_data_2[i]={'data':eng2}

							cursor.execute("SELECT * from solar_panel_data,energy_meter where solar_panel_data.api_key=%s and solar_panel_data.ID=energy_meter.slave_id and solar_panel_data.EID=energy_meter.equipment_id and energy_meter.id=%s and TIME_STAMP>=%s and TIME_STAMP<=%s",(api_key,int(i),from_date,to_date))
							eng3=cursor.fetchall()
							eng_data_3[i]={'data':eng3}

					
					if ajb_data!={}:

						contents = ajb_data
						# print(ajb_para)
						plot_data = dict()
						for i in contents:
						    for j in contents[i]["data"]:
						        #print(j["TIME_STAMP"])
						        plot_data[j["TIME_STAMP"]] = dict()
						        for k in j:
                                                                for m in ajb_para:
                                                                    if m == k:
                                                                        if (m=='FIELD33') or (m=='FIELD34'):
                                                                                voltage=j[k]/10
                                                                                plot_data[j["TIME_STAMP"]][k] =voltage
                                                                        else:
                                                                                temperature=j[k]/100
                                                                                plot_data[j["TIME_STAMP"]][k] = temperature
						# print("plot_data",plot_data)
						graphs = list()
						for i in plot_data:
						    for j in plot_data[i]:
						        graphs.append(j)


						graphs = list(set(graphs))

						final_graph = dict()

						for graph in graphs:
							graph_name={"DC Current":"DC Current","DC ISOLATOR STATUS":"DC ISOLATOR STATUS","POWER":"POWER","SPD STATUS":"SPD STATUS","FIELD1":"STRING 1","FIELD2":"STRING 2","FIELD3":"STRING 3","FIELD4":"STRING 4","FIELD5":"STRING 5","FIELD6":"STRING 6","FIELD7":"STRING 7","FIELD8":"STRING 8","FIELD9":"STRING 9","FIELD10":"STRING 10","FIELD11":"STRING 11","FIELD12":"STRING 12","FIELD13":"STRING 13","FIELD14":"STRING 14","FIELD15":"STRING 15","FIELD16":"STRING 16","FIELD17":"STRING 17","FIELD18":"STRING 18","FIELD19":"STRING 19","FIELD20":"STRING 20","FIELD21":"STRING 21","FIELD22":"STRING 22","FIELD23":"STRING 23","FIELD24":"STRING 24","FIELD33":"TEMP1","FIELD34":"VOLTAGE"}

							final_graph[graph] = {"x": list(), "y": list(), "type": "scatter","name":str(graph_name[graph])}
							for i in plot_data:
								seconds = i.strftime("%Y-%m-%d %H:%M:%S")
								# seconds = dateparser.parse(i).strftime("%Y-%m-%d %H:%M:%S")
								final_graph[graph]["x"].append(seconds)
								final_graph[graph]["y"].append(plot_data[i][graph])

						
						for i in final_graph:
						    final_ajb_data.append(final_graph[i])

					if w_w_d_data!={}:

						contents = w_w_d_data
						# print(w_w_d_para)
						plot_data = dict()
						for i in contents:
						    for j in contents[i]["data"]:
						        #print(j["TIME_STAMP"])
						        plot_data[j["TIME_STAMP"]] = dict()
						        for k in j:
                                                                for m in w_w_d_para:
                                                                    if m == k:
                                                                        if m=='FIELD14':
                                                                                plot_data[j["TIME_STAMP"]][k] = j[k]/1000
                                                                        elif m=='FIELD15':
                                                                        		plot_data[j["TIME_STAMP"]][k]=j[k]/1000
                                                                        elif m=='FIELD4':
                                                                        		plot_data[j["TIME_STAMP"]][k]=j[k]
                                                                        else:
                                                                                plot_data[j["TIME_STAMP"]][k] = j[k]/10
						# print("plot_data",plot_data)
						graphs = list()
						for i in plot_data:
						    for j in plot_data[i]:
						        graphs.append(j)


						graphs = list(set(graphs))

						final_graph = dict()

						for graph in graphs:
							graph_name={"FIELD4":"Wind Speed","FIELD1":"Ambinet temperature","FIELD15":"POA","FIELD14":"GHA","FIELD21":"Bom Temperature"}

							final_graph[graph] = {"x": list(), "y": list(), "type": "scatter","name":str(graph_name[graph])}
							for i in plot_data:
								seconds = i.strftime("%Y-%m-%d %H:%M:%S")
								# seconds = dateparser.parse(i).strftime("%Y-%m-%d %H:%M:%S")
								final_graph[graph]["x"].append(seconds)
								final_graph[graph]["y"].append(plot_data[i][graph])

						
						for i in final_graph:
						    final_w_w_d_data.append(final_graph[i])

					if inv_data_1!={}:

						contents = inv_data_1
						# print(inv_data_1)
						plot_data = dict()
						plot_data1 = dict()
						for i in contents:
						    for j in contents[i]["data"]:
						        #print(j["TIME_STAMP"])
						        plot_data[j["TIME_STAMP"]] = dict()
						        for k in j:
                                                                for m in inv_para:
                                                                    if m == k:
                                                                        if m=='FIELD2':
                                                                                plot_data[j["TIME_STAMP"]][k] = j[k]
                                                                                # print(j["TIME_STAMP"])
                                                                        elif m=="FIELD5":
                                                                        		plot_data[j["TIME_STAMP"]][k] = j[k]/100
                                                                        elif m=="FIELD6":
                                                                        		plot_data[j["TIME_STAMP"]][k] = j[k]/1000
                                                                        elif m=="FIELD3":
                                                                        		# print(j[k])
                                                                        		if j[k]==65535.0:
                                                                        			# print(j[k])
                                                                        			plot_data[j["TIME_STAMP"]][k] = 0
                                                                        		else:
                                                                        			plot_data[j["TIME_STAMP"]][k] = j[k]/100
                                                                        else:
                                                                                plot_data[j["TIME_STAMP"]][k] = j[k]/10
						contents = inv_data_2
						for i in contents:
						    for j in contents[i]["data"]:
						        #print(j["TIME_STAMP"])
						        plot_data1[j["TIME_STAMP"]] = dict()
						        for k in j:
                                                                for m in inv_para:
                                                                    
                                                                        if m=='FIELD101':
                                                                        	if k=="FIELD1":
                                                                                        print(plot_data1[j["TIME_STAMP"]]	)
                                                                                        plot_data1[j["TIME_STAMP"]][m] = j[k]/10
                                                                                        # print(j["TIME_STAMP"])
                                                                        elif m=="FIELD102":
                                                                        	if k=="FIELD2":
                                                                        		plot_data1[j["TIME_STAMP"]][m] = j[k]/10
                                                                        elif m=="FIELD103":
                                                                        	if k=="FIELD3":
                                                                        		plot_data1[j["TIME_STAMP"]][m] = j[k]/10
                                                                        		# print(j["TIME_STAMP"])
                                                                        elif m=="FIELD1010":
                                                                        	if k=="FIELD10":
                                                                        		plot_data1[j["TIME_STAMP"]][m] = j[k]/10
                                                                        elif m=="FIELD104":
                                                                        	if k=="FIELD4":
                                                                        		plot_data1[j["TIME_STAMP"]][m] = j[k]/10
                                                                        elif m=="FIELD107":
                                                                        	if k=="FIELD7":
                                                                        		plot_data1[j["TIME_STAMP"]][m] = j[k]/10
                                                                        elif m=="FIELD105":
                                                                        	if k=="FIELD5":
                                                                        		plot_data1[j["TIME_STAMP"]][m] = j[k]/10
                                                                        elif m=="FIELD115":
                                                                        	if k=="FIELD15":
                                                                        		plot_data1[j["TIME_STAMP"]][m] = j[k]/10
                                                                        elif m=="FIELD132":
                                                                        	if k=="FIELD32":
                                                                        		plot_data1[j["TIME_STAMP"]][m] = j[k]/1000
                                                                        elif m=="FIELD131":
                                                                        	if k=="FIELD31":
                                                                        		# print('======================================',j[k]/10)
                                                                        		plot_data1[j["TIME_STAMP"]][m] = j[k]/1000		
                                                                        
						# print("plot_data",inv_para)
						graphs = list()
						for i in plot_data:
						    for j in plot_data[i]:
						        graphs.append(j)
						# print(plot_data1)
						for i in plot_data1:
						    for j in plot_data1[i]:
						        graphs.append(j)


						graphs = list(set(graphs))

						final_graph = dict()

						for graph in graphs:
							graph_name={"FIELD104":"AC CURRENT","FIELD5":"AC FREQUENCY","FIELD2":"AC POWER","FIELD4":"AC VOLTAGE","FIELD101":"AC VOLTAGE B-PHASE","FIELD102":"AC  VOLTAGE R-PHASE","FIELD103":"AC VOLTAGE Y-PHASE","FIELD1010":"CUBICLE TEMPERATURE","FIELD107":"DC CURRENT","FIELD105":"DC VOLTAGE","FIELD115":"HEAT SINK TEMPERATURE","FIELD6":"POWER FACTOR","FIELD3":"REACTIVE POWER","FIELD131":"TODAY GENERATION","FIELD132":"TOTAL GENERATION"}
							final_graph[graph] = {"x": list(), "y": list(), "type": "scatter","name":graph_name[graph]}
							for i in plot_data:
								try:
									seconds = i.strftime("%Y-%m-%d %H:%M:%S")
									# seconds = dateparser.parse(i).strftime("%Y-%m-%d %H:%M:%S")
									final_graph[graph]["x"].append(seconds)
									final_graph[graph]["y"].append(plot_data[i][graph])
								except:
									pass
							for i in plot_data1:
								try:
									seconds = i.strftime("%Y-%m-%d %H:%M:%S")
									# seconds = dateparser.parse(i).strftime("%Y-%m-%d %H:%M:%S")
									final_graph[graph]["x"].append(seconds)
									final_graph[graph]["y"].append(plot_data1[i][graph])
									# print(final_graph)
								except:
									pass
							    	
						for i in final_graph:
						    final_inv_data.append(final_graph[i])

					if eng_data_1!={}:

						contents = eng_data_1
						# print(eng_para)
						plot_data = dict()
						plot_data1 = dict()
						plot_data2 = dict()
						for i in contents:
						    for j in contents[i]["data"]:

						    	if int(j['DID'])==1:
							        # print(j["TIME_STAMP"])
							        plot_data[j["TIME_STAMP"]] = dict()
							        for k in j:
	                                                                for m in eng_para:
	                                                                    if m == k:
	                                                                        # print(m)
	                                                                        if m=='FIELD18':
	                                                                                print('=======================',j['TIME_STAMP'],j[k])
	                                                                                plot_data[j["TIME_STAMP"]][k] = j[k]
	                                                                                # print(j["TIME_STAMP"])
	                                                                        elif m=="FIELD14":
	                                                                        		plot_data[j["TIME_STAMP"]][k] = j[k]
	                                                                        elif m=="FIELD16":
	                                                                        		plot_data[j["TIME_STAMP"]][k] = j[k]
	                                                                        elif m=="FIELD20":
	                                                                        		plot_data[j["TIME_STAMP"]][k] = j[k]
	                                                                        elif m=="FIELD34":
	                                                                        		plot_data[j["TIME_STAMP"]][k] = j[k]
	                                                                        elif m=="FIELD38":
	                                                                        		plot_data[j["TIME_STAMP"]][k] = j[k]
	                                                                        elif m=="FIELD0":
	                                                                        		plot_data[j["TIME_STAMP"]][k] = j[k]
	                                                                        elif m=="FIELD2":
	                                                                        		plot_data[j["TIME_STAMP"]][k] = j[k]
	                                                                        elif m=="FIELD4":
	                                                                        		plot_data[j["TIME_STAMP"]][k] = j[k]
	                                                                        elif m=="FIELD6":
	                                                                        		plot_data[j["TIME_STAMP"]][k] = j[k]
	                                                                        elif m=="FIELD8":
	                                                                        		if j[k]>=10000:
	                                                                        			# print('==========================',j["TIME_STAMP"],j[k])
	                                                                        			plot_data[j["TIME_STAMP"]][k] = j[k]
	                                                                        elif m=="FIELD10":
	                                                                        		plot_data[j["TIME_STAMP"]][k] = j[k]
	                                                                        elif m=="FIELD12":
	                                                                        		plot_data[j["TIME_STAMP"]][k] = j[k]
	                                                                       
						# print('plost_data',eng_para)
						contents = eng_data_2
						for i in contents:
						    for j in contents[i]["data"]:
						    	if int(j['DID'])==2:
							        #print(j["TIME_STAMP"])
							        plot_data1[j["TIME_STAMP"]] = dict()
							        for k in j:
	                                                                for m in eng_para:
	                                                                    
	                                                                        if m=='FIELD132':
	                                                                        	if k=="FIELD32":
	                                                                                        plot_data1[j["TIME_STAMP"]][m] = j[k]
	                                                                                        # print(j["TIME_STAMP"])
	                                                                        elif m=="FIELD100":
	                                                                        	if k=="FIELD0":
	                                                                        		plot_data1[j["TIME_STAMP"]][m] = j[k]
	                                                                        elif m=="FIELD103":
	                                                                        	if k=="FIELD3":
	                                                                        		plot_data1[j["TIME_STAMP"]][m] = j[k]
	                                                                        		# print(j["TIME_STAMP"])
	                                                                        elif m=="FIELD110":
	                                                                        	if k=="FIELD10":
	                                                                        		plot_data1[j["TIME_STAMP"]][m] = j[k]
	                                                                        elif m=="FIELD112":
	                                                                        	if k=="FIELD12":
	                                                                        		plot_data1[j["TIME_STAMP"]][m] = j[k]
	                                                                        elif m=="FIELD114":
	                                                                        	if k=="FIELD14":
	                                                                        		plot_data1[j["TIME_STAMP"]][m] = j[k]
	                                                                        elif m=="FIELD116":
	                                                                        	if k=="FIELD16":
	                                                                        		plot_data1[j["TIME_STAMP"]][m] = j[k]
	                                                                        elif m=="FIELD118":
	                                                                        	if k=="FIELD18":
	                                                                        		plot_data1[j["TIME_STAMP"]][m] = j[k]
	                                                                        elif m=="FIELD120":
	                                                                        	if k=="FIELD20":
	                                                                        		plot_data1[j["TIME_STAMP"]][m] = j[k]
	                                                                        elif m=="FIELD122":
	                                                                        	if k=="FIELD22":
	                                                                        		plot_data1[j["TIME_STAMP"]][m] = j[k]
	                                                                        elif m=="FIELD124":
	                                                                        	if k=="FIELD24":
	                                                                        		plot_data1[j["TIME_STAMP"]][m] = j[k]
	                                                                        elif m=="FIELD102":
	                                                                        	if k=="FIELD2":
	                                                                        		plot_data1[j["TIME_STAMP"]][m] = j[k]
	                                                                        elif m=="FIELD104":
	                                                                        	if k=="FIELD4":
	                                                                        		plot_data1[j["TIME_STAMP"]][m] = j[k]
	                                                                        elif m=="FIELD106":
	                                                                        	if k=="FIELD6":
	                                                                        		plot_data1[j["TIME_STAMP"]][m] = j[k]
	                                                                        elif m=="FIELD108":
	                                                                        	if k=="FIELD8":
	                                                                        		plot_data1[j["TIME_STAMP"]][m] = j[k]

						# print('plost_data',plot_data)
						contents = eng_data_3
						for i in contents:
						    for j in contents[i]["data"]:
						    	if int(j['DID'])==3:
							        #print(j["TIME_STAMP"])
							        plot_data2[j["TIME_STAMP"]] = dict()
							        for k in j:
	                                                                for m in eng_para:
	                                                                    
	                                                                        if m=='FIELD200':
	                                                                        	if k=="FIELD0":
	                                                                                        plot_data2[j["TIME_STAMP"]][m] = j[k]
	                                                                                        # print(j["TIME_STAMP"])
	                                                                        elif m=='FIELD202':
	                                                                        	if k=="FIELD2":
	                                                                                        plot_data2[j["TIME_STAMP"]][m] = j[k]
	                                                                                        # print(j["TIME_STAMP"])
	                                                                        
                                                                        
						# print("plot_data",eng_para)
						graphs = list()
						for i in plot_data:
						    for j in plot_data[i]:
						        graphs.append(j)
						for i in plot_data1:
						    for j in plot_data1[i]:
						        graphs.append(j)
						for i in plot_data2:
						    for j in plot_data2[i]:
						        graphs.append(j)


						graphs = list(set(graphs))

						final_graph = dict()

						for graph in graphs:
							graph_name={"FIELD18":"C_B_PHASE","FIELD14":"C_R_PHASE","FIELD16":"C_Y_PHASE","FIELD20":"CURRENT TOTAL","FIELD132":"FREQUENCY","FIELD100":"PF_AVG","FIELD38":"PF_B_PHASE","FIELD34":"PF_R_PHASE","FIELD36":"PF_Y_PHASE","FIELD114":"VAR_B_PHASE","FIELD110":"VAR_R_PHASE","FIELD112":"VAR_Y_PHASE","FIELD124":"VA TOTAL","FIELD122":"VA_B_PHASE","FIELD118":"VA_R_PHASE","FIELD120":"VA_Y_PHASE","FIELD116":"VAR TOTAL","FIELD12":"VB_PHASE","FIELD4":"VBR_PHASE","FIELD8":"VR_PHASE","FIELD0":"VRY_PHASE","FIELD6":"VLN AVG","FIELD10":"VY_PHASE","FIELD2":"VYB_PHASE","FIELD108":"WATT_TOTAL","FIELD106":"WATTS_B_PHASE","FIELD102":"WATTS_R_PHASE","FIELD104":"WATTS_Y_PHASE","FIELD200":"WH_DELIVERED","FIELD202":"VAH_DELIVERED"}
							final_graph[graph] = {"x": list(), "y": list(), "type": "scatter","name":graph_name[graph]}
							for i in plot_data:
								try:
									seconds = i.strftime("%Y-%m-%d %H:%M:%S")
									# seconds = dateparser.parse(i).strftime("%Y-%m-%d %H:%M:%S")
									final_graph[graph]["x"].append(seconds)
									final_graph[graph]["y"].append(plot_data[i][graph])
								except:
									pass
							for i in plot_data1:
								try:
									seconds = i.strftime("%Y-%m-%d %H:%M:%S")
									# seconds = dateparser.parse(i).strftime("%Y-%m-%d %H:%M:%S")
									final_graph[graph]["x"].append(seconds)
									final_graph[graph]["y"].append(plot_data1[i][graph])
								except:
									pass
							for i in plot_data2:
								try:
									seconds = i.strftime("%Y-%m-%d %H:%M:%S")
									# seconds = dateparser.parse(i).strftime("%Y-%m-%d %H:%M:%S")
									final_graph[graph]["x"].append(seconds)
									final_graph[graph]["y"].append(plot_data2[i][graph])
								except:
									pass
							    	
						for i in final_graph:
						    final_eng_data.append(final_graph[i])
					# print('finally',final_ajb_data)
					return make_response(jsonify({'message':'Successfull',"final_w_w_d_data":final_w_w_d_data,"ajb_data":final_ajb_data,"inv_data":final_inv_data,"eng_data":final_eng_data}),200)
					# else:
					# 	return make_response(jsonify({'message':'data doesnot exit in database'}),400)

				# except Exception as e:
				# 	return{'message':str(e)},400

				finally:
					cursor.close()
					connection.close()
			else:
				return make_response(jsonify({"message":"Not authorized"}),401)
		else:
			return make_response(jsonify({"message":'Something Wrong Please Logout And Login Again'}),400)
