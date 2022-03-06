# SWAMI KARUPPASWAMI THUNNAI
from flask import send_file
from datetime import date, timedelta
import hashlib
import requests
from flask import request, redirect, url_for, session,flash,jsonify
from flask import render_template
from flask import Blueprint
import jwt
import random
import string
import os
import string
from io import BytesIO
from database.get_connection import get_connection
from inventory.token_validator import get_inventory_token, inventory_token
from inventory.power.rights import rights,password_encryption,username_check
from inventory.power.save import *
from sys import platform
import pytz

#salt
salt='jeeva$kani*vichu&69'
salt=hashlib.sha512(salt.encode("utf-8")).hexdigest()
#===============================================================================# Starts #========================================  


inventory = Blueprint("inventory", __name__, url_prefix="/solar_panel/")

today=date.today()
ist=pytz.timezone('Asia/Kolkata')
from pytz import timezone
from datetime import datetime
timedate =datetime.now(timezone('Asia/Kolkata'))
timedate=timedate.replace(tzinfo=None)
timedate=timedate
today=timedate.date()

# site_url="https://solarpanel.ai-being.com/api/"
if "linux" in platform:
	# site_url="https://solar.alliancetech.co.in/api/"
	site_url="https://solarpanel.ai-being.com/api/"
	# server_path="/var/www/data/"
	server_path="/var/www/solar-energy-monitor/static/"

else:
	site_url="http://127.0.0.1:5000/api/"
	server_path="D:\\projects\\Aibeing\\solar_panel_\\solar_panel\\static\\"


#===============================================================================# Login #========================================  
@inventory.route("/",methods=['POST','GET'])
def render_login():
	if request.method=="POST":
		username=request.form['username']
		password=request.form['password']
		
		url=site_url+'login'
		data={"username":username,
				"password":password
				}
		
		login_api=requests.post(url,json=data)
		
		result=login_api.json()
		if result['message']=="Login Successfull":
			session['inventory_token']=result['token']
			if rights()!=None:
				access=rights()['access']
				if( access=='super_admin'):
					return redirect(url_for("inventory.dashboard"))
				if( access=='controller'):
					return redirect(url_for("inventory.add_superadmin"))
				else:
					return redirect(url_for("inventory.plant",type_='today'))
		else:
			error_message=result['message']
			flash(error_message)

	username='admin@tpt.com'
	password='admin'
	
	url=site_url+'login'
	data={"username":username,
			"password":password
			}
	
	login_api=requests.post(url,json=data)
	
	result=login_api.json()
	# print(result)
	if result['message']=="Login Successfull":
		session['inventory_token']=result['token']
		if rights()!=None:
			access=rights()['access']
			if( access=='super_admin'):
				return redirect(url_for("inventory.dashboard"))
			if( access=='controller'):
				return redirect(url_for("inventory.add_superadmin"))
			else:
				return redirect(url_for("inventory.plant",type_='today'))
	
	# return render_template("inventory/login.html")
#===============================================================================# logout #========================================  
@inventory.route("/logout")
def logout():
	session.clear()
	return redirect(url_for('inventory.render_login'))
#===============================================================================# dashboard #========================================  
@inventory.route("/dashboard",methods=['POST','GET'])
@inventory_token
def dashboard():
	
	if rights()!=None:
		access=rights()['access']

		url=site_url+'view_admin'
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		
		if result['message']=="successfull":
			my_data=result['data']
			alloted_admin=result['admin_result']
		else:
			error_message=result['message']
			flash(error_message)
			my_data=None
			alloted_admin=""

		url=site_url+'view_admin_group'
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		print(result)
		if result['message']=="successfull":
			admingrp_data=result['data']

		else:
			error_message=result['message']
			flash(error_message)
			admingrp_data=""

		# ---------college details-----------
		url=site_url+'super_admin_view_w_w'
		
		data={'my_data':my_data}
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,json=data,headers=headers)
		result=data_api.json()
		# print(result)
		if result['message']=="successfull":
			w_w_data=result['data']
			college_details=result['college_details']
			inv_data=result['inv_data']
			inv_sl_data=result['inv_sl_data']
			poa_data=result['poa_data']
		else:
			error_message=result['message']
			flash(error_message)
			w_w_data=""
			college_details=""
			inv_data=""
			inv_sl_data=""
			poa_data=""

		# print("+++++++++++++++++college_details",college_details)
		if rights()!=None:
			access=rights()['access']
			access_id=rights()['admin_id']
			
			if access=='super_admin':
				return render_template("inventory/dashboard.html",poa_data=poa_data,inv_sl_data=inv_sl_data,inv_data=inv_data,w_w_data=w_w_data,college_details=college_details,alloted_admin=alloted_admin,my_data=my_data,access=access,access_id=access_id,admingrp_data=admingrp_data)
			else:
				return redirect(url_for("inventory.error_page"))
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))
	
#===============================================================================# admin #========================================  
@inventory.route("/add_admin",methods=['POST','GET'])
@inventory_token
def add_admin():
	if request.method=="POST":
		
		url=site_url+'create_admin'
		data={'name':request.form['name'],
				'username':request.form['username'],
				'password':request.form['password'],
				'location':request.form['location'],
				'address':request.form['address'],
				'lat_lon':request.form['lat_lon'],
				'status':request.form['status'],
				'admin_grp_list':request.form.getlist("teams")
				}
		
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.post(url,json=data,headers=headers)
		result=data_api.json()
		if result['message']=="Successfully Created":
			flash("Created Successfull")
		else:
			error_message=result['message']
			flash(error_message)

	url=site_url+'view_admin'
	headers={"x-access-token":session['inventory_token']}
	data_api=requests.get(url,headers=headers)
	result=data_api.json()
	
	if result['message']=="successfull":
		data=result['data']
		alloted_admin=result['admin_result']
	else:
		error_message=result['message']
		flash(error_message)
		data=None

	url=site_url+'view_admin_group'
	headers={"x-access-token":session['inventory_token']}
	data_api=requests.get(url,headers=headers)
	result=data_api.json()
	print(result)
	if result['message']=="successfull":
		admingrp_data=result['data']

	else:
		error_message=result['message']
		flash(error_message)
		admingrp_data=""

	if rights()!=None:
		access=rights()['access']
		access_id=rights()['admin_id']
		
		if access=='super_admin':
			return render_template("inventory/create_admin.html",alloted_admin=alloted_admin,data=data,access=access,access_id=access_id,admingrp_data=admingrp_data)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))

@inventory.route("/delete_admin/<int:id>",methods=['POST','GET'])
@inventory_token
def delete_admin(id):
	if rights()!=None:
		access=rights()['access']
		if request.method=="POST":

			url=site_url+'create_admin'
			data={  'id':id	}
			
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.delete(url,json=data,headers=headers)
			result=data_api.json()

			if result['message']=="successfull":
				flash("Delete Successfull")
			else:
				error_message=result['message']
				flash(error_message)
			return redirect(url_for("inventory.add_admin"))
		else:
			return redirect(url_for("inventory.add_admin"))
	else:
		return redirect(url_for("inventory.error_page"))

#===============================================================================# edit admin #========================================  
@inventory.route("/edit_admin/<int:id>",methods=['POST','GET'])
@inventory_token
def edit_admin(id):
	if request.method=="POST":
		
		url=site_url+'create_admin'
		data={'id':id,
				'name':request.form['name'],
				'username':request.form['username'],
				'password':request.form['password'],
				'location':request.form['location'],
				'address':request.form['address'],
				'lat_lon':request.form['lat_lon'],
				'status':request.form['status'],
				'admin_grp_list':request.form.getlist("teams")
				}
		
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.put(url,json=data,headers=headers)
		result=data_api.json()
		if result['message']=="Successfully Created":
			flash("Created Successfull")
		else:
			error_message=result['message']
			flash(error_message)

	url=site_url+'view_admin'
	headers={"x-access-token":session['inventory_token']}
	data_api=requests.get(url,headers=headers)
	result=data_api.json()
	
	if result['message']=="successfull":
		data=result['data']
		alloted_admin=result['admin_result']
	else:
		error_message=result['message']
		flash(error_message)
		data=None

	url=site_url+'view_admin_group'
	headers={"x-access-token":session['inventory_token']}
	data_api=requests.get(url,headers=headers)
	result=data_api.json()
	
	if result['message']=="successfull":
		admingrp_data=result['data']

	else:
		error_message=result['message']
		flash(error_message)
		admingrp_data=""
	# ================================================ multi choice option ======================		
	selected_admin=[]
	for i in alloted_admin:
		selected_admin.append(i['admin_grp_id'])

	print("+++++++++++===========selected_admin",selected_admin)
	admin_select_data=[]
	for i in admingrp_data:
		if i['id'] in selected_admin:
			admin_select_data.append({'id':i['id'],'name':i['name'],'type':'selected'})
		else:
			admin_select_data.append({'id':i['id'],'name':i['name'],'type':'unselected'})
	admingrp_data=admin_select_data
	print("+++++++++++===========admin_select_data",admin_select_data)

	if rights()!=None:
		access=rights()['access']
		access_id=rights()['admin_id']
		
		if access=='super_admin':
			return render_template("inventory/edit_admin.html",id=id,alloted_admin=alloted_admin,data=data,access=access,access_id=access_id,admingrp_data=admingrp_data)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))
#===============================================================================# super_admin #========================================  
@inventory.route("/add_superadmin",methods=['POST','GET'])
@inventory_token
def add_superadmin():
	if request.method=="POST":

		url=site_url+'create_super_admin'
		data={'name':request.form['name'],
				'username':request.form['username'],
				'password':request.form['password'],
				'location':request.form['location'],
				'status':request.form['status']
				}
		
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.post(url,json=data,headers=headers)
		result=data_api.json()
		if result['message']=="Successfully Created":
			flash("Created Successfull")
		else:
			error_message=result['message']
			flash(error_message)

	url=site_url+'view_super_admin'
	headers={"x-access-token":session['inventory_token']}
	data_api=requests.get(url,headers=headers)
	result=data_api.json()
	
	if result['message']=="successfull":
		data=result['data']
	else:
		error_message=result['message']
		flash(error_message)
		data=None
	if rights()!=None:
		access=rights()['access']

		if access=='controller':
			return render_template("inventory/create_super.html",data=data,access=access)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))
