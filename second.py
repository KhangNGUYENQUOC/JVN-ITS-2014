__author__ = 'Phoe'

import json
import os
import mysql
import mysql.connector
from mysql.connector import Error
import datetime
from math import radians, cos, sin, asin, sqrt

import xml.etree.ElementTree as ET


myConnectedToDatabase = 'fase'

def get_distance(long1,lat1 , long2,lat2):
	long1, lat1, long2, lat2 = map(radians, [long1, lat1, long2, lat2] )

	dlong = long2 - long1
	dlat = lat2 - lat1
	a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlong/2)**2
	c = 2 * asin(sqrt(a) )

	r = 6371
	return c * r

def calculate_velocity_moh(dis,sec):
	if sec ==0:
		return float( 0)

	return float(dis/sec*3600)


#here, we consider if we need ALL raw data or not?
#currently, ALL raw data are loaded. 
#But we should devide them into days, weeks, months?
def LoadAllRawData():
	print "Load ALL Raw Data here!"
	print "----------------------------"
	conn = mysql.connector.connect( host	= 'localhost',
					database= 'ITS2014',
					user	= 'root',
					password= '5fe5e619eaff' )

	if not conn.is_connected():
		print "Can NOT connect to database"
		#myConnectedToDatabse = 'true'
		return "fail";

	load_raw = ("select * from LocationData ")
	cur = conn.cursor()
	cur.execute(load_raw)
	data = cur.fetchall()

#	for row in data:
#		print row[0], row[1]

	cur.close()
	conn.close()	

	#having raw data

	

	

	return data

def LoadRawData():
	print "Load Raw Data here!"
	print "----------------------------"
	return 
	


#The size of the segment data is somehow FIXED.
#only need to update the segment data each month?(if needed)
def LoadSegmentData():
	return

def LoadAllInfoSegment():
	print "Load Segment Data here!"
	print "----------------------------"
	conn = mysql.connector.connect(	host	= 'localhost',
					database= 'ITS2014',
					user	= 'root',
					password= '5fe5e619eaff')
	if not conn.is_connected():
		print "Connection FAIL!"
		return "fail"
	cur = conn.cursor()

	str_select=" select S.segmentID, R1.longitude , R1.lattitude, R2.longitude, R2.lattitude " 
	str_from=" from RoadPoint R1, SegmentData S, RoadPoint R2 " 
	str_where=" where ( R1.RpointID = S.startRoadPointID ) and ( R2.RpointID = S.endRoadPointID )"

	load_segment = str_select + str_from + str_where
	cur.execute(load_segment)
	print "*"
	
	AllInfoData = cur.fetchall()
	print "*"
	cur.close()
	conn.close()
	print " "
	print " "
	return AllInfoData


def Load_GPS_Current_Day():
	i = datetime.datetime.now().date()
	print "Load GPS for today"
	print "------------------"
	print "Today is: " + str(i)

	conn = mysql.connector.connect( host	='localhost',
					database='ITS2014',
					user	='root',
					password='5fe5e619eaff')
	if not conn.is_connected():
		print " DATABASE CONNECTION FAIL "
		return "fail"

	cur = conn.cursor()

#	cur = Create_database_connection()
#	if cur == "fail":
#		print "~~~~~~~~~~~~~~~~~~~~~~ERROR: in Load_GPS_Current_Day!"
#		return "fail"
	
	load_current_day = " select * from LocationData L where L.sampleDate = curdate()" 
	cur.execute(load_current_day)
	data_cur_date = cur.fetchall()

	cur.close()
	conn.close()

	
	print " "
	print " "
	return data_cur_date


def Create_database_connection():
	conn = mysql.connector.connect( host	= 'localhost',
					database= 'ITS2014',
					user	= 'root',
					password= '5fe5e619eaff')
	if not conn.is_connected():
		print "FAIL TO CONNECT TO DATABASE"
		return "fail"

	cur = conn.cursor()

	return cur



def LoadPointData():

	load_point = " select * from RoadPoint "

	return


def Mapping_GPS_to_segment():
	return

def Hash_value(number):
	return int(number*100)

def CreateStandardizedData():
	print "Create Standardized Data here!"
	print "----------------------------"
	return

def main():
	print "main here!"
	
	cur_dis = get_distance( 106.96, 10.6321, 106.97, 10.6321) 
	print str(cur_dis) + " (Kilometer)"
	
#	cur_vel = calculate_velocity_mos(cur_dis*1000, 3)
#	print str(cur_vel) + " (met over sec)"
#	raw_location = LoadAllRawData()

	t = "\t \t"
 	
	#load gps for current day
#	gps_cur_day = Load_GPS_Current_Day()
#	gps_cur_day
#	if gps_cur_day == "fail":
#		print "..........EXITING........."
#		return
#
	#test data:
#	for r in gps_cur_day:
#		print str(r[0])+t+str(r[2])+t+str(r[3])+t+str(r[4])

	

	#load all map info
#	all_info =  LoadAllInfoSegment()
#	all_info
#	if all_info == "fail":
#		print "..........EXITING........."
#		return 

	#mapping step!
	
	#processing all segment data here
#	for r in all_info:
#		print str(r[0])+t+ str(r[1])+t+ str(r[2])+t+ str(r[3])+t+ str(r[4])


#	for r in gps_cur_day:
		#find list of candidate segment
		#simple way, not save data into segment database
		
		# find current gps grid:
#		long_grid = Hash_value(r[2])
#		latt_grid = Hash_value(r[3])
#		list_of_segment = []
#		for i in all_info:
#			cur1_long = Hash_value(i[1])
#			cur1_lat  = Hash_value(i[2])
#			cur2_long = Hash_value(i[3])
#			cur2_lat  = Hash_value(i[4])
			

		

#	CreateStandardizedData()

	

	return


if __name__ == '__main__':
	main()
