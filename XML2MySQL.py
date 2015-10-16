__author__ = 'Phoe'

import os
import mysql
import mysql.connector
from mysql.connector import Error
import datetime

import xml.etree.ElementTree as ET


def ImportRoadPoint(roadfilename):
	print " "
	print "Import Road Point"
	print "-----------------"
	
	tree_point = ET.parse(roadfilename)
	root_point = tree_point.getroot()

	print "==Load done====="
	
	print " "
	print "Saving to Database"
	print "------------------"
	
	#opening database connection
	print "--->Open database connection"
	conn = mysql.connector.connect( host	= 'localhost',
					database= 'ITS2014',
					user	= 'root',
					password= '5fe5e619eaff')

	if not conn.is_connected():
		print "FAIL TO CONNECT TO DATABASE-----EXITING!!!"
		return fail;
	cur = conn.cursor()
	
	insert_point = (" insert into RoadPoint  "
					" (RpointID, OSMID, longitude, lattitude) "
					" values (%s, %s, %s, %s)")

	

	curInternal = -1
	curID = -1
	cur_lat = cur_long = 0

	#loop for all xml item
	print "--->"
	for child in root_point:
		for sub in child:
			if sub.tag == "InternalID":
				curInternal = sub.text
			#	print curInternal
			if sub.tag == "ID":
				curID = sub.text
			if sub.tag == "lat":
				cur_lat = sub.text
			if sub.tag == "long":
				cur_long = sub.text


		data_point = (	curInternal,		#RpointID
 						curID,
						cur_long,
						cur_lat)
		cur.execute(insert_point, data_point)	
	
	conn.commit()
	#close database connection
	print "--->Close database connection"
	cur.close()
	conn.close()
	
	i = datetime.datetime.now()
	print "=====Done function at: " + str(i)

	return

def ImportSegmentData(segmentfilename):
	print " "
	print "Import Segment Data"
	print "-------------------"
	
	segment_point = ET.parse(segmentfilename)
	root_segment = segment_point.getroot()

	print "==Load done====="
	
	print " "
	print "Saving to Database"
	print "------------------"
	
	#opening database connection
	print "--->Open database connection"
	conn = mysql.connector.connect( host	= 'localhost',
					database= 'ITS2014',
					user	= 'root',
					password= '5fe5e619eaff')

	if not conn.is_connected():
		print "FAIL TO CONNECT TO DATABASE-----EXITING!!!"
		return fail;
	cur = conn.cursor()

	insert_segment = (" insert into SegmentData  "
					" (startRoadPointID, endRoadPointID, WayID) "
					" values (%s, %s, %s)")

	curIDa 		= -1
	curIDb 		= -1
	curWayID 	= -1


	#loop for all xml item
	print "--->"
	for child in root_segment:
		for sub in child:
			if sub.tag == "IDa":
				curIDa = sub.text
			
			if sub.tag == "IDb":
				curIDb = sub.text
			
			if sub.tag == "WayID":
				curWayID = sub.text

		data_segment = (curIDa,
				curIDb,
				curWayID)
		cur.execute(insert_segment, data_segment)	
	conn.commit()
	#close database connection
	print "--->Close database connection"
	cur.close()
	conn.close()
	
	i = datetime.datetime.now()
	print "=====Done function at: " + str(i)

	return
	
	
	



def main():
	#ImportRoadPoint('Map_data/NodeData.xml')
	ImportSegmentData('Map_data/SegmentData.xml')
	



	return

if __name__ == '__main__':
	main()