#===============================================================================# edit admin #========================================  
@inventory.route("/edit_super_admin/<int:id>",methods=['POST','GET'])
@inventory_token
def edit_super_admin(id):
	if request.method=="POST":
		print("=============",id)
		url=site_url+'edit_super_admin'
		data={'id':id,
				'name':request.form['name'],
				'username':request.form['username'],
				'password':request.form['password'],
				'location':request.form['location'],
				'status':request.form['status']
				}
		print("===================",data)
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.put(url,json=data,headers=headers)
		result=data_api.json()
		print("======================result",result)
		if result['message']=="Successfully Updated":
			flash("Created Successfull")
		else:
			error_message=result['message']
			flash(error_message)

	url=site_url+'view_super_admin'
	headers={"x-access-token":session['inventory_token']}
	data_api=requests.get(url,headers=headers)
	result=data_api.json()
	
	if result['message']=="successfull":
		data=result['data']
	else:
		error_message=result['message']
		flash(error_message)
		data=None


	if rights()!=None:
		access=rights()['access']
		access_id=rights()['admin_id']
		
		if access=='controller':
			return render_template("inventory/edit_super_admin.html",id=id,data=data,access=access,access_id=access_id)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))
#===============================================================================# admin_group #========================================  
@inventory.route("/add_admin_group",methods=['POST','GET'])
@inventory_token
def add_admin_group():
	if request.method=="POST":

		url=site_url+'create_admin_group'
		data={'name':request.form['name'],
				'username':request.form['username'],
				'password':request.form['password'],
				'status':request.form['status'],
				'address':request.form['address'],
				'dc_capacity':request.form['dc_capacity']
				}
		
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.post(url,json=data,headers=headers)
		result=data_api.json()
		print(result)
		if result['message']=="Successfully Created":
			account_id=result['account_id']
			fileName=request.files['fileName']
			image_check=image_securty(fileName)
			print(image_check)
			if image_check==True:
				type_='admin_group'
				image_save= image_(fileName,account_id,server_path,type_)
				message=image_save['message']
				print(image_save)
				if image_save['message'] == "save successfully":
					flash("Created Successfull")
					flash("file saved..")
				else:
					flash("account added successfully..")
					flash(message)
			else:
				flash(image_check)
		else:
			error_message=result['message']
			flash(error_message)

	url=site_url+'view_admin_group'
	headers={"x-access-token":session['inventory_token']}
	data_api=requests.get(url,headers=headers)
	result=data_api.json()
	print(result)
	if result['message']=="successfull":
		data=result['data']

	else:
		error_message=result['message']
		flash(error_message)
		data=""
	if rights()!=None:
		access=rights()['access']

		if access=='super_admin':
			return render_template("inventory/create_admin_group.html",data=data,access=access)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))
	

@inventory.route("/edit_admin_group/<int:id>",methods=['POST','GET'])
@inventory_token
def edit_admin_group(id):
	if request.method=="POST":	
		url=site_url+'create_admin_group'
		data={	'id':id,
				'name':request.form['name'],
				'username':request.form['username'],
				'password':request.form['password'],
				'status':request.form['status'],
				'address':request.form['address'],
				'dc_capacity':request.form['dc_capacity']
				}
		
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.put(url,json=data,headers=headers)
		result=data_api.json()
		print(result)
		if result['message']=="Successfully Updated":
			account_id=id
			fileName=request.files['fileName']
			image_check=image_securty(fileName)
			print("image_check",image_check)
			if image_check==True:
				type_='admin_group'
				image_save= image_(fileName,account_id,server_path,type_)
				message=image_save['message']

				if image_save['message'] == "save successfully":
					flash("Created Successfull")
					flash("file saved..")
				else:
					flash("account added successfully..")
					flash(message)
			else:
				flash(image_check)
		else:
			error_message=result['message']
			flash(error_message)

	url=site_url+'view_admin_group'
	headers={"x-access-token":session['inventory_token']}
	data_api=requests.get(url,headers=headers)
	result=data_api.json()
	
	if result['message']=="successfull":
		data=result['data']

	else:
		error_message=result['message']
		flash(error_message)
		data=""
	if rights()!=None:
		access=rights()['access']

		if access=='super_admin':
			return render_template("inventory/edit_admin_group.html",data=data,access=access,id=id)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))

@inventory.route("/delete_grp_admin/<int:id>",methods=['POST','GET'])
@inventory_token
def delete_grp_admin(id):
	if rights()!=None:
		access=rights()['access']
		if request.method=="POST":

			url=site_url+'create_admin_group'
			data={  'id':id	}
			
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.delete(url,json=data,headers=headers)
			result=data_api.json()

			if result['message']=="successfull":
				flash("Delete Successfull")
			else:
				error_message=result['message']
				flash(error_message)
			return redirect(url_for("inventory.add_admin_group"))
		else:
			return redirect(url_for("inventory.add_admin_group"))
	else:
		return redirect(url_for("inventory.error_page"))
#===============================================================================# energy_meter #========================================  
@inventory.route("/add_energy_meter",methods=['POST','GET'])
@inventory_token
def add_energy_meter():
	if rights()!=None:
		access=rights()['access']
		if request.method=="POST":

			url=site_url+'create_energy_meter'
			data={'EM_id':request.form['meter_id'],
					'capacity':request.form['capacity'],
					'admin':request.form['admin'],
					'status':request.form['status'],
					'groupadmin':request.form['groupadmin'],
					'equipment_id':request.form['equipment_id'],
					'slave_id':request.form['slave_id']
					}
			
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.post(url,json=data,headers=headers)
			result=data_api.json()

			if result['message']=="Successfully Created":
				flash("Created Successfull")
			else:
				error_message=result['message']
				flash(error_message)
		
		if( access=='super_admin'):
			url=site_url+'view_energy_meter'
		else:
			url=site_url+'admin_view_energy_meter'
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		print('result',result)
		if result['message']=="successfull":
			data=result['data']
		else:
			error_message=result['message']
			flash(error_message)
			data=""
		print(data)
		if( access=='super_admin'):
			url=site_url+'view_admin'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="successfull":
				admin_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				admin_data=""

			url=site_url+'view_inverter'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="successfull":
				inverter_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				inverter_data=""

			url=site_url+'view_admin_group'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="successfull":
				admingroup_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				admingroup_data=''
			url=site_url+'create_admin'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="Successfull":
				admin_name_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				admin_name_data=""
		else:
			admingroup_data=""
			admin_data=""
			inverter_data=""
			admin_name_data=""

		
		if(access=='admin')|(access=='super_admin'):
			return render_template("inventory/create_energy_meter.html",admin_name_data=admin_name_data,admingroup_data=admingroup_data,data=data,admin_data=admin_data,inverter_data=inverter_data,access=access)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))
	
@inventory.route("/edit_energy_meter/<int:id>",methods=['POST','GET'])
@inventory_token
def edit_energy_meter(id):
	if rights()!=None:
		access=rights()['access']
		if request.method=="POST":

			url=site_url+'create_energy_meter'
			data={ 'id':id,
					'EM_id':request.form['meter_id'],
					'capacity':request.form['capacity'],
					'admin':request.form['admin'],
					'status':request.form['status'],
					'groupadmin':request.form['groupadmin'],
					'equipment_id':request.form['equipment_id'],
					'slave_id':request.form['slave_id']
					}
			
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.put(url,json=data,headers=headers)
			result=data_api.json()
			if result['message']=="Successfully Created":
				flash("Created Successfull")
			else:
				error_message=result['message']
				flash(error_message)
		
		if( access=='super_admin'):
			url=site_url+'view_energy_meter'
		else:
			url=site_url+'admin_view_energy_meter'
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		
		if result['message']=="successfull":
			data=result['data']
		else:
			error_message=result['message']
			flash(error_message)
			data=""
		# print(data)
		if( access=='super_admin'):
			url=site_url+'view_admin'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="successfull":
				admin_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				admin_data=""

			url=site_url+'view_inverter'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="successfull":
				inverter_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				inverter_data=""

			url=site_url+'view_admin_group'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="successfull":
				admingroup_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				admingroup_data=''
			url=site_url+'create_admin'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="Successfull":
				admin_name_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				admin_name_data=""
		else:
			admingroup_data=""
			admin_data=""
			inverter_data=""
			admin_name_data=""

		
		if(access=='admin')|(access=='super_admin'):
			return render_template("inventory/edit_energy_meter.html",id=id,admin_name_data=admin_name_data,admingroup_data=admingroup_data,data=data,admin_data=admin_data,inverter_data=inverter_data,access=access)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))

@inventory.route("/delete_energy_meter/<int:id>",methods=['POST','GET'])
@inventory_token
def delete_energy_meter(id):
	if rights()!=None:
		access=rights()['access']
		if request.method=="POST":

			url=site_url+'create_energy_meter'
			data={  'id':id	}
			
			headers={"x-access-token":session['inventory_token']}
			
			data_api=requests.delete(url,json=data,headers=headers)
			result=data_api.json()
			if result['message']=="Successfull":
				flash("Delete Successfull")
			else:
				error_message=result['message']
				flash(error_message)
			return redirect(url_for("inventory.add_energy_meter"))
		else:
			return redirect(url_for("inventory.add_energy_meter"))
	else:
		return redirect(url_for("inventory.error_page"))
