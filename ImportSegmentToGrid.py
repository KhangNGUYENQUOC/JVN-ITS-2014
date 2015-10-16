__author__ = 'Phoe'

import 	os
import 	mysql
import 	mysql.connector
from 	mysql.connector	import Error
from 	math		import radians, cos, sin, asin, sqrt
import 	datetime
import 	second
import 	LoadData
	
import xml.etree.ElementTree 	as ET

#load segment data from database
def LoadSegmentData():
	print "Load Segment data here!"
	print "-----------------------"
	conn = mysql.connector.connect(	host	= 'localhost',
					database= 'ITS2014',
					user	= 'root',
					password= '5fe5e619eaff')
	if not conn.is_connected():
		print "Database connection fail!"
		return "fail"
	cur = conn.cursor()

	query_data = "select * from SegmentData"
	cur.execute(query_data)
	print "*"
	my_Segment = cur.fetchall()
	print "*"
	cur.close()
	conn.close()
	print " "
	print " "

	return my_Segment

#Waring, this function should run ONLY 1 time!
def Create_Grid_row():
	print "Create Grid data here!"
	print "----------------------"
	
	conn = mysql.connector.connect(	host	= 'localhost',
					database= 'ITS2014',
					user	= 'root',
					password= '5fe5e619eaff')
	if not conn.is_connected():
		print "Database connection fail!"
		return "fail"

	cur = conn.cursor()

	add_grid = ("insert into GridData "
		" (longitude, lattitude) "
		" values (%s , %s) " )

	
	org_x = 106.43
	org_y = 10.63
	#get in the for loop-create grid 
	for y in range(0,35):
		cur_y = org_y + float(y)/100
		#print str(cur_y) 
		for x in range(0,54):
			cur_x = org_x + float(x)/100
			#print "\t" + str(cur_x)
			data_grid = ( cur_x, cur_y )
			cur.execute(add_grid, data_grid)


	print "*"

	conn.commit()
	print "*"
	cur.close()
	conn.close()
			
	print " "
	print " "
	return


def segment_inside_grid(seg,grid):
	left 	= grid[1]
	right 	= grid[1] + 0.01
	up	= grid[2] + 0.01
	down	= grid[2]

	if (left <= seg[1] <= right) and (down <= seg[2] <= up) :
		#print str(grid[0]) +"\t"+ str(left) + "\t" + str(seg[1])+ "\t" + str(right)
		return 1
	elif (left <= seg[3] <= right) and (down <= seg[4] <= up):
		#print str(grid[0]) +"\t"+ str(left) + "\t" + str(seg[3])+ "\t" + str(right)
		return 1

	#print str(segment[2]) + str(segment[3])
	return 0	#false	:	0 

def In_order(x1,y1, x2,y2, x3,y3):
	ax = x2 - x1
	ay = y2 - y1
	
	bx = x3 - x2
	by = y3 - y2

	cx = x3 - x1
	cy = y3 - y1

	if (cy == ay + by) and (cx == ax + bx):
		return 1
	else:
		return 0



#return 1 if they are intersection; 0 otherwise
def segment_intersection(x1, y1, x2, y2 , Ax, Ay, Bx, By):
	#m1 = float( (y2-y1)/(x2-x1) ) 
	#c1 = float ( y1 - m1*x1 ) 
	#m2 = float( (Ay - By)/(Ax-Bx) )
	#c2 = float ( Ay - m2*Ax)

	a1 = y1 - y2
	b1 = x2 - x1
	c1 = x1 * y2 - x2 * y1

	a2 = Ay - By
	b2 = Bx - Ax
	c2 = Ax * By - Bx * Ay 

	#find determinat
	x = y = float( 0 )

	deter = a1 * b2 - a2 * b1
	if deter == 0:
		#do nothing here! because det ==0!
		return 0
	else:
		#det != 0
		x = (c1 * b2 - b1 * c2)/deter
		y = (a1 * c2 - a2 * c1)/deter
		if In_order(Ax,Ay, x,y, Bx, By) and In_order(x1,y1, x,y, x2,y2):
			print str(1)
			return 1
		else:
			return 0
		 
	
	
	return 0

def segment_intersect_grid(segment,grid):
	#setting
	x1 = segment[1]
	y1 = segment[2]

	x2 = segment[3]
	y2 = segment[4]


	
	Ax = grid[1]
	Ay = grid[2] + 0.01
	
	Bx = grid[1] + 0.01
	By = grid[2] + 0.01

	Cx = grid[1] + 0.01
	Cy = grid[2]

	Dx = grid[1]
	Dy = grid[2]

	if segment_intersection(x1,y1, x2,y2, Ax,Ay, Bx,By) ==1:
		return 1
	elif segment_intersection(x1,y1, x2,y2, Bx,By, Cx,Cy) ==1:
		return 1
	elif segment_intersection(x1,y1, x2,y2, Cx,Cy, Dx,Dy) ==1:
		return 1
	elif segment_intersection(x1,y1, x2,y2, Ax,Ay, Dx,Dy) ==1:
		return 1
	
	return 0 	#false 	:	0

def main():

	i = datetime.datetime.now()
	print "Starting at: " + str(i)
	#load segment data from: 	SegmentData
#	my_seg = LoadSegmentData() 
#	if my_seg == "fail":
#		return

#	Create_Grid_row()
	
	seg_and_point_data = LoadData.LoadSegmentWithPointData()
#	t = "\t \t"
#	for r in SegAndPointData:
#		a = str(r[0]) + t
#		a = a + str(r[1]) + t + str(r[2]) + t
#		a = a + str(r[3]) + t + str(r[4])
#		print a
#	Done!


	#create grid data to: 		GridData
#	Done!

	#Load Grid data

	grid_data = LoadData.LoadGridData() 
	#Done




	count_inside = 0
	count_intersect = 0
	
	conn = mysql.connector.connect(	host	= 'localhost',
					database= 'ITS2014',
					user 	= 'root',
					password= '5fe5e619eaff' )

	cur = conn.cursor()


	add_grid_segment = ("insert into GridSegment "
		" (GridID, SegmentID ) "
		" values (%s, %s)" )
	

	

	#create the relationship for segments and grids
	print "Comparing Grids and Segments"
	print "----------------------------"
	for g in grid_data:
		print str(g[0])
		for s in seg_and_point_data:
			#compare here!
			if segment_inside_grid(s,g)== 1:
				#add
				data_grid_segment = (g[0], s[0] )
				cur.execute(add_grid_segment, 
					data_grid_segment) 
				
				#print "inside"
				count_inside += 1
				
			elif segment_intersect_grid(s,g)== 1:
				#add
				count_intersect += 1
				print str( g[0] ) + "\tintersect"
		conn.commit()
		print "Committed database!"
	
	cur.close()
	conn.close()
	#save the link into: 		GridSegment
	print " "
	print ( "Number of inside: " + str(count_inside) )
	print ( "Number of intersection: " + str(count_intersect) )
	
	os.system('clear')
	print "Started at: " + str(i)
	i1 = datetime.datetime.now()
	print "Done at:	   " + str(i1)

	return

if __name__ == '__main__':
	main()
