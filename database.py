import mysql

myConnectedToDatabase = 'false'
myConnectError = 'false'

def connect():
	try:
		conn = mysql.connector.connect( host= 'localhost'
						database = 'ITS2014',
						user = 'root',
						password = '5fe5e619eaff')

		if conn.is_connected():
			myConnectedToDatabase = 'true'

	except Error as e:
		myConnectError = 'True'

	finally: 
		conn.close()





def closeConnection():