#===============================================================================# inventor #========================================  
@inventory.route("/add_inventor",methods=['POST','GET'])
@inventory_token
def add_inventor():
	if rights()!=None:
		access=rights()['access']
		if request.method=="POST":

			url=site_url+'create_inverter'
			data={'name':request.form['name'],
					'capacity':request.form['capacity'],
					'install_date':request.form['date'],
					'admin':request.form['admin_name'],
					'status':request.form['status'],
					'groupadmin':request.form['groupadmin'],
					'equipment_id':request.form['equipment_id'],
					'slave_id':request.form['slave_id'],
					'energy_meter':request.form['energy_meter']
					}
			
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.post(url,json=data,headers=headers)
			result=data_api.json()

			if result['message']=="Successfully Created":
				flash("Created Successfull")
			else:
				error_message=result['message']
				flash(error_message)
		if( access=='super_admin'):
			url=site_url+'view_inverter'
		else:
			url=site_url+'admin_view_inverter'
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		
		if result['message']=="successfull":
			data=result['data']
		else:
			error_message=result['message']
			flash(error_message)
			data=""

		if( access=='super_admin'):
			url=site_url+'view_energy_meter'
		else:
			url=site_url+'admin_view_energy_meter'
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		
		if result['message']=="successfull":
			eng_data=result['data']
		else:
			error_message=result['message']
			flash(error_message)
			eng_data=""

		if( access=='super_admin'):
			url=site_url+'view_admin'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="successfull":
				admin_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				admin_data=None

			url=site_url+'view_admin_group'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="successfull":
				admingroup_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				admingroup_data=''
			url=site_url+'create_admin'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="Successfull":
				admin_name_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				admin_name_data=""
		else:
			admin_data=""
			admingroup_data=""
			admin_name_data=""
			eng_data=""
		# print(eng_data)
		if( access=='admin' )|( access=='super_admin'):
			return render_template("inventory/create_inventor.html",eng_data=eng_data,admin_name_data=admin_name_data,data=data,admin_data=admin_data,access=access,admingroup_data=admingroup_data)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))

@inventory.route("/delete_inventor/<int:id>",methods=['POST','GET'])
@inventory_token
def delete_inventor(id):
	if rights()!=None:
		access=rights()['access']
		if request.method=="POST":

			url=site_url+'create_inverter'
			data={  'id':id	}
			
			headers={"x-access-token":session['inventory_token']}
			
			data_api=requests.delete(url,json=data,headers=headers)
			result=data_api.json()
			if result['message']=="Successfull":
				flash("Delete Successfull")
			else:
				error_message=result['message']
				flash(error_message)
			return redirect(url_for("inventory.add_inventor"))
		else:
			return redirect(url_for("inventory.add_inventor"))
	else:
		return redirect(url_for("inventory.error_page"))
#===============================================================================# edit inventor #========================================  
@inventory.route("/edit_inventor/<int:id>",methods=['POST','GET'])
@inventory_token
def edit_inventor(id):
	if rights()!=None:
		access=rights()['access']
		if request.method=="POST":

			url=site_url+'create_inverter'
			data={	'id':id,
					'name':request.form['name'],
					'capacity':request.form['capacity'],
					'install_date':request.form['date'],
					'admin':request.form['admin_name'],
					'status':request.form['status'],
					'groupadmin':request.form['groupadmin'],
					'equipment_id':request.form['equipment_id'],
					'slave_id':request.form['slave_id'],
					'energy_meter':request.form['energy_meter']
					}
			
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.put(url,json=data,headers=headers)
			result=data_api.json()

			if result['message']=="Successfully Created":
				flash("Created Successfull")
			else:
				error_message=result['message']
				flash(error_message)
		if( access=='super_admin'):
			url=site_url+'view_inverter'
		else:
			url=site_url+'admin_view_inverter'
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		
		if result['message']=="successfull":
			data=result['data']
		else:
			error_message=result['message']
			flash(error_message)
			data=""

		if( access=='super_admin'):
			url=site_url+'view_energy_meter'
		else:
			url=site_url+'admin_view_energy_meter'
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		
		if result['message']=="successfull":
			eng_data=result['data']
		else:
			error_message=result['message']
			flash(error_message)
			eng_data=""

		if( access=='super_admin'):
			url=site_url+'view_admin'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="successfull":
				admin_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				admin_data=None

			url=site_url+'view_admin_group'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="successfull":
				admingroup_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				admingroup_data=''
			url=site_url+'create_admin'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="Successfull":
				admin_name_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				admin_name_data=""
		else:
			admin_data=""
			admingroup_data=""
			admin_name_data=""
			eng_data=""
		# print(eng_data)
		if( access=='admin' )|( access=='super_admin'):
			return render_template("inventory/edit_inventor.html",id=id,eng_data=eng_data,admin_name_data=admin_name_data,data=data,admin_data=admin_data,access=access,admingroup_data=admingroup_data)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))
#===============================================================================# catagory #========================================  
@inventory.route("/add_catagory",methods=['POST','GET'])
@inventory_token
def add_catagory():
	if request.method=="POST":

		url=site_url+'create_catagory'
		data={'name':request.form['name'],
				'type':request.form['type']
				}
		
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.post(url,json=data,headers=headers)
		result=data_api.json()

		if result['message']=="Successfully Created":
			flash("Created Successfull")
		else:
			error_message=result['message']
			flash(error_message)
	
	url=site_url+'view_catagory'
	headers={"x-access-token":session['inventory_token']}
	data_api=requests.get(url,headers=headers)
	result=data_api.json()
	
	if result['message']=="successfull":
		data=result['data']
	else:
		error_message=result['message']
		flash(error_message)
		data=""
	if rights()!=None:
		access=rights()['access']

		if access=='super_admin':
			return render_template("inventory/create_catagory.html",data=data,access=access)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))	

#===============================================================================# catagory #========================================  
@inventory.route("/edit_catagory/<int:id>",methods=['POST','GET'])
@inventory_token
def edit_catagory(id):
	if request.method=="POST":

		url=site_url+'create_catagory'
		data={'id':id,
				'name':request.form['name'],
				'type':request.form['type']
				}
		
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.put(url,json=data,headers=headers)
		result=data_api.json()

		if result['message']=="Successfully Created":
			flash("updated Successfull")
		else:
			error_message=result['message']
			flash(error_message)
	
	url=site_url+'view_catagory'
	headers={"x-access-token":session['inventory_token']}
	data_api=requests.get(url,headers=headers)
	result=data_api.json()
	
	if result['message']=="successfull":
		data=result['data']
	else:
		error_message=result['message']
		flash(error_message)
		data=""
	if rights()!=None:
		access=rights()['access']

		if access=='super_admin':
			return render_template("inventory/edit_catagory.html",id=id,data=data,access=access)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))

@inventory.route("/delete_catagory/<int:id>",methods=['POST','GET'])
@inventory_token
def delete_catagory(id):
	if rights()!=None:
		access=rights()['access']
		if request.method=="POST":

			url=site_url+'create_catagory'
			data={  'id':id	}
			
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.delete(url,json=data,headers=headers)
			result=data_api.json()

			if result['message']=="Successfully Created":
				flash("Delete Successfull")
			else:
				error_message=result['message']
				flash(error_message)
			return redirect(url_for("inventory.add_catagory"))
		else:
			return redirect(url_for("inventory.add_catagory"))
	else:
		return redirect(url_for("inventory.error_page"))
#===============================================================================# roll #========================================  
@inventory.route("/add_roll",methods=['POST','GET'])
@inventory_token
def add_roll():
	if request.method=="POST":

		url=site_url+'create_roll'
		data={'name':request.form['name'],
				'accounts_approver':request.form['Notification'],
				'status':request.form['status']
				}
		
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.post(url,json=data,headers=headers)
		result=data_api.json()

		if result['message']=="Successfully Created":
			flash("Created Successfull")
		else:
			error_message=result['message']
			flash(error_message)
	
	url=site_url+'view_roll'
	headers={"x-access-token":session['inventory_token']}
	data_api=requests.get(url,headers=headers)
	result=data_api.json()
	
	if result['message']=="successfull":
		data=result['data']
	else:
		error_message=result['message']
		flash(error_message)
		data=""
	if rights()!=None:
		access=rights()['access']

		if access=='super_admin':
			return render_template("inventory/create_roll.html",data=data,access=access)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))
	
#===============================================================================# smb #========================================  
@inventory.route("/add_smb",methods=['POST','GET'])
@inventory_token
def add_smb():
	if rights()!=None:
		access=rights()['access']
		if request.method=="POST":

			url=site_url+'create_smb'
			data={'smb_id':request.form['smb_id'],
					'capacity':request.form['capacity'],
					'admin':request.form['admin'],
					'inverter':request.form['inverter'],
					'status':request.form['status'],
					'groupadmin':request.form['groupadmin'],
					'equipment_id':request.form['equipment_id'],
					'slave_id':request.form['slave_id']
					}
			
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.post(url,json=data,headers=headers)
			result=data_api.json()

			if result['message']=="Successfully Created":
				flash("Created Successfull")
			else:
				error_message=result['message']
				flash(error_message)
		if( access=='super_admin'):
			url=site_url+'view_smb'
		else:
			url=site_url+'admin_view_smb'
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		
		if result['message']=="successfull":
			data=result['data']
		else:
			error_message=result['message']
			flash(error_message)
			data=""

		if( access=='super_admin'):
			url=site_url+'view_inverter'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="successfull":
				inverter_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				inverter_data=""

			url=site_url+'view_admin'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="successfull":
				admin_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				admin_data=""

			url=site_url+'view_admin_group'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="successfull":
				admingroup_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				admingroup_data=''
			url=site_url+'create_admin'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="Successfull":
				admin_name_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				admin_name_data=""
		else:
			inverter_data=""
			admin_data=""
			admingroup_data=""
			admin_name_data=""
		
		if( access=='admin' )|( access=='super_admin'):
			return render_template("inventory/create_smb.html",admin_name_data=admin_name_data,data=data,admin_data=admin_data,inverter_data=inverter_data,access=access,admingroup_data=admingroup_data)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))
	
#===============================================================================# edit smb #========================================  
@inventory.route("/edit_smb/<int:id>",methods=['POST','GET'])
@inventory_token
def edit_smb(id):
	if rights()!=None:
		access=rights()['access']
		if request.method=="POST":

			url=site_url+'create_smb'
			data={  'id':id,
					'smb_id':request.form['smb_id'],
					'capacity':request.form['capacity'],
					'admin':request.form['admin'],
					'inverter':request.form['inverter'],
					'status':request.form['status'],
					'groupadmin':request.form['groupadmin'],
					'equipment_id':request.form['equipment_id'],
					'slave_id':request.form['slave_id']
					}
			
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.put(url,json=data,headers=headers)
			result=data_api.json()

			if result['message']=="Successfully Created":
				flash("Update Successfull")
			else:
				error_message=result['message']
				flash(error_message)
		if( access=='super_admin'):
			url=site_url+'view_smb'
		else:
			url=site_url+'admin_view_smb'
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		
		if result['message']=="successfull":
			data=result['data']
		else:
			error_message=result['message']
			flash(error_message)
			data=""

		if( access=='super_admin'):
			url=site_url+'view_inverter'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="successfull":
				inverter_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				inverter_data=""

			url=site_url+'view_admin'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="successfull":
				admin_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				admin_data=""

			url=site_url+'view_admin_group'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="successfull":
				admingroup_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				admingroup_data=''
			url=site_url+'create_admin'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="Successfull":
				admin_name_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				admin_name_data=""
		else:
			inverter_data=""
			admin_data=""
			admingroup_data=""
			admin_name_data=""
		
		if( access=='admin' )|( access=='super_admin'):
			return render_template("inventory/edit_smb.html",id=id,admin_name_data=admin_name_data,data=data,admin_data=admin_data,inverter_data=inverter_data,access=access,admingroup_data=admingroup_data)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))

