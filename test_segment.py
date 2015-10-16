__author__ = "Phoe"

import ImportSegmentToGrid as ISTG
import os

def main():
	print "asfd asdf as"
	os.system('clear')

	
	x1 = 1 
	y1 = 1
	
	x2 = 2
	y2 = 3
	
	Ax = 3
	Ay = 0

	Bx = 3
	By = 4

	print (str ( ISTG.segment_intersection(x1,y1, x2,y2, Ax,Ay, Bx,By ) ) ) 

	return

if __name__ == '__main__':
	main()
