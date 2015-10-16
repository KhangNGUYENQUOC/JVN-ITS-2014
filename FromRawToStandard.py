__author__ = 'Phoe'

import LoadData as LD
import os
import datetime
import math
import numpy
import mysql
import mdatabase as mData
import csv


def Hash_grid_index(long,lat):
	if (106.43 < long < 106.97) and (10.63 < lat < 10.98):
		m_long = int( long * 100 )
		m_lat  = int( lat * 100)
		d_long = m_long - 10643
		d_lat  = m_lat - 1063
		
		g_index = d_lat * 54 + d_long
		
		return g_index 
	
	return -1
def dot_pro(Ax,Ay, Bx,By):
	return float( Ax*Bx + Ay*By )

def magnitude(Ax,Ay):
	return float(math. sqrt(Ax*Ax + Ay*Ay) )

def Calculate_distance(Ax,Ay, Bx,By, Cx,Cy):    #find distance point -> segment

	A_x = Ax
	A_y = Ay
	
	AB_x = Bx - Ax
	AB_y = By - Ay

	AC_x = Cx - Ax
	AC_y = Cy - Ay

	mag_AB = math.sqrt( AB_x * AB_x + AB_y * AB_y  )
	if mag_AB ==0:
		return [-1,-1]
	
	AH = float( dot_pro(AB_x,AB_y, AC_x,AC_y)/mag_AB )
	
	H_x = A_x
	H_y = A_y 
	
	if 0< AH and AH < mag_AB:
		AC = magnitude(AC_x,AC_y)
		mag_CH = math.sqrt( AC*AC - AH*AH )
		ratio = float( AH / mag_AB )
		H_x = (Bx - Ax)*ratio + Ax
		H_y = (By - Ay)*ratio + Ay
	else:
		if AH >= mag_AB:
			ratio = 1
			mag_CH = magnitude( Bx - Cx, By - Cy)
			H_x = Bx
			H_y = By
			
		if AH <= 0:
			ratio = 0
			mag_CH = magnitude( AC_x, AC_y)
			H_x = Ax
			H_y = Ay

	return [mag_CH, ratio, H_x, H_y]


def pnt2line(pnt, start, end):
    line_vec = vector(start, end)
    pnt_vec = vector(start, pnt)
    line_len = length(line_vec)
    line_unitvec = unit(line_vec)
    pnt_vec_scaled = scale(pnt_vec, 1.0/line_len)
    t = dot(line_unitvec, pnt_vec_scaled)    
    if t < 0.0:
        t = 0.0
    elif t > 1.0:
        t = 1.0
    nearest = scale(line_vec, t)
    dist = distance(nearest, pnt_vec)
    nearest = add(nearest, start)
    return (dist, nearest)

def Create_Standard():

	list_seg 	= LD.LoadSegmentWithPointData()
	list_grid	= LD.LoadGridData()
	list_link	= LD.LoadLinkGridSegment()
	
	#--------------------danger!!!!-----------
	#if load all, then data would dublicate!--
	#list_gps 	= LD.LoadAllLocationData()
	#-----------------------------------------
#	list_gps	= LD.Load_current_15_min_Raw()
	
	#list_gps	= LD.Load_Location_previous_sec( 86400  )

	link_matrix 	= LD.LoadLinkMatrix()
	conn = mysql.connector.connect( host 	='localhost',
					database='ITS2014',
					user	='root',
					password='5fe5e619eaff')

	cur = conn.cursor()
	query =("insert into StandardizedData "
		"(sampleID, segmentID, velocity, locationRatio, distance) "
		"values (%s, %s, %s, %s, %s)" )



	load_query = "select * from LocationData L where L.sampleDate = '2015-06-15' and L.googleSpeed is not null  " 
	list_gps 	= LD.Load(load_query)
	print "Number of Raw location: " + str( len(list_gps) )
	list_stand = []


	for gps in list_gps:
		#pass
		#data = " "
		ratio = -1
		#find the gridID using the long and latt of GPS point!
		g_index = Hash_grid_index( gps[2] , gps[3] )
		#from the gridID, jump to the link[grid]
		candidate_list = link_matrix[g_index]
		min_dist = -1
		min_seg  = -1
		
		Hx = float(0)
		Hy = float(0)
		if len(candidate_list) == 0:
			print "can not found any segment"
		else:
			for segID in candidate_list:
				cur = list_seg[segID-1]
				Ax = cur[1]
				Ay = cur[2]
				Bx = cur[3]
				By = cur[4]
				#(dist,m_ratio) = Calculate_distance(Ax,Ay,Bx,By,gps[2],gps[3])
				temp_data = Calculate_distance(Ax,Ay, Bx,By, gps[2],gps[3])
				#print str(temp_data)
				#print str(temp_data[0]) +"\t" + str(temp_data[1])
				dist = temp_data[0]
				m_ratio = temp_data[1]
				if (min_dist == -1)or(dist < min_dist):
					min_dist = dist
					min_seg  = segID
					ratio 	 = m_ratio
					Hx = temp_data[2]
					Hy = temp_data[3]
				
		# save seg to standardized data
		if not (min_seg==-1):
			pass
			#print "gps id: " +str( gps[0]) +"\t  segID: "  +str(min_seg)
		else:
			print "gps id: " + str( gps[0]) + "\t NO FOUND!"	
			return 
		# data to save to standardized data:
		speed = gps[6]
		#print str(speed)


		############################
		#speed = 0
 		####### ATTENTION HERE!!!!!!!

		data = (gps[0], min_seg, speed , ratio, min_dist )
		stand = [gps[0],min_seg,speed,ratio,min_dist]
		list_stand.append(stand)
		#print "Execute query... Saving one more Standard data"
		#print query
		#print data
		#mData.Save_database(query,data)
		#cur.execute( str(query ))#, str(data) )
		#print str(data)
		
	#conn.commit()
