from pymongo import Connection
import datetime
import time

def LoadUniversal(q):
	conn = Connection()
	db = conn['022015']
	assert db.connection == conn

	mdata = list( db.GPSTracking.find(q  ))
	return mdata

def LoadOneBusDataForSegment(start,end,veh):
	conn = Connection()
	db = conn['022015']
	#connecting to Feb 2015 data##################
	assert db.connection == conn
	if not ( isinstance(start,int) 
		and isinstance(end,int) 
		and isinstance(veh,str) ):
		return 
	print "================================================="
	print "Loading Data:"
	temp1 = time.strftime( '%Y-%m-%d %H:%M:%S'
		, time.localtime( start) )
	temp2 = time.strftime( '%Y-%m-%d %H:%M:%S'
		, time.localtime( end) ) 	
	
	print "From: " + temp1 +"\t to: " + temp2
	print "."
	print " "
	mdata = list( db.GPSTracking.find( 
		{"vehicle":veh,"datetime":{"$gte":start,"$lte":end}}
		,
		{
		"_id":1, "vehicle":1, "datetime":1, "x":1, "y":1 #, "z":1
		}
		))
	print "Done Loading"
	print "================================================="
	print " "
	print " "
	return  mdata 

def LoadOneBusData(start,end,veh):
	conn = Connection()
	db = conn['022015']
	#connecting to Feb 2015 data##################
	assert db.connection == conn
	if not ( isinstance(start,int) 
		and isinstance(end,int) 
		and isinstance(veh,str) ):
		return 
	print "================================================="
	print "Loading Data:"
	temp1 = time.strftime( '%Y-%m-%d %H:%M:%S'
		, time.localtime( start) )
	temp2 = time.strftime( '%Y-%m-%d %H:%M:%S'
		, time.localtime( end) ) 	
	print "From: " + temp1 +"\t to: " + temp2
	print "."
	print " "
	mdata = list( db.GPSTracking.find( 
		{"vehicle":veh,"datetime":{"$gte":start,"$lte":end}}
		,
		{
		"_id":1, "vehicle":1, "datetime":1, "x":1, "y":1 #, "z":1
		}
		))
	print "Done Loading"
	print "================================================="
	print " "
	print " "
	return  mdata 

def LoadAllBusData(start,end):
	conn = Connection()
	db = conn['022015']
	#connect to Feb 2015
	assert db.connection  == conn
	if not (isinstance(start,int) and isinstance(end,int)):
		print "trap here!!!"
		return

	mdata = list( db.GPSTracking.find(
		{
		"datetime":{"$gte":start,"$lte":end}
		},
		{
		"_id":0, "vehicle":1, "datetime":1, "x":1, "y":1
		} 
		))
	
	return mdata


def LoadAllBusWithin(long,lat,start,end):
	conn = Connection()
	db = conn['022015']
	assert db.connection == conn

	mdata = list( db.GPSTracking.find(
		{
		"datetime":{"$gte":start,"$lte":end},
		"x":{"$gte":long-0.02,"$lte":long+0.02},
		"y":{"$gte":lat-0.01,"$lte":lat+0.01}
		},
		{"_id":0,"vehicle":1,"datetime":1,"x":1,"y":1}
		))
	return mdata