@inventory.route("/delete_smb/<int:id>",methods=['POST','GET'])
@inventory_token
def delete_smb(id):
	if rights()!=None:
		access=rights()['access']
		if request.method=="POST":

			url=site_url+'create_smb'
			data={  'id':id	}
			
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.delete(url,json=data,headers=headers)
			result=data_api.json()

			if result['message']=="Successfully Created":
				flash("Delete Successfull")
			else:
				error_message=result['message']
				flash(error_message)
			return redirect(url_for("inventory.add_smb"))
		else:
			return redirect(url_for("inventory.add_smb"))
	else:
		return redirect(url_for("inventory.error_page"))

#===============================================================================# smb #========================================  
@inventory.route("/add_weather",methods=['POST','GET'])
@inventory_token
def add_weather():
	if rights()!=None:
		access=rights()['access']

		if request.method=="POST":

			url=site_url+'create_w_w'
			data={'w_w':request.form['weather'],
					'capacity':request.form['capacity'],
					'admin':request.form['admin'],
					'status':request.form['status'],
					'groupadmin':request.form['groupadmin'],
					'equipment_id':request.form['equipment_id'],
					'slave_id':request.form['slave_id']
					}
			
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.post(url,json=data,headers=headers)
			result=data_api.json()

			if result['message']=="Successfully Created":
				flash("Created Successfull")
			else:
				error_message=result['message']
				flash(error_message)
		if( access=='super_admin'):
			url=site_url+'view_w_w'
		else:
			url=site_url+'admin_view_w_w'
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		
		if result['message']=="successfull":
			data=result['data']
		else:
			error_message=result['message']
			flash(error_message)
			data=""

		if( access=='super_admin'):
			url=site_url+'view_admin'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="successfull":
				admin_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				admin_data=''

			url=site_url+'view_admin_group'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="successfull":
				admingroup_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				admingroup_data=''

			url=site_url+'create_admin'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="Successfull":
				admin_name_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				admin_name_data=""
		else:
			admin_data=""
			admingroup_data=""
			admin_name_data=""
		

		print("data",data)
		if( access=='super_admin') | (access=="admin"):
			return render_template("inventory/create_weather.html",admin_name_data=admin_name_data,data=data,admin_data=admin_data,access=access,admingroup_data=admingroup_data)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))

@inventory.route("/edit_weather/<int:id>",methods=['POST','GET'])
@inventory_token
def edit_weather(id):
	if rights()!=None:
		access=rights()['access']

		if request.method=="POST":

			url=site_url+'create_w_w'
			data={  'id':id,
					'w_w':request.form['weather'],
					'capacity':request.form['capacity'],
					'admin':request.form['admin'],
					'status':request.form['status'],
					'groupadmin':request.form['groupadmin'],
					'equipment_id':request.form['equipment_id'],
					'slave_id':request.form['slave_id']
					}
			
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.put(url,json=data,headers=headers)
			result=data_api.json()

			if result['message']=="Successfully Created":
				flash("Created Successfull")
			else:
				error_message=result['message']
				flash(error_message)
		if( access=='super_admin'):
			url=site_url+'view_w_w'
		else:
			url=site_url+'admin_view_w_w'
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		
		if result['message']=="successfull":
			data=result['data']
		else:
			error_message=result['message']
			flash(error_message)
			data=""

		if( access=='super_admin'):
			url=site_url+'view_admin'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="successfull":
				admin_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				admin_data=''

			url=site_url+'view_admin_group'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="successfull":
				admingroup_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				admingroup_data=''

			url=site_url+'create_admin'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="Successfull":
				admin_name_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				admin_name_data=""
		else:
			admin_data=""
			admingroup_data=""
			admin_name_data=""
		

		print("data",data)
		if( access=='super_admin') | (access=="admin"):
			return render_template("inventory/edit_weather.html",id=id,admin_name_data=admin_name_data,data=data,admin_data=admin_data,access=access,admingroup_data=admingroup_data)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))

@inventory.route("/delete_weather/<int:id>",methods=['POST','GET'])
@inventory_token
def delete_weather(id):
	if rights()!=None:
		access=rights()['access']
		if request.method=="POST":

			url=site_url+'create_w_w'
			data={  'id':id	}
			
			headers={"x-access-token":session['inventory_token']}
			
			data_api=requests.delete(url,json=data,headers=headers)
			result=data_api.json()
			if result['message']=="Successfull":
				flash("Delete Successfull")
			else:
				error_message=result['message']
				flash(error_message)
			return redirect(url_for("inventory.add_weather"))
		else:
			return redirect(url_for("inventory.add_weather"))
	else:
		return redirect(url_for("inventory.error_page"))
#===============================================================================# add_gateway #========================================  
@inventory.route("/add_gateway",methods=['POST','GET'])
@inventory_token
def gateway():
	if rights()!=None:
		access=rights()['access']
		if request.method=="POST":

			url=site_url+'create_gateway'
			data={'meter_id':request.form['meter_id'],
					'capacity':request.form['capacity'],
					'admin':request.form['admin'],
					'status':request.form['status'],
					'api_key':request.form['api_key'],
					'groupadmin':request.form['groupadmin']
					}
			
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.post(url,json=data,headers=headers)
			result=data_api.json()

			if result['message']=="Successfully Created":
				flash("Created Successfull")
			else:
				error_message=result['message']
				flash(error_message)
		# print(session)
		if( access=='super_admin'):
			url=site_url+'view_gateway'
		else:
			url=site_url+'admin_view_gateway'
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		print(result)
		if result['message']=="successfull":
			data=result['data']
		else:
			error_message=result['message']
			flash(error_message)
			data=""

		if( access=='super_admin'):
			url=site_url+'create_admin'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="Successfull":
				admin_name_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				admin_name_data=""

			url=site_url+'view_admin'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="successfull":
				admin_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				admin_data=""

			url=site_url+'view_admin_group'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="successfull":
				admingroup_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				admingroup_data=''

			generate_api_key = ''.join([random.choice( string.ascii_uppercase +
		                                            string.ascii_lowercase +
		                                            string.digits)  
		                                            for n in range(8)])
		else:
			admin_data=""
			admingroup_data=""
			generate_api_key=""
			admin_name_data=""
		if( access=='admin' )|( access=='super_admin'):

			return render_template("inventory/create_gateway.html",generate_api_key=generate_api_key,admin_name_data=admin_name_data,data=data,admin_data=admin_data,access=access,admingroup_data=admingroup_data)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))

@inventory.route("/edit_gateway/<int:id>",methods=['POST','GET'])
@inventory_token
def edit_gateway(id):
	if rights()!=None:
		access=rights()['access']
		if request.method=="POST":

			url=site_url+'create_gateway'
			data={	'id':id,
					'meter_id':request.form['meter_id'],
					'capacity':request.form['capacity'],
					'admin':request.form['admin'],
					'status':request.form['status'],
					'api_key':request.form['api_key'],
					'groupadmin':request.form['groupadmin']
					}
			
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.put(url,json=data,headers=headers)
			result=data_api.json()

			if result['message']=="Successfully Created":
				flash("Created Successfull")
			else:
				error_message=result['message']
				flash(error_message)
		# print(session)
		if( access=='super_admin'):
			url=site_url+'view_gateway'
		else:
			url=site_url+'admin_view_gateway'
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		
		if result['message']=="successfull":
			data=result['data']
		else:
			error_message=result['message']
			flash(error_message)
			data=""
		if( access=='super_admin'):
			url=site_url+'create_admin'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="Successfull":
				admin_name_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				admin_name_data=""

			url=site_url+'view_admin'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="successfull":
				admin_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				admin_data=""

			url=site_url+'view_admin_group'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			
			if result['message']=="successfull":
				admingroup_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				admingroup_data=''

			generate_api_key = ''.join([random.choice( string.ascii_uppercase +
		                                            string.ascii_lowercase +
		                                            string.digits)  
		                                            for n in range(8)])
		else:
			admin_data=""
			admingroup_data=""
			generate_api_key=""
			admin_name_data=""
		if( access=='admin' )|( access=='super_admin'):

			return render_template("inventory/edit_gateway.html",id=id,generate_api_key=generate_api_key,admin_name_data=admin_name_data,data=data,admin_data=admin_data,access=access,admingroup_data=admingroup_data)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))

@inventory.route("/delete_gateway/<int:id>",methods=['POST','GET'])
@inventory_token
def delete_gateway(id):
	if rights()!=None:
		access=rights()['access']
		if request.method=="POST":

			url=site_url+'create_gateway'
			data={  'id':id	}
			
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.delete(url,json=data,headers=headers)
			result=data_api.json()

			if result['message']=="Successfully Created":
				flash("Delete Successfull")
			else:
				error_message=result['message']
				flash(error_message)
			return redirect(url_for("inventory.gateway"))
		else:
			return redirect(url_for("inventory.gateway"))
	else:
		return redirect(url_for("inventory.error_page"))

@inventory.route("/404",methods=['POST','GET'])
@inventory_token
def error_page():
	return render_template("inventory/404.html")

#===============================================================================# child admin #========================================  

