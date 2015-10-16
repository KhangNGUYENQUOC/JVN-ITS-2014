import BusMongoLoader as BML
import CreateBusMap as CBM
import csv
import time

def Export_heat_html():
	for i in range(6*12,19*12):
		print str(i)
		start = int(1422723602 + 60*5*i)
		end = start + 60*5
		long = float(106.6959116) 
		lat = float(10.7826196)
		data = BML.LoadAllBusWithin(long,lat,start,end)
		#print str(len(data
		CBM.Create_heat_map(data,i,long,lat)
	return
def SaveToFile(data, long, lat, start, end):
	string_date = time.strftime('%Y-%m-%d %H:%M:%S',
		time.localtime(start))
	file_name = str(long)+ ","+str(lat)+"at"+string_date+".csv"

	heading = ['vehicle','datetime','x','y']
	with open (filename, "w") as myCSVFile:
		csvWriter = csv.DicWriter(myCSVFile, fieldnames = heading)
		csvWriter.writeheader()
		for d in data:
			csvWriter.writerow(d)
	return

def main():
	start = int( 1422723602)
	end = start + 60*60*24

	long 	= float(10.7826196) 
	lat 	= float(106.6959116)
	#Export_heat_html()
	data = BML.LoadAllBusWithin(long,lat,start,end)
	SaveToFile(data, long, lat, start, end)
	return


if  __name__ == '__main__':
	main()
