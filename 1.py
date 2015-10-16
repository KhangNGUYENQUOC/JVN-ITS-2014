import mysql.connector
from mysql.connector import Error

def connect():
	try:
		conn = mysql.connector.connect(host = 'localhost',
					database = 'ITS2014',
					user = 'root',
					password = '5fe5e619eaff')
		if conn.is_connected():
			print('connected')
	except Error as e:
		print(e)

	finally:
		conn.close()

if __name__ == '__main__':
	connect()
	