@inventory.route("/plant/<string:type_>",methods=['POST','GET'])
@inventory_token
def plant(type_):
	if rights()!=None:
		access=rights()['access']
		url=site_url+'admin_view_w_w'
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		# print(result)
		if result['message']=="successfull":
			data=result['data']
			w_w_data=result['data']
			college_details=result['college_details']
		else:
			error_message=result['message']
			flash(error_message)
			data=""
			college_details=""

		url=site_url+'w_w_solar_panel_data'
		data={'w_w_data':data}
		data_api=requests.get(url,json=data,headers=headers)
		result=data_api.json()

		if result['message']=="Successfull":
			sl_data=result['data']
			poa_data=result['poa_data']
		else:
			error_message=result['message']
			flash(error_message)
			sl_data=''

		# ------------------ ajbs ----------
		url=site_url+'admin_view_smb'
		
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		
		if result['message']=="successfull":
			smb_data=result['data']
		else:
			error_message=result['message']
			flash(error_message)
			smb_data=""

		url=site_url+'abj_solar_panel_data'
		data={'smb_data':smb_data}
		data_api=requests.get(url,json=data,headers=headers)
		result=data_api.json()

		if result['message']=="Successfull":
			ajbs_sl_data=result['data']
		else:
			error_message=result['message']
			flash(error_message)
			ajbs_sl_data=''

		# --------------------- inv ----------------
		url=site_url+'admin_view_inverter'
		
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		# print(result)
		if result['message']=="successfull":
			inverter_data=result['data']
		else:
			error_message=result['message']
			flash(error_message)
			inverter_data=""

		url=site_url+'inverter_solar_panel_data'
		data={'inv_data':inverter_data}
		data_api=requests.get(url,json=data,headers=headers)
		result=data_api.json()

		if result['message']=="Successfull":
			inv_sl_data=result['data']
			tdy_gen=result['tdy_gen']
		else:
			error_message=result['message']
			flash(error_message)
			inv_sl_data=''
			tdy_gen=''


		# --------------------- current poa graph ---------------
		url=site_url+'admin_view_inverter'
		
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		# print(result)
		if result['message']=="successfull":
			inverter_data=result['data']
		else:
			error_message=result['message']
			flash(error_message)
			inverter_data=""
		

		url=site_url+'admin_view_w_w'
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		# print(result)
		if result['message']=="successfull":
			data=result['data']
			w_w_data=result['data']
			college_details=result['college_details']
		else:
			error_message=result['message']
			flash(error_message)
			data=""
			college_details=""
		
		if type_=="ALL":
			from_date=request.form['from_date']
			to_date=request.form['to_date']
		else:
			from_date=""	
			to_date=""

		url=site_url+'current_solar_panel_data'
		data={'inv_data':inverter_data,
				'w_w_data':data,
				'type_':type_,
				'from_date':from_date,
				'to_date':to_date}
		data_api=requests.get(url,json=data,headers=headers)
		result=data_api.json()

		if result['message']=="Successfull":
			poa_graph_data=result['poa_graph_data']
			current_graph_data=result['current_graph_data']
			last_data=result['last_data']
			irradiation=result['irradiation']
		else:
			error_message=result['message']
			flash(error_message)
			poa_graph_data=''
			current_graph_data=''
			last_data=""
			irradiation=""

		weather_api="ae1f4a946da049955ecb72c2c8c6103e"
		url="https://api.openweathermap.org/data/2.5/onecall?lat=9.819409036090583&lon=78.28742075292091&exclude=hourly,daily&appid="+weather_api
		data_api=requests.post(url)
		
		result=data_api.json()
		description=result['current']['weather'][0]['description']
		temperture=result['current']['temp']
		wind_speed=result['current']['wind_speed']
		humidity=result['current']['humidity']

		print('college_details',college_details)
		from datetime import datetime
		_timedate =datetime.now(timezone('Asia/Kolkata'))
		_timedate=_timedate.replace(tzinfo=None)
		_timedate=_timedate
		today_date=_timedate
		print("poa_graph_data",poa_graph_data)
		print("current poa graph",current_graph_data)
		print("=======================",last_data)
		print("-------------------- weather details--------------",temperture,wind_speed,humidity,description)
		relink="/solar_panel/plant/ALL"
		if( access=='admin' )|( access=='super_admin'):

			return render_template("inventory/plant.html",irradiation=irradiation,wind_speed=wind_speed,temperture=temperture,humidity=humidity,description=description,relink=relink,last_data=last_data,current_graph_data=current_graph_data,poa_graph_data=poa_graph_data,poa_data=poa_data,today_date=today_date,inverter_data=inverter_data,inv_sl_data=inv_sl_data,access=access,sl_data=sl_data,w_w_data=w_w_data,college_details=college_details,smb_data=smb_data,ajbs_sl_data=ajbs_sl_data)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))
	
@inventory.route("/inverter",methods=['POST','GET'])
@inventory_token
def inventor():
	if rights()!=None:
		access=rights()['access']

		url=site_url+'admin_view_inverter'
		
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		# print(result)
		if result['message']=="successfull":
			inverter_data=result['data']
		else:
			error_message=result['message']
			flash(error_message)
			inverter_data=""

		url=site_url+'inverter_solar_panel_data'
		data={'inv_data':inverter_data}
		data_api=requests.get(url,json=data,headers=headers)
		result=data_api.json()

		if result['message']=="Successfull":
			sl_data=result['data']
			tdy_gen=result['tdy_gen']
		else:
			error_message=result['message']
			flash(error_message)
			sl_data=''
			tdy_gen=''
		# print(inverter_data)
		print("**************************************************&&")

		url=site_url+'admin_view_smb'
		
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		
		if result['message']=="successfull":
			smb_data=result['data']
		else:
			error_message=result['message']
			flash(error_message)
			smb_data=""

		url=site_url+'abj_solar_panel_data'
		data={'smb_data':smb_data}
		data_api=requests.get(url,json=data,headers=headers)
		result=data_api.json()

		if result['message']=="Successfull":
			smb_sl_data=result['data']
		else:
			error_message=result['message']
			flash(error_message)
			smb_sl_data=''

		print("================== smb_sl_data ===============",smb_sl_data)
		# print("================== sl_data ===============",sl_data)
		# print("================== smb_data ===============",smb_data)
		if( access=='admin' )|( access=='super_admin'):

			return render_template("inventory/inventor.html",smb_data=smb_data,smb_sl_data=smb_sl_data,access=access,inverter_data=inverter_data,sl_data=sl_data,tdy_gen=tdy_gen)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))

@inventory.route("/ajbs/<string:filter_>",methods=['POST','GET'])
@inventory_token
def ajbs(filter_):
	if rights()!=None:
		access=rights()['access']

		url=site_url+'admin_view_smb'
		
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		
		if result['message']=="successfull":
			smb_data=result['data']
		else:
			error_message=result['message']
			flash(error_message)
			smb_data=""

		url=site_url+'abj_solar_panel_data'
		data={'smb_data':smb_data}
		data_api=requests.get(url,json=data,headers=headers)
		result=data_api.json()

		if result['message']=="Successfull":
			sl_data=result['data']
		else:
			error_message=result['message']
			flash(error_message)
			sl_data=''

		if filter_=='online':
			filter_='online'
		elif filter_=='offline':
			filter_='offline'
		else:
			filter_='ALL'
		if( access=='admin' )|( access=='super_admin'):

			return render_template("inventory/AJBs.html",access=access,smb_data=smb_data,sl_data=sl_data,filter_=filter_)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))

@inventory.route("/energymeter",methods=['POST','GET'])
@inventory_token
def energymeter():
	if rights()!=None:
		access=rights()['access']

		url=site_url+'admin_view_energy_meter'
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		
		if result['message']=="successfull":
			eng_data=result['data']
		else:
			error_message=result['message']
			flash(error_message)
			eng_data=""

		url=site_url+'engerymeter_solar_panel_data'
		data={'eng_data':eng_data}
		data_api=requests.get(url,json=data,headers=headers)
		result=data_api.json()

		if result['message']=="Successfull":
			eng_sl_data=result['data']
			vcb_check_data=result['vcb_check_data']
			
		else:
			error_message=result['message']
			flash(error_message)
			eng_sl_data=''
			vcb_check_data=""
		print("--------------------------------------- vcb check data ------------------",vcb_check_data)
		# ---------------------inv----------------
		url=site_url+'admin_view_inverter'
		
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		# print(result)
		if result['message']=="successfull":
			inverter_data=result['data']
		else:
			error_message=result['message']
			flash(error_message)
			inverter_data=""

		url=site_url+'inverter_solar_panel_data'
		data={'inv_data':inverter_data}
		data_api=requests.get(url,json=data,headers=headers)
		result=data_api.json()

		if result['message']=="Successfull":
			inv_sl_data=result['data']
			tdy_gen=result['tdy_gen']
		else:
			error_message=result['message']
			flash(error_message)
			inv_sl_data=''
			tdy_gen=''

		# print(eng_sl_data)
		if( access=='admin' )|( access=='super_admin'):

			return render_template("inventory/Energy_meter.html",vcb_check_data=vcb_check_data,inverter_data=inverter_data,inv_sl_data=inv_sl_data,access=access,eng_sl_data=eng_sl_data,eng_data=eng_data)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))

@inventory.route("/datavisual",methods=['POST','GET'])
@inventory_token
def datavisual():
	if rights()!=None:
		access=rights()['access']
		if request.method=="POST":
			ajb=request.form.getlist('ajb')
			ajb_para=request.form.getlist('ajb_para')
			inv=request.form.getlist('inv')
			inv_para=request.form.getlist('inv_para')
			eng=request.form.getlist('eng')
			eng_para=request.form.getlist('eng_para')
			w_w_d=request.form.getlist('w_w_d')
			w_w_d_para=request.form.getlist('w_w_d_para')
			data={  'ajb':ajb,
					'ajb_para':ajb_para,
					'inv':inv,
					'inv_para':inv_para,
					'eng':eng,
					'eng_para':eng_para,
					'w_w_d':w_w_d,
					'w_w_d_para':w_w_d_para,
					'w_w':['None'],
					"w_w_para":['None'],
					'from_date':request.form['from_date'],
					'to_date':request.form['to_date']
					}

			url=site_url+'data_visual_graph'
			
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.post(url,json=data,headers=headers)
			result=data_api.json()

			if result['message']=="Successfull":
				ajb_data=result['ajb_data']
				inv_data=result['inv_data']
				eng_data=result['eng_data']
				w_w_d_data=result['final_w_w_d_data']
			else:
				error_message=result['message']
				flash(error_message)
				ajb_data=""
				inv_data=""
				eng_data=""
				w_w_d_data=""

			# print(ajb_data)
			# import json
			# with open('result.json', 'w') as fp:
			#     json.dump(ajb_data, fp)
			return render_template("inventory/data_visualisation_graph.html",w_w_d_para=w_w_d_para,w_w_d=w_w_d,w_w_d_data=w_w_d_data,access=access,ajb_para=ajb_para,inv_para=inv_para,eng_para=eng_para,ajb_data=ajb_data,eng_data=eng_data,inv_data=inv_data)
		url=site_url+'admin_view_smb'
		
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		
		if result['message']=="successfull":
			smb_data=result['data']
		else:
			error_message=result['message']
			flash(error_message)
			smb_data=""

		url=site_url+'admin_view_inverter'
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		
		if result['message']=="successfull":
			inv_data=result['data']
		else:
			error_message=result['message']
			flash(error_message)
			inv_data=""

		url=site_url+'admin_view_energy_meter'
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		
		if result['message']=="successfull":
			eng_data=result['data']
		else:
			error_message=result['message']
			flash(error_message)
			eng_data=""


		url=site_url+'admin_view_w_w'
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		# print(result)
		if result['message']=="successfull":
			data=result['data']
			w_w_data=result['data']
			college_details=result['college_details']
		else:
			error_message=result['message']
			flash(error_message)
			w_w_data=""
			college_details=""

		if( access=='admin' )|( access=='super_admin'):

			return render_template("inventory/data_visualisation.html",college_details=college_details,w_w_data=w_w_data,access=access,smb_data=smb_data,inv_data=inv_data,eng_data=eng_data)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))

