# SWAMI KARUPPASWAMI THUNNAI

import pymysql
from sys import platform

def get_connection():
	if "linux" in platform:
		connection = pymysql.connect(
			host="141.136.36.151", user="thamarai_kani", password="thamarai123_K@ni",
			db="solar_panel_tracking", charset="utf8", cursorclass=pymysql.cursors.DictCursor
			)
	else:
		connection = pymysql.connect(
			host="141.136.36.151", user="thamarai_kani", password="thamarai123_K@ni",
			db="solar_panel_tracking", charset="utf8", cursorclass=pymysql.cursors.DictCursor
			)
	# else:
	# 	connection = pymysql.connect(
	# 		host="127.0.0.1", user="root", password="",
	# 		db="solar_panel", charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor
	# 		)
	return connection






	

