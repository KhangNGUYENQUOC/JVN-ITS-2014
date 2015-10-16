__author__ = 'Phoe'

import LoadData as LD
import FromRawToStandard as FRTS
import os
import sys
import BusMongoLoader as BML
import second
import datetime
import time
import csv

def SpeedOfOneBus(): #(start,end,veh):
	start = int(1422723602+60*60*0)
	end = int(start + 60*60*24*1)
	#veh = "51B02724"
	#veh = "53N4338"
	veh = "53N4307"
	data = BML.LoadOneBusData(start,end,veh)
	long = data[0]['x']
	lat = data[0]['y']
	time = data[0]['datetime']
	
	for d in data:
		d['x1'] = long
		d['y1'] = lat
		dist = second.get_distance(long,lat,d['x'],d['y'])
		interval = d['datetime'] - time
		speed = second.calculate_velocity_moh(dist,interval)
		d['speed'] = speed
		long = d['x']
		lat = d['y']
		time = d['datetime']

	return list( data )

def ListOfSegmentWithBusData():
	#Load bus data in one day 
	start = int( 1422723602  )
	end_day = int( start + 60*60*24 )
	end_hour = int ( start + 60*60 )
	allday = BML.LoadAllBusData(start,end_hour)

	print " Loaded "+ str(len(allday)) + " bus sample"


	#Load Map data with grid info
	list_seg 	= LD.LoadSegmentWithPointData()
	list_grid 	= LD.LoadGridData()
	list_link	= LD.LoadLinkGridSegment() 
	
	list_bus_segment = FRTS.MapSampleToSegment(allday)
	print "================================================="
	print " Mapped "+ str( len(list_bus_segment) ) 

	#Find SegmentID with given Bus_location
	#add into list of segment ID
	





		

	#Sort SegmentID, remove dublicate
#	sorted = list_bus_segment.sort()
#	final_list = []
#	t = -1
#	for s in sorted:
#		if not  (t==-1) :
#			if not(t == s):
#				final_list.append(s)
#				t = s
#			else:
#				pass
#		else:
#			final_list.append(s)
	#Got list of segmentID here
	

#	return final_list

	return list_bus_segment

def Create_heat_map(data,hour,long,lat):
	f1 	= open("heat_upper.txt","r")
	up 	= f1.read()
	f11	= open("heat_upper1.txt","r")
	mid_str	= f11.read()
	f2 	= open("heat_lower.txt", "r")
	down 	= f2.read()

	f1.close()
	f11.close()
	f2.close()
	m_str = "var taxiData =  "
	
	mid = []
	t_str = "{location: new google.maps.LatLng( " 
	for d in data:
		t1_str = t_str + str( d['y'])+" , " +str( d['x'])  +" ),weight:10} "
		mid.append(t1_str)
	
	
	mid1 = str(mid)
	

	mid1 = mid1.replace("'","")
	m_str = m_str + mid1 + " ; "
	t_str = str(lat)+ " , "+ str(long)
	m_string = up + t_str + mid_str   + m_str + down

	fname	= "BusHeatMapofFeb1-at" + str(hour)+ "hour.html"
	f 	= open(fname,"w" )
	f.write(m_string) 
	f.close()


	return 

def Create_heat_map_2(data,marker,hour,long,lat):
	f1 	= open("heat_upper.txt","r")
	up 	= f1.read()
	f11	= open("heat_upper1.txt","r")
	mid_str	= f11.read()
	f2 	= open("heat_lower.txt", "r")
	down 	= f2.read()

	f1.close()
	f11.close()
	f2.close()
	m_str = "var taxiData =  "
	
	mid = []
	t_str = "{location: new google.maps.LatLng( " 
	
	long1 	= long - 0.02
	lat1 	= lat - 0.01
	step_long = float(0.04/200)
	step_lat  = float(0.02/100)
	
	for i in range(0,100):
		for j in range(0,200):
			if marker[i][j]==1:
				if data[i][j] == 0:
					data[i][j] = 1
				
				y = i*step_lat + lat1 
				x = j*step_long + long1
				
				t1_str = t_str + str(y)+" , " +str(x)  +" ),weight:" + str(data[i][j] * 10)+ " } "
				mid.append(t1_str)
	
	
	mid1 = str(mid)
	

	mid1 = mid1.replace("'","")
	m_str = m_str + mid1 + " ; "
	t_str = str(lat)+ " , "+ str(long)
	m_string = up + t_str + mid_str   + m_str + down

	fname	= "BusHeatMapofFeb1-at" + str(hour)+ "hour.html"
	f 	= open(fname,"w" )
	f.write(m_string) 
	f.close()


	return 

	
	