@inventory.route("/datavisual_report",methods=['POST','GET'])
@inventory_token
def datavisual_report():
	if rights()!=None:
		access=rights()['access']
		if request.method=="POST":
			ajb=request.form.getlist('ajb')
			ajb_para=request.form.getlist('ajb_para')
			inv=request.form.getlist('inv')
			inv_para=request.form.getlist('inv_para')
			eng=request.form.getlist('eng')
			eng_para=request.form.getlist('eng_para')
			w_w=request.form.getlist('w_w')
			w_w_para=request.form.getlist('w_w_para')
			w_w_d=request.form.getlist('w_w_d')
			w_w_d_para=request.form.getlist('w_w_d_para')
			to_date=request.form['to_date']

			data={  'ajb':ajb,
					'ajb_para':ajb_para,
					'inv':inv,
					'inv_para':inv_para,
					'eng':eng,
					'eng_para':eng_para,
					'w_w':w_w,
					'w_w_para':w_w_para,
					'w_w_d':w_w_d,
					'w_w_d_para':w_w_d_para,
					'from_date':request.form['from_date'],
					'to_date':request.form['to_date']
					}

			url=site_url+'data_visual'
			
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.post(url,json=data,headers=headers)
			result=data_api.json()

			if result['message']=="Successfull":
				

				report_ajb_data=result["report_ajb_data"]

				report_inv_data_1=result["report_inv_data_1"]
				report_inv_data_2=result["report_inv_data_2"]

				report_eng_data_1=result["report_eng_data_1"]
				report_eng_data_2=result["report_eng_data_2"]
				report_eng_data_3=result["report_eng_data_3"]

				report_w_w_d_data=result['report_w_w_d_data']

				remodified_inv_data=result['remodified_inv_data']

				remodified_eng_data=result['remodified_eng_data']

				w_w_sl_data=result['w_w_sl_data']
				poa_data=result['poa_data']
			else:
				error_message=result['message']
				flash(error_message)
				
				report_ajb_data=""
				report_inv_data_1=""
				report_inv_data_2=""
				report_eng_data_1=""
				report_eng_data_2=""
				report_eng_data_3=""
				remodified_inv_data=""
				remodified_eng_data=""
				poa_data=""
				report_w_w_d_data=""
				w_w_sl_data=""

			# ---------------------inv----------------
			url=site_url+'admin_view_inverter'
			
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			# print(result)
			if result['message']=="successfull":
				inverter_data=result['data']
			else:
				error_message=result['message']
				flash(error_message)
				inverter_data=""

			url=site_url+'inverter_solar_panel_data_'
			data={'inv_data':inverter_data,'to_date':to_date}
			data_api=requests.get(url,json=data,headers=headers)
			result=data_api.json()

			if result['message']=="Successfull":
				inv_sl_data=result['data']
				tdy_gen=result['tdy_gen']
			else:
				error_message=result['message']
				flash(error_message)
				inv_sl_data=''
				tdy_gen=''

			ajb_graph_name={"DC Current":"DC Current","DC ISOLATOR STATUS":"DC ISOLATOR STATUS","POWER":"POWER","SPD STATUS":"SPD STATUS","FIELD1":"STRING 1","FIELD2":"STRING 2","FIELD3":"STRING 3","FIELD4":"STRING 4","FIELD5":"STRING 5","FIELD6":"STRING 6","FIELD7":"STRING 7","FIELD8":"STRING 8","FIELD9":"STRING 9","FIELD10":"STRING 10","FIELD11":"STRING 11","FIELD12":"STRING 12","FIELD13":"STRING 13","FIELD14":"STRING 14","FIELD15":"STRING 15","FIELD16":"STRING 16","FIELD17":"STRING 17","FIELD18":"STRING 18","FIELD19":"STRING 19","FIELD20":"STRING 20","FIELD21":"STRING 21","FIELD22":"STRING 22","FIELD23":"STRING 23","FIELD24":"STRING 24","FIELD33":"TEMP1","FIELD34":"VOLTAGE"}
			inv_graph_name={"FIELD104":"AC CURRENT","FIELD5":"AC FREQUENCY","FIELD2":"AC POWER","FIELD4":"AC VOLTAGE","FIELD101":"AC VOLTAGE B-PHASE","FIELD102":"AC  VOLTAGE R-PHASE","FIELD103":"AC VOLTAGE Y-PHASE","FIELD1010":"CUBICLE TEMPERATURE","FIELD107":"DC CURRENT","FIELD105":"DC VOLTAGE","FIELD115":"HEAT SINK TEMPERATURE","FIELD6":"POWER FACTOR","FIELD3":"REACTIVE POWER","FIELD131":"TODAY GENERATION","FIELD132":"TOTAL GENERATION"}
			eng_graph_name={"FIELD18":"C_B_PHASE","FIELD14":"C_R_PHASE","FIELD16":"C_Y_PHASE","FIELD20":"CURRENT TOTAL","FIELD132":"FREQUENCY","FIELD100":"PF_AVG","FIELD38":"PF_B_PHASE","FIELD34":"PF_R_PHASE","FIELD36":"PF_Y_PHASE","FIELD114":"VAR_B_PHASE","FIELD110":"VAR_R_PHASE","FIELD112":"VAR_Y_PHASE","FIELD124":"VA TOTAL","FIELD122":"VA_B_PHASE","FIELD118":"VA_R_PHASE","FIELD120":"VA_Y_PHASE","FIELD116":"VAR TOTAL","FIELD12":"VB_PHASE","FIELD4":"VBR_PHASE","FIELD8":"VR_PHASE","FIELD0":"VRY_PHASE","FIELD6":"VLN AVG","FIELD10":"VY_PHASE","FIELD2":"VYB_PHASE","FIELD108":"WATT_TOTAL","FIELD106":"WATTS_B_PHASE","FIELD102":"WATTS_R_PHASE","FIELD104":"WATTS_Y_PHASE","FIELD200":"WH_DELIVERED","FIELD202":"VAH_DELIVERED"}
			w_w_d_graph_name={"FIELD4":"Wind Speed","FIELD1":"Ambinet temperature","FIELD15":"POA","FIELD14":"GHA","FIELD21":"Bom Temperature"}
			# contents = report_ajb_data
			# _key = list(contents.keys())[0]
			# print('contents',contents[_key])

			url=site_url+'admin_view_w_w'
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			result=data_api.json()
			# print(result)
			if result['message']=="successfull":
				data=result['data']
				w_w_data=result['data']
				college_details=result['college_details']
			else:
				error_message=result['message']
				flash(error_message)
				w_w_data=""
				college_details=""
			# print(ajb_para)
			return render_template("inventory/data_visualisation_report.html",report_w_w_d_data=report_w_w_d_data,w_w_d_graph_name=w_w_d_graph_name,w_w_d_para=w_w_d_para,w_w_d=w_w_d,inverter_data=inverter_data,poa_data=poa_data,college_details=college_details,tdy_gen=tdy_gen,inv_sl_data=inv_sl_data,w_w_data=w_w_data,w_w_para=w_w_para,eng_graph_name=eng_graph_name,remodified_eng_data=remodified_eng_data,inv_graph_name=inv_graph_name,remodified_inv_data=remodified_inv_data,ajb_graph_name=ajb_graph_name,report_ajb_data=report_ajb_data,report_eng_data_3=report_eng_data_3,report_eng_data_2=report_eng_data_2,report_eng_data_1=report_eng_data_1,report_inv_data_2=report_inv_data_2,report_inv_data_1=report_inv_data_1,access=access,ajb_para=ajb_para,inv_para=inv_para,eng_para=eng_para)
		url=site_url+'admin_view_smb'
		
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		
		if result['message']=="successfull":
			smb_data=result['data']
		else:
			error_message=result['message']
			flash(error_message)
			smb_data=""

		url=site_url+'admin_view_inverter'
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		
		if result['message']=="successfull":
			inv_data=result['data']
		else:
			error_message=result['message']
			flash(error_message)
			inv_data=""

		url=site_url+'admin_view_energy_meter'
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		
		if result['message']=="successfull":
			eng_data=result['data']
		else:
			error_message=result['message']
			flash(error_message)
			eng_data=""

		url=site_url+'admin_view_w_w'
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.get(url,headers=headers)
		result=data_api.json()
		
		if result['message']=="successfull":
			w_w_data=result['data']
		else:
			error_message=result['message']
			flash(error_message)
			w_w_data=""

		if( access=='admin' )|( access=='super_admin'):

			return render_template("inventory/data_visualisation_download.html",w_w_data=w_w_data,access=access,smb_data=smb_data,inv_data=inv_data,eng_data=eng_data)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))

@inventory.route("/metric_com",methods=['POST','GET'])
@inventory_token
def metric_com():
	if rights()!=None:
		access=rights()['access']

		if( access=='admin' )|( access=='super_admin'):

			return render_template("inventory/metrics_com.html",access=access)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))

