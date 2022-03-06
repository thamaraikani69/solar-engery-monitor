import requests
from datetime import date,datetime
import datetime
def api_check():
	
	api_key='c8DrAnUs'
	S_NO=1
	IP=1
	DID=1
	EID=20
	ID=111
	FC=1
	ADDRESS=1
	QUANTITY=1
	TIME_STAMP='20201010'
	FIELD0=0
	FIELD1=0
	FIELD2=0
	FIELD3=0
	FIELD4=0
	FIELD5=0
	FIELD6=0
	FIELD7=0
	FIELD8=0
	FIELD9=0
	FIELD10=0
	FIELD11=0
	FIELD12=0
	FIELD13=0
	FIELD14=0
	FIELD15=0
	FIELD16=0
	FIELD17=0
	FIELD18=0
	FIELD19=0
	FIELD20=0
	FIELD21=0
	FIELD22=0
	FIELD23=0
	FIELD24=0
	FIELD25=0
	FIELD26=0
	FIELD27=0
	FIELD28=0
	FIELD29=0
	FIELD30=0
	FIELD31=0
	FIELD32=0
	FIELD33=0
	FIELD34=0
	FIELD35=0
	FIELD36=0
	FIELD37=0
	FIELD38=0
	FIELD39=0
	url='https://solar.alliancetech.co.in/api/'+'solar_panel_data'
	print(url)
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
	
	# print(data)
	data_api=requests.post(url,json=data)
	# print(data_api)
	result=data_api.json()
	print(result)
	if result['message']=="Successfully Created":
		print("Created Successfull")
		return redirect("/dashboard")
	else:
		error_message=result['message']
		print(error_message)
		return "error occured"
def web_check():
	url='http://solar.alliancetech.co.in/solar_panel/solar_panel_data?api_key=c8DrAnUs&S_NO=721&IP=192.168.1.101:502/81&DID=1&EID=20&ID=111&FC=3&ADDRESS=42545&QUANTITY=30&TIME_STAMP=1605846449966&FIELD0=0&FIELD1=0&FIELD2=0&FIELD3=0&FIELD4=0&FIELD5=0&FIELD6=0&FIELD7=0&FIELD8=0&FIELD9=0&FIELD10=0&FIELD11=0&FIELD12=0&FIELD13=0&FIELD14=0&FIELD15=0&FIELD16=0&FIELD17=0&FIELD18=0&FIELD19=0&FIELD20=0&FIELD21=0&FIELD22=0&FIELD23=0&FIELD24=0&FIELD25=0&FIELD26=0&FIELD27=0&FIELD28=0&FIELD29=0&FIELD30=0&FIELD31=0&FIELD32=0&FIELD33=0&FIELD34=0&FIELD35=0&FIELD36=0&FIELD37=0&FIELD38=0&FIELD39=0'
	data_api=requests.get(url)
	result=data_api.json()
	print(result)
	if result['message']=="Successfully Created":
		print('re')
def api_check_data():
	url='http://127.0.0.1:5000/solar_panel/api/abj_solar_panel_data'
	data_api=requests.get(url)
	result=data_api.json()
	print(result)
	if result['message']=="Successfully Created":
		pass
def time_check():
	
	mytime = datetime.datetime.strptime('0130','%H%M').time()
	mydatetime = datetime.datetime.combine(datetime.date.today(), mytime)
	print(mydatetime)

import json
sms_status={"Gateway": 1, "Inverter": 1, "vcb": 1}
def sms_switch(name,status):
   	# sms_status=open("D:\\projects\\Aibeing\\solar_panel_\\solar_panel\\templates\\inventory\\sms_status.py",'r')
   	# sms_status=json.load(sms_status)
   	# print(sms_status)
   	for i in sms_status:
   		if i==name:
   			print('name pass and sms_status: ',sms_status[i])
   			if status==0 and sms_status[i]==1:
   				print("message")
   				sms_status[i]=0
   				# with open("D:\\projects\\Aibeing\\solar_panel_\\solar_panel\\templates\\inventory\\sms_status.py",'w') as f:
   				# 	f.write(json.dumps(sms_status))
   			elif(status==1 and sms_status[i]==0):
   				print("message alert on")
   				sms_status[i]=1
   				# with open("D:\\projects\\Aibeing\\solar_panel_\\solar_panel\\templates\\inventory\\sms_status.py",'w') as f:
   				# 	f.write(json.dumps(sms_status))
   			print(sms_status)

import requests
url="http://sms.ourcampus.in/sendsms?uname=alliance20&pwd=allian234&senderid=SECSMS&to=+919789301757&msg=message&route=T&peid=1701158038234467676&tempid=1707162411054704156"

weather_api="ae1f4a946da049955ecb72c2c8c6103e"
url="https://api.openweathermap.org/data/2.5/onecall?lat=33.44&lon=-94.04&exclude=hourly&appid="+weather_api
data_api=requests.post(url)

result=data_api.json()
description=result['current']['weather'][0]['description']
temperture=result['current']['temp']
wind_speed=result['current']['wind_speed']
humidity=result['current']['humidity']
print(description,temperture,wind_speed,humidity)


if __name__ == '__main__':
	# for i in range(0,2):
	# 	print(i)
	# 	sms_switch('vcb',i)
	# 	sms_switch('Gateway',i)

	web_check()