#	cur.close()
#	conn.close()
	print "Exiting..."
	print " "
	print " "

	return list_stand

	
def MapSampleToSegment(sample_data):      #return segment ID of the nearest segment 
	list_seg 	= LD.LoadSegmentWithPointData()
	list_grid	= LD.LoadGridData()
	list_link	= LD.LoadLinkGridSegment()
	
	#--------------------danger!!!!-----------
	#if load all, then data would duplicate!--
	#list_gps 	= LD.LoadAllLocationData()
	#-----------------------------------------
#	list_gps	= LD.Load_current_15_min_Raw()
	
	#list_gps	= LD.Load_Location_previous_sec( 86400  )

	link_matrix 	= LD.LoadLinkMatrix()
	conn = mysql.connector.connect( host 	='localhost',
					database='ITS2014',
					user	='root',
					password='5fe5e619eaff')

	cur = conn.cursor()
	query =("insert into StandardizedData "
		"(sampleID, segmentID, velocity, locationRatio, distance) "
		"values (%s, %s, %s, %s, %s)" )

	#print "Number of Raw location: " + str( len(list_gps) )
	list_stand = []
	list_Bus_segment = []
	list_fail_sample = []
	counter = 1
	for gps in sample_data:
		#pass
		#data = " "
		ratio = -1
		point_longitude = float (gps["x"])
		point_lattitude = float (gps["y"])
		#print str( point_longitude )
		#print str( point_lattitude )
		if counter%1000 ==0:
			print counter
		counter += 1
		#find the gridID using the long and latt of GPS point!
		g_index = Hash_grid_index( point_longitude, point_lattitude)  #long,latt
		#print str(g_index)
		#from the gridID, jump to the link[grid]
		candidate_list = link_matrix[g_index]
		min_dist = -1
		min_seg  = -1
		
		Hx = float(0)
		Hy = float(0)
		if len(candidate_list) == 0:
			print "can not found any segment"
		else:
			for segID in candidate_list:
				cur = list_seg[segID-1]
				Ax = cur[1]
				Ay = cur[2]
				Bx = cur[3]
				By = cur[4]
				#(dist,m_ratio) = Calculate_distance(Ax,Ay,Bx,By,gps[2],gps[3])
				temp_data = Calculate_distance(Ax,Ay, Bx,By, gps[2],gps[3])
				#print str(temp_data)
				#print str(temp_data[0]) +"\t" + str(temp_data[1])
				dist = temp_data[0]
				m_ratio = temp_data[1]
				if (min_dist == -1)or(dist < min_dist):
					min_dist = dist
					min_seg  = segID
					ratio 	 = m_ratio
					Hx = temp_data[2]
					Hy = temp_data[3]
				
		# save seg to standardized data
		if not (min_seg==-1):
			#pass
			list_Bus_segment.append( [int( min_seg),Hx,Hy] )
			#print "gps id: " +str( gps[0]) +"\t  segID: "  +str(min_seg)
		else:
			#print "gps sample:  NO FOUND!"	
			#return
			list_fail_sample.append([str(gps["_id"] )] ) 
		# data to save to standardized data:
		#speed = gps[6]
		#print str(speed)


		############################
		#speed = 0
 		####### ATTENTION HERE!!!!!!!
		#list_Bus_segment.append(int(min_seg))
		#data = (gps[0], min_seg, speed , ratio, min_dist )
		#stand = [gps[0],min_seg,speed,ratio,min_dist]
		#list_stand.append(stand)
		#print "Execute query... Saving one more Standard data"
		#print query
		#print data
		#mData.Save_database(query,data)
		#cur.execute( str(query ))#, str(data) )
		#print str(data)
		
	#conn.commit()
#	cur.close()
#	conn.close()
	print "Exiting..."
	print " "
	print " "

	c = csv.writer( open("bus_mapping_fail.csv","wb" ) )
	c.writerow(list_fail_sample)
	#return list_stand
	return list_Bus_segment


def main():

	data= Create_Standard()
	if data== -1:
		print "++++++++++++++++++++++fail+++++++++++++++++++"
	else:
		print str(len(data))
	query_segment = "select * from SegmentData"
	list_seg 	= LD.Load(query_segment)
	number_of_seg 	=len(list_seg)
	traffic = []
	for i in range(0, number_of_seg):
		traffic.append([])
	
	print "Creating a new traffic condition"
	for d in data:
		cur_seg_id 	= d[1]
		cur_seg 	= traffic[cur_seg_id-1]
		#print str( traffic[cur_seg_id -1] )
		if len(cur_seg) ==0:
			#temp = [cur_seg_id, d[2], 1 ]
			traffic[cur_seg_id -1].append(cur_seg_id)
			traffic[cur_seg_id -1].append(d[2])
			traffic[cur_seg_id -1].append(1)
		else:
			#print str(traffic[cur_seg_id-1])
			traffic[cur_seg_id-1][1] += d[2]
			traffic[cur_seg_id-1][2] += 1	
	
	for t in traffic:
		if not( len(t)==0 ):
			print str( t[1] )
			pass
			speed =float( t[1]/t[2] )
			print "Seg ID:"+ str( t[0] )+"\tSpeed: " + str(speed)+"\tNumber of sample: " + str(t[2])
	
	
	return 

if __name__ == '__main__':
	main()