@inventory.route("/sl_data",methods=['POST','GET'])
@inventory_token
def sl_data():
	if rights()!=None:
		access=rights()['access']

		if( access=='controller'):
			url=site_url+'solar_panel_data'
			
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.get(url,headers=headers)
			
			result=data_api.json()
			print(result)
			if result['message']=="Successfull":
				data=result['data']
				print(data)
			else:
				error_message=result['message']
				flash(error_message)
				data=""
			return render_template("inventory/sl.html",access=access,data=data)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))
#===============================================================================# account #========================================  
@inventory.route("/add_account",methods=['POST','GET'])
@inventory_token
def add_account():

	if request.method=="POST":

		url=site_url+'create_accounts'
		fileName=request.files['fileName']
		data={'name':request.form['title'],
				'description':request.form['details'],
				'account_cat':request.form['account_cat'],
				'admin':request.form['admin_name'],
				'status':request.form['status'],
				'remarks':request.form['remarks'],
				'fileName':'null',
				'amount':request.form['amount']
				}
		
		headers={"x-access-token":session['inventory_token']}
		image_check=image_securty(fileName)
		if image_check==True:
			data_api=requests.post(url,json=data,headers=headers)
			result=data_api.json()
			
			if result['message']=="Successfully Created":
				account_id=result['account_id']
				type_='account'
				image_save= image_(fileName,account_id,server_path,type_)
				message=image_save['message']

				if image_save['message'] == "save successfully":
					flash("file saved..")
				else:
					flash("account added successfully..")
					flash(message)
			else:
				error_message=result['message']
				flash(error_message)
		else:
			flash(image_check)
	
	url=site_url+'view_accounts'
	headers={"x-access-token":session['inventory_token']}
	data_api=requests.get(url,headers=headers)
	result=data_api.json()
	
	if result['message']=="successfull":
		data=result['data']
	else:
		error_message=result['message']
		flash(error_message)
		data=""
	
	url=site_url+'view_catagory'
	headers={"x-access-token":session['inventory_token']}
	data_api=requests.get(url,headers=headers)
	result=data_api.json()
	
	if result['message']=="successfull":
		cat_data=result['data']
	else:
		error_message=result['message']
		flash(error_message)
		cat_data=""

	url=site_url+'view_admin'
	headers={"x-access-token":session['inventory_token']}
	data_api=requests.get(url,headers=headers)
	result=data_api.json()
	
	if result['message']=="successfull":
		admin_data=result['data']
	else:
		error_message=result['message']
		flash(error_message)
		admin_data=None

	if rights()!=None:
		access=rights()['access']

		if access=='super_admin':
			return render_template("inventory/create_account.html",data=data,access=access,cat_data=cat_data,admin_data=admin_data)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))

@inventory.route("/edit_account/<int:id>",methods=['POST','GET'])
@inventory_token
def edit_account(id):

	if request.method=="POST":

		url=site_url+'create_accounts'
		fileName=request.files['fileName']
		data={	'id':id,
				'name':request.form['title'],
				'description':request.form['details'],
				'account_cat':request.form['account_cat'],
				'admin':request.form['admin_name'],
				'status':request.form['status'],
				'remarks':request.form['remarks'],
				'fileName':'null',
				'amount':request.form['amount']
				}
		
		headers={"x-access-token":session['inventory_token']}
		
		data_api=requests.put(url,json=data,headers=headers)
		result=data_api.json()
		print(result)
		if result['message']=="Successfully Created":
			account_id=result['account_id']
			image_check=image_securty(fileName)
			if image_check==True:
				type_='account'
				image_save= image_(fileName,account_id,server_path,type_)
				message=image_save['message']

				if image_save['message'] == "save successfully":
					flash("file saved..")
				else:
					flash("account added successfully..")
					flash(message)
			else:
				flash(image_check+'\tRemaining data update')

		else:
			error_message=result['message']
			flash(error_message)
		
	url=site_url+'view_accounts'
	headers={"x-access-token":session['inventory_token']}
	data_api=requests.get(url,headers=headers)
	result=data_api.json()
	
	if result['message']=="successfull":
		data=result['data']
	else:
		error_message=result['message']
		flash(error_message)
		data=""
	
	url=site_url+'view_catagory'
	headers={"x-access-token":session['inventory_token']}
	data_api=requests.get(url,headers=headers)
	result=data_api.json()
	
	if result['message']=="successfull":
		cat_data=result['data']
	else:
		error_message=result['message']
		flash(error_message)
		cat_data=""

	url=site_url+'view_admin'
	headers={"x-access-token":session['inventory_token']}
	data_api=requests.get(url,headers=headers)
	result=data_api.json()
	
	if result['message']=="successfull":
		admin_data=result['data']
	else:
		error_message=result['message']
		flash(error_message)
		admin_data=None

	if rights()!=None:
		access=rights()['access']

		if access=='super_admin':
			return render_template("inventory/edit_account.html",id=id,data=data,access=access,cat_data=cat_data,admin_data=admin_data)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))

@inventory.route("/delete_account/<int:id>",methods=['POST','GET'])
@inventory_token
def delete_account(id):
	if rights()!=None:
		access=rights()['access']
		if request.method=="POST":

			url=site_url+'create_accounts'
			data={'id':id	}
			
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.delete(url,json=data,headers=headers)
			result=data_api.json()

			if result['message']=="successfull":
				flash("Delete Successfull")
			else:
				error_message=result['message']
				flash(error_message)
			return redirect(url_for("inventory.add_account"))
		else:
			return redirect(url_for("inventory.add_account"))
	else:
		return redirect(url_for("inventory.error_page"))
#===============================================================================# users #========================================  
@inventory.route("/add_users",methods=['POST','GET'])
@inventory_token
def add_users():

	if request.method=="POST":

		url=site_url+'create_users'
		data={'name':request.form['name'],
				'username':request.form['username'],
				'password':request.form['password'],
				'admin_list':request.form['teams'],
				'view':request.form['view'],
				'edit':request.form['edit'],
				'approve':request.form['approve']
				}
		
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.post(url,json=data,headers=headers)
		result=data_api.json()
		print(result)
		if result['message']=="Successfully Created":
			flash("Created Successfull")
		else:
			error_message=result['message']
			flash(error_message)
	
	url=site_url+'view_users'
	headers={"x-access-token":session['inventory_token']}
	data_api=requests.get(url,headers=headers)
	result=data_api.json()
	
	if result['message']=="successfull":
		data=result['data']
	else:
		error_message=result['message']
		flash(error_message)
		data=""
	
	url=site_url+'view_admin'
	headers={"x-access-token":session['inventory_token']}
	data_api=requests.get(url,headers=headers)
	result=data_api.json()
	
	if result['message']=="successfull":
		admin_data=result['data']
	else:
		error_message=result['message']
		flash(error_message)
		admin_data=None

	if rights()!=None:
		access=rights()['access']

		if access=='super_admin':
			return render_template("inventory/create_users.html",data=data,access=access,admin_data=admin_data)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))

@inventory.route("/edit_users/<int:id>",methods=['POST','GET'])
@inventory_token
def edit_users(id):

	if request.method=="POST":

		url=site_url+'create_users'
		data={'id':id,
				'name':request.form['name'],
				'username':request.form['username'],
				'password':request.form['password'],
				'admin_list':request.form['teams'],
				'view':request.form['view'],
				'edit':request.form['edit'],
				'approve':request.form['approve']
				}
		
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.put(url,json=data,headers=headers)
		result=data_api.json()
		print(result)
		if result['message']=="Successfully Created":
			flash("Created Successfull")
		else:
			error_message=result['message']
			flash(error_message)
	
	url=site_url+'view_users'
	headers={"x-access-token":session['inventory_token']}
	data_api=requests.get(url,headers=headers)
	result=data_api.json()
	
	if result['message']=="successfull":
		data=result['data']
	else:
		error_message=result['message']
		flash(error_message)
		data=""
	
	url=site_url+'view_admin'
	headers={"x-access-token":session['inventory_token']}
	data_api=requests.get(url,headers=headers)
	result=data_api.json()
	
	if result['message']=="successfull":
		admin_data=result['data']
	else:
		error_message=result['message']
		flash(error_message)
		admin_data=None

	url=site_url+'user_admin'
	headers={"x-access-token":session['inventory_token']}
	data_api=requests.get(url,headers=headers)
	result=data_api.json()
	
	if result['message']=="successfull":
		user_data=result['data']
	else:
		error_message=result['message']
		flash(error_message)
		user_data=None
	# ================================================ multi choice option ======================		
	selected_admin=[]
	for i in user_data:
		selected_admin.append(i['user_id'])

	print("+++++++++++===========selected_admin",selected_admin)
	admin_select_data=[]
	for i in admin_data:
		if i['id'] in selected_admin:
			admin_select_data.append({'id':i['id'],'name':i['name'],'type':'selected'})
		else:
			admin_select_data.append({'id':i['id'],'name':i['name'],'type':'unselected'})
	admin_data=admin_select_data
	print("+++++++++++===========admin_select_data",admin_select_data)

	if rights()!=None:
		access=rights()['access']

		if access=='super_admin':
			return render_template("inventory/edit_user.html",user_data=user_data,data=data,access=access,admin_data=admin_data,id=id)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))

@inventory.route("/delete_users/<int:id>",methods=['POST','GET'])
@inventory_token
def delete_users(id):
	if rights()!=None:
		access=rights()['access']
		if request.method=="POST":

			url=site_url+'create_users'
			data={  'id':id	}
			
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.delete(url,json=data,headers=headers)
			result=data_api.json()

			if result['message']=="successfull":
				flash("Delete Successfull")
			else:
				error_message=result['message']
				flash(error_message)
			return redirect(url_for("inventory.add_users"))
		else:
			return redirect(url_for("inventory.add_users"))
	else:
		return redirect(url_for("inventory.error_page"))
