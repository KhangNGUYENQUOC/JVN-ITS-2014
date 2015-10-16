import mysql
import mysql.connector
import json
from mysql.connector import Error 
import datetime
from decimal import Decimal

myConnectedToDatabase = 'false'
myConnectError = 'false'

def Save_database(query,data):
	conn = mysql.connector.connect(	host	='localhost',
					database='ITS2014',
					user	='root',
					password='5fe5e619eaff' )
	if not conn.is_connected():
		print "fail to connect to database"
		return
	cur = conn.cursor()
	cur.execute(query,data)
	conn.commit()
	cur.close()
	conn.close()	
	return



def insert_new_JSON_data(JSON_File_name ):
	#print JSON_File_name
	f = open(JSON_File_name)
	dataJSON = json.load(f)
	f.close()
	numberOfJsonItem = len(dataJSON)
	#check for all item in JSON list
	conn = mysql.connector.connect(	host 	= 'localhost',
					database = 'ITS2014',
					user 	= 'root',
					password= '5fe5e619eaff' )

	if not conn.is_connected():
		return  str("Can not connect to database")
	#print "Connected to database"
	cur = conn.cursor()
	add_gps = ("insert into LocationData "
		"(deviceId, longitude, lattitude, sampleDate, sampleTime, googleSpeed, googleAccuracy) "
		"values (%s, %s, %s, %s, %s, %s, %s)" )
	
	#print "Get in for loop , for each dataJSON..."
	for index in dataJSON:

		#print "convert to the right type"
		curDeviceID 	= str ( index['deviceID'] )
		curLong 	= float ( index['longitude'] )
		curLatt 	= float ( index['latitude'] )
		curSampleDate 	= str ( index['sampleDate'] ) + ""
		curVelocity	= float ( index['speed'] )
		curAccuracy	= float ( index['accuracy'] ) 
		device_id = curDeviceID
		longitude = curLong
		lattitude = curLatt
		temp = datetime.datetime.strptime( curSampleDate,
						"%Y-%m-%d %H:%M:%S")
		mdate = temp.date()
		mtime = temp.time()
		if not ( isinstance( mdate, datetime.date )
			and isinstance( mtime, datetime.time) ):
			return str("Error in datetime data type")
		
		data_gps = (device_id, longitude, lattitude, mdate, mtime, curVelocity, curAccuracy)
		#print "ready to execute"
                #print device_id
                #print longitude
                #print lattitude
                #print mdate
                #print mtime
		#print str( type(device_id) +" "+ device_id)
		#print str( type(longitude) +" "+longitude)		
		#print str( type(lattitude) +" "+ lattitude)
		#print str( type(mdate) +" "+ mdate)
		#print str( type(mtime) +" "+ mtime)
		cur.execute(add_gps, data_gps)
                #print "executed"
		#conn.commit()
		#print "commited"
		#print "Execute mysql query"

#		i = datetime.datetime.now()			#verbose
#		print "New data added at: " + str(i)		#verbose
        
	#print "Commit and Closing connection"
	conn.commit()
	cur.close()
	conn.close()
	i = datetime.datetime.now()
        log = 		"Done save JSON to database at: 	" + str(i)
        print log
	print str(	"Number of item: 		") + str(numberOfJsonItem)

        return str("true")
		





def insert_new_gps( device_id, longitude, lattitude, mdate, mtime ):
	#print ("checking condition ...")
	#check data type for parameters
	if not (    isinstance(device_id, str)  
		and isinstance(longitude, float) 
		and isinstance(lattitude, float)
		and isinstance(mdate, datetime.date)
		and isinstance(mtime, datetime.time) ) :
		#print ("false")
		return str("false")
	#print( "true")
	conn = mysql.connector.connect(	host ='localhost', 
					database = 'ITS2014',
					user = 'root', 
					password = '5fe5e619eaff')
	cur = conn.cursor()
	#cur.execute("Insert into GPSdata(deviceID) Values(device_id) ")
	#cur.execute("Insert into GPSdata(gpslongitude) Values(longitude)")
	#cur.execute("Insert into GPSdata(gpslattitude) Values(lattitude)")
	#cur.execute("Insert into GPSdata(timestamps) Values(time_stamp)") 
	#use this for current datetime.
	#i = datetime.datetime.now()
	add_gps = ("insert into LocationData "
		"(deviceId, longitude, lattitude, sampleDate, sampleTime) "
		"values (%s, %s, %s, %s, %s)")
	#data_gps = ( 'abc123', 321, 123, i.date(), i.time() )
	data_gps = (device_id, longitude, lattitude, mdate, mtime)
	cur.execute(add_gps, data_gps)
	#ready to commit and close.
	conn.commit()
	cur.close()
	conn.close()
	i = datetime.datetime.now()
	log = "New data added to database at: " + str(i)
	print log
	return 'true'

def closeConnection():
	if conn:
		conn.close()
	return null
 

