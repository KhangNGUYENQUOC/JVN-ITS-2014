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
def Load_current_15_min_Raw():
	print "Load 15 min raw"
	print "---------------"
	return Load_Location_previous_sec( 900 )


def Load(query):
	print "Loading database..."
	print "-------------------"
	conn = mysql.connector.connect(	host	='localhost',
					database='ITS2014',
					user	='root',
					password='5fe5e619eaff')
	cur = conn.cursor()
	cur.execute(query)
	data = cur.fetchall()
	cur.close()
	conn.close()

	print "Done"
	return data



def Load_Location_previous_sec( sec ):
	print "Load raw data with given time interval"
	print "--------------------------------------"

	conn = mysql.connector.connect(	host	='localhost',
					database='ITS2014',
					user 	='root',
					password='5fe5e619eaff')
	cur = conn.cursor()
	query =" select * from LocationData L where L.sampleDate = CURDATE()  and SUBTIME(CURTIME(),L.sampleTime)< " + str(sec)
	cur.execute(query)
	data = cur.fetchall()
	print " "
	print " "
	return data

def Load_Grid_With_Segments():
	print "Load Grid with segments"
	print "-----------------------"

	conn = mysql.connector.connect( host	= 'localhost',
					database= 'ITS2014',
					user	= 'root',
					password= '5fe5e619eaff')

	cur = conn.cursor()
	list_of_grid = LoadGridData()
	map_grid = []
	if list_of_grid =="fail":
		return "fail"
	else:
		print str( len( list_of_grid ) )
		#for i in range(len (list_of_grid) ):
		for g in list_of_grid:
			#pass
			#load segments in the grid
			query_segment = " select S.segmentID, R1.longitude, R1.lattitude, R2.longitude, R2.lattitude "
			query_segment += " from GridData G, GridSegment L, SegmentData S, RoadPoint R1, RoadPoint R2 "
			query_segment += " where (L.GridID = " + str(g[0]) + " ) and (L.SegmentID = S.segmentID) "
			query_segment += " and (S.startRoadPointID=R1.RpointID) and (S.endRoadPointID= R2.RpointID ) " 
			print "gridID: " + str(g[0]) 
			cur.execute(query_segment)
			
			list_seg = cur.fetchall()
			print "Number of segment in the grid: " + str( len( list_seg  ) )
			map_grid.append(list_seg)
	return 

def LoadLinkMatrix():
	print "Load Link matrix here!"
	print "----------------------"

	conn = mysql.connector.connect(	host	= 'localhost',
					database= 'ITS2014',
					user	= 'root',
					password= '5fe5e619eaff' )
	cur = conn.cursor()
	data_matrix = [] 
	for i in range(0,1890):
		data_matrix.append( [] )

 
	query = (" select * " 
		" from GridData G, GridSegment L "
		" where L.GridID = G.gridID " )
	
	cur.execute(query)
	print "Execute data!"
	data_list = cur.fetchall()
	
	print "Ready for processing"
	
	for r in data_list:
		gid = r[0]
		data_matrix[gid].append( r[5] )
		
	return data_matrix

def LoadAllLocationData():
	print "Load All Location Data here!"
	print "----------------------------"
	conn = mysql.connector.connect( host	= 'localhost',
					database= 'ITS2014',
					user	= 'root',
					password= '5fe5e619eaff' )
	cur = conn.cursor()
	query = "select * from LocationData "
	cur.execute(query)
	print "*"
	list_gps = cur.fetchall()


	return list_gps

def LoadLinkGridSegment():
	print "Load Link Grid Segment"
	print "----------------------"
	
	conn = mysql.connector.connect( host	= 'localhost',
					database= 'ITS2014',
					user	= 'root',
					password= '5fe5e619eaff' )

	cur = conn.cursor()
	query = "select * from GridSegment G order by G.GridID ASC "
	cur.execute(query)
	data_list_link = cur.fetchall()
		
	
	return data_list_link

def LoadGridData():
	print "Load Grid Data here!"
	print "--------------------"
	
	conn = mysql.connector.connect(	host	= 'localhost',
					database= 'ITS2014',
					user	= 'root',
					password= '5fe5e619eaff')
	if not conn.is_connected():
		print "Connection FAIL!"
		return "fail"
	cur = conn.cursor()
	query = "select * from GridData"
	
	cur.execute(query)
	print "*"
	
	data_Grid = cur.fetchall()
	print "*"
	
	print " "
	print " "
	return data_Grid

def LoadSegmentWithPointData():
	print "Load Segment Data here!"
	print "-----------------------"
	conn = mysql.connector.connect(	host	= 'localhost',
					database= 'ITS2014',
					user	= 'root',
					password= '5fe5e619eaff')
	if not conn.is_connected():
		print "Connection FAIL!"
		return "fail"
	cur = conn.cursor()

	str_select=" select S.segmentID, R1.longitude , R1.lattitude, R2.longitude, R2.lattitude " 
	str_from=" from SegmentData S,RoadPoint R1, RoadPoint R2 " 
	str_where=" where ( R1.RpointID = S.startRoadPointID ) and ( R2.RpointID = S.endRoadPointID )"
	str_order=" order by S.segmentID "

	load_segment = str_select + str_from + str_where + str_order
	cur.execute(load_segment)
	print "*"
	
	AllInfoData = cur.fetchall()
	print "*"
	cur.close()
	conn.close()
	print " "
	print " "
	return AllInfoData

def main():
	print "Nothing in this main"
	return

if __name__ == '__main__':
	main()