def CreateHTMLFile(data):
	f1 		= open("HTML_upper.txt","r")
	up 		= f1.read()
	f2 		= open("HTML_lower.txt","r")
	down 	= f2.read()
	
	f1.close()
	f2.close()
	
	# green 	= "var GreenBus =  "
	# orange	= "var OrangeBus = "
	# yellow	= "var YellowBus = "
	# red 	= "var RedBus 	= "
	# lime	= "var LimeBus 	= "
	way = []
	#g_list = []
	#o_list = []
	#y_list = []
	#r_list = []
	#l_list = []
	#convert list -> HTML,JS style
	temp = " "
	#va = float( 0.01026)
	for d in data:
		# if temp ==" ":
			# pass
		temp = "new Way ([ new google.maps.LatLng(" 
		temp +=	str( d['y'])	+ " , " 
		temp += str( d['x'])	+ " ), "
		temp += "new google.maps.LatLng("
		temp += str( d['y1']) + " , " + str(d['x1']) + " )],"
 
		sp = float(d['speed'])
		if   sp <= 5 :
			str_color = "'#FF0000'"
			#r_list.append(temp)
		elif sp <= 15:
			str_color = "'#FFA500'"
			#pass
			#o_list.append(temp)
		elif sp <= 25:
			str_color = "'#FFFF00'"
			#pass
			#y_list.append(temp)
		elif sp <= 40:
			str_color = "'#008000'"
			#pass
			#g_list.append(temp)
		else:
			str_color = "'#00FF00'"
			#pass
			#l_list.append(temp)
		
		temp += str_color + ")"
		way.append(temp)
		
		
	# str_r = str(r_list)
	# str_r = str_r.replace("'","")
	# red = red + str_r + "\n"
	
	# str_o = str(o_list)
	# str_o = str_o.replace("'","")
	# orange = orange + str_o + "\n"

	# str_y = str(y_list)
	# str_y = str_y.replace("'","")
	# yellow = yellow + str_y + "\n"

	# str_g = str(g_list)
	# str_g = str_g.replace("'","")
	# green = green + str_g + "\n"

	# str_l = str(l_list)
	# str_l = str_l.replace("'","")	
	# lime = lime + str_l + "\n"
	
	way = str(way)
	
	way =  " var Map_Ways = " + way  
	#way = way.replace("'","")
	#string_HTML = up+ red+ orange + yellow + green + lime + down
	string_HTML = up + way + down
	f 	= open ("ResultHTML.html","w")
	f.write(string_HTML)
	f.close()


	return 

def main():
	data = SpeedOfOneBus()
	vehicle = data[0]['vehicle']
	string_time = time.strftime( '%Y-%m-%d %H:%M:%S'
		,time.localtime( data[0]['datetime'] )  ) 
	#heading = ['_id','vehicle','datetime','x1','y1','x','y','speed']
	filename = str(string_time) +" " +str(vehicle)+".txt"
	
	f = open( filename, "w")
	temp_str = ""
	for d in data:
		temp_str =  str(d['_id'])+"\t"+str(d['vehicle'])+"\t"+str(d['datetime'])+"\t"
		temp_str += str(d['x1'])+"\t"+str(d['y1'])
		temp_str += "\t"+str(d['x'])+"\t"+str(d['y'])
		temp_str += "\t"+str(d['speed'])+"\n"
		f.write(temp_str)
	f.close()
	 #as myCSVFile:
	#	csvWriter = csv.DictWriter(myCSVFile, fieldnames = heading)
	#	csvWriter.writeheader()
	#	for d in data:
	#		csvWriter.writerow(d)
	
	
 	CreateHTMLFile( data )

	return

if __name__ == '__main__':
	main()
