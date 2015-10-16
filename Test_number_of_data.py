import BusMongoLoader as BML
import CreateBusMap as CBM
import numpy

def main():
	long	= float(106.6959116) 
	lat 	= float(10.7826196)
	start 	= int( 1422723602+60*60*6 )
	end 	= start + 60*60*12
	data_4h	= BML.LoadAllBusWithin(long,lat,start,end)
	
	long1 	= long - 0.02
	long2 	= long + 0.02
	
	lat1 	= lat - 0.01
	lat2	= lat + 0.01
	
	step_long = float(0.04/200)

	step_lat  = float(0.02/100)
	a =numpy.zeros(shape=(100,200))
	road_marker =numpy.zeros(shape=(100,200))
	count_5 = 0
	count_10 =0
	for d in data_4h: 
		m_long = d['x']
		m_lat = d['y']
		
		h_long = int((m_long  - long1)/step_long)
		h_lat = int((m_lat  - lat1)/step_lat)
		
		a[h_lat][h_long] += 1
		
		
	for i  in range(0,100):
		for j in range(0,200):
			if a[i][j] > 5:
				road_marker[i][j] = 1 
	
	
	for i in range(6*12,19*12):
		print str(i)
		start = int(1422723602 + 60*5*i)
		end = start + 60*5
		long = float(106.6959116) 
		lat = float(10.7826196)
		data = BML.LoadAllBusWithin(long,lat,start,end)
		
		a = numpy.zeros(shape=(100,200))
		for d in data: 
			m_long = d['x']
			m_lat = d['y']
		
			h_long = int((m_long  - long1)/step_long)
			h_lat = int((m_lat  - lat1)/step_lat)
		
			a[h_lat][h_long] += 1
			#print str(len(data
			
		CBM.Create_heat_map_2(a,road_marker,i,long,lat)
	
	return
	
	
if __name__ == '__main__':
	main()