#===============================================================================# account #========================================  
@inventory.route("/add_support",methods=['POST','GET'])
@inventory_token
def add_support():

	if request.method=="POST":

		url=site_url+'create_support'
		data={'name':request.form['admin'],
				'title':request.form['title'],
				'description':request.form['description'],
				'due_date':request.form['due_date'],
				'admin':request.form['admin'],
				'user_list':request.form.getlist('teams'),
				'remarks':request.form['remarks'],
				'status':request.form['status'],
				'type':request.form['type']
				}
		
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.post(url,json=data,headers=headers)
		result=data_api.json()
		
		if result['message']=="Successfully Created":
			flash("Created Successfull")
		else:
			error_message=result['message']
			flash(error_message)

	url=site_url+'view_support'
	headers={"x-access-token":session['inventory_token']}
	data_api=requests.get(url,headers=headers)
	result=data_api.json()
	
	if result['message']=="successfull":
		data=result['data']
	else:
		error_message=result['message']
		flash(error_message)
		data=""
	
	url=site_url+'view_users'
	headers={"x-access-token":session['inventory_token']}
	data_api=requests.get(url,headers=headers)
	result=data_api.json()
	
	if result['message']=="successfull":
		user_data=result['data']
	else:
		error_message=result['message']
		flash(error_message)
		user_data=""
	
	url=site_url+'view_admin'
	headers={"x-access-token":session['inventory_token']}
	data_api=requests.get(url,headers=headers)
	result=data_api.json()
	
	if result['message']=="successfull":
		admin_data=result['data']
	else:
		error_message=result['message']
		flash(error_message)
		admin_data=None

	if rights()!=None:
		access=rights()['access']

		if access=='super_admin':
			return render_template("inventory/create_support.html",data=data,access=access,admin_data=admin_data,user_data=user_data)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))

#===============================================================================# account #========================================  
@inventory.route("/edit_support/<int:id>",methods=['POST','GET'])
@inventory_token
def edit_support(id):

	if request.method=="POST":

		url=site_url+'create_support'
		data={	'id':id,
				'name':request.form['admin'],
				'title':request.form['title'],
				'description':request.form['description'],
				'due_date':request.form['due_date'],
				'admin':request.form['admin'],
				'user_list':request.form.getlist('teams'),
				'remarks':request.form['remarks'],
				'status':request.form['status'],
				'type':request.form['type']
				}
		
		headers={"x-access-token":session['inventory_token']}
		data_api=requests.put(url,json=data,headers=headers)
		result=data_api.json()
		
		if result['message']=="Successfully Created":
			flash("Update Successfull")
		else:
			error_message=result['message']
			flash(error_message)

	url=site_url+'view_support'
	headers={"x-access-token":session['inventory_token']}
	data_api=requests.get(url,headers=headers)
	result=data_api.json()
	
	if result['message']=="successfull":
		data=result['data']
	else:
		error_message=result['message']
		flash(error_message)
		data=""

	url=site_url+'view_alloted_to'
	headers={"x-access-token":session['inventory_token']}
	data_api=requests.get(url,headers=headers)
	result=data_api.json()
	
	if result['message']=="successfull":
		allot_data=result['data']
	else:
		error_message=result['message']
		flash(error_message)
		allot_data=""
	
	url=site_url+'view_users'
	headers={"x-access-token":session['inventory_token']}
	data_api=requests.get(url,headers=headers)
	result=data_api.json()
	
	if result['message']=="successfull":
		user_data=result['data']
	else:
		error_message=result['message']
		flash(error_message)
		user_data=""
	
	url=site_url+'view_admin'
	headers={"x-access-token":session['inventory_token']}
	data_api=requests.get(url,headers=headers)
	result=data_api.json()
	
	if result['message']=="successfull":
		admin_data=result['data']
	else:
		error_message=result['message']
		flash(error_message)
		admin_data=None

	if rights()!=None:
		access=rights()['access']

		if access=='super_admin':
			return render_template("inventory/edit_support.html",allot_data=allot_data,id=id,data=data,access=access,admin_data=admin_data,user_data=user_data)
		else:
			return redirect(url_for("inventory.error_page"))
	else:
		return redirect(url_for("inventory.error_page"))

@inventory.route("/delete_support/<int:id>",methods=['POST','GET'])
@inventory_token
def delete_support(id):
	if rights()!=None:
		access=rights()['access']
		if request.method=="POST":

			url=site_url+'create_support'
			data={  'id':id	}
			
			headers={"x-access-token":session['inventory_token']}
			data_api=requests.delete(url,json=data,headers=headers)
			result=data_api.json()

			if result['message']=="successfull":
				flash("Delete Successfull")
			else:
				error_message=result['message']
				flash(error_message)
			return redirect(url_for("inventory.add_support"))
		else:
			return redirect(url_for("inventory.add_support"))
	else:
		return redirect(url_for("inventory.error_page"))

@inventory.route('/return-files/<string:folder_name>/<string:file_name>')
@inventory_token
def return_files_tut(folder_name,file_name):
	try:
		link=os.path.join(server_path,folder_name,file_name)
		print("------------------------> ", link)
		return send_file(link,attachment_filename=file_name)
		# return send_file("/var/www/solar_panel/static/images/solar.png")
	except Exception as e:
		print(e)
	# except Exception as e:
	# 	link=os.path.join(server_path,folder_name,'default.jpg')
	# 	return send_file(link, attachment_filename='default.jpg')
	finally:
		pass
		
# ===============================================================================# solar_panel_data #========================================  
@inventory.route("/solar_panel_data",methods=['POST','GET'])
def solar_panel_data():
	
	api_key=request.args.get("api_key")
	S_NO=request.args.get("S_NO")
	IP=request.args.get("IP")
	DID=request.args.get("DID")
	EID=request.args.get("EID")
	ID=request.args.get("ID")
	FC=request.args.get("FC")
	ADDRESS=request.args.get("ADDRESS")
	QUANTITY=request.args.get("QUANTITY")
	TIME_STAMP=float(request.args.get("TIME_STAMP")) / 1000
	from datetime import datetime
	print("=========>", TIME_STAMP,'ist',ist)
	formatted_time = datetime.fromtimestamp(int(TIME_STAMP),ist)
	formatted_time=formatted_time.replace(tzinfo=None)
	formatted_time = str(formatted_time)
	print("---------------> Formatted Time", formatted_time)
	TIME_STAMP = formatted_time
	print("DATA Entry Check")
	FIELD0=request.args.get("FIELD0")
	print("+++++++++++++++ Field 0 ++++++++++",FIELD0)
	FIELD1=request.args.get("FIELD1")
	FIELD2=request.args.get("FIELD2")
	FIELD3=request.args.get("FIELD3")
	FIELD4=request.args.get("FIELD4")
	FIELD5=request.args.get("FIELD5")
	FIELD6=request.args.get("FIELD6")
	FIELD7=request.args.get("FIELD7")
	FIELD8=request.args.get("FIELD8")
	FIELD9=request.args.get("FIELD9")
	FIELD10=request.args.get("FIELD10")
	FIELD11=request.args.get("FIELD11")
	FIELD12=request.args.get("FIELD12")
	FIELD13=request.args.get("FIELD13")
	FIELD14=request.args.get("FIELD14")
	FIELD15=request.args.get("FIELD15")
	FIELD16=request.args.get("FIELD16")
	FIELD17=request.args.get("FIELD17")
	FIELD18=request.args.get("FIELD18")
	FIELD19=request.args.get("FIELD19")
	FIELD20=request.args.get("FIELD20")
	FIELD21=request.args.get("FIELD21")
	FIELD22=request.args.get("FIELD22")
	FIELD23=request.args.get("FIELD23")
	FIELD24=request.args.get("FIELD24")
	FIELD25=request.args.get("FIELD25")
	FIELD26=request.args.get("FIELD26")
	FIELD27=request.args.get("FIELD27")
	FIELD28=request.args.get("FIELD28")
	FIELD29=request.args.get("FIELD29")
	FIELD30=request.args.get("FIELD30")
	FIELD31=request.args.get("FIELD31")
	FIELD32=request.args.get("FIELD32")
	FIELD33=request.args.get("FIELD33")
	FIELD34=request.args.get("FIELD34")
	FIELD35=request.args.get("FIELD35")
	FIELD36=request.args.get("FIELD36")
	FIELD37=request.args.get("FIELD37")
	FIELD38=request.args.get("FIELD38")
	FIELD39=request.args.get("FIELD39")
	url=site_url+'solar_panel_data'
	data={
    "api_key":api_key,
		"S_NO":S_NO,
		"IP":IP,
		"DID":DID,
		"EID":EID,
		"ID":ID,
		"FC":FC,
		"ADDRESS":ADDRESS,
		"QUANTITY":QUANTITY,
		"TIME_STAMP":TIME_STAMP,
		"FIELD0":FIELD0,
		"FIELD1":FIELD1,
		"FIELD2":FIELD2,
		"FIELD3":FIELD3,
		"FIELD4":FIELD4,
		"FIELD5":FIELD5,
		"FIELD6":FIELD6,
		"FIELD7":FIELD7,
		"FIELD8":FIELD8,
		"FIELD9":FIELD9,
		"FIELD10":FIELD10,
		"FIELD11":FIELD11,
		"FIELD12":FIELD12,
		"FIELD13":FIELD13,
		"FIELD14":FIELD14,
		"FIELD15":FIELD15,
		"FIELD16":FIELD16,
		"FIELD17":FIELD17,
		"FIELD18":FIELD18,
		"FIELD19":FIELD19,
		"FIELD20":FIELD20,
		"FIELD21":FIELD21,
		"FIELD22":FIELD22,
		"FIELD23":FIELD23,
		"FIELD24":FIELD24,
		"FIELD25":FIELD25,
		"FIELD26":FIELD26,
		"FIELD27":FIELD27,
		"FIELD28":FIELD28,
		"FIELD29":FIELD29,
		"FIELD30":FIELD30,
		"FIELD31":FIELD31,
		"FIELD32":FIELD32,
		"FIELD33":FIELD33,
		"FIELD34":FIELD34,
		"FIELD35":FIELD35,
		"FIELD36":FIELD36,
		"FIELD37":FIELD37,
		"FIELD38":FIELD38,
		"FIELD39":FIELD39
}
	
	print(data)
	data_api=requests.post(url,json=data)
	
	result=data_api.json()
	print(result)
	if result['message']=="Successful":
		
		return jsonify({"message": result["message"], "id": result["id"]})
	else:
		error_message=result['message']
		
		return jsonify({"message":"Failed!"})

#  keys
# admin
# admin_group
# super_admin
# controller
