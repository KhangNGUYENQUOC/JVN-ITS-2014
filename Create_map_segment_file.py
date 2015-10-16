import BusMongoLoader as BML
import LoadData as LD

def main():
	data = LD.LoadSegmentWithPointData()
	f = open("Segment.txt","w")
	for d in data:
		f.write(str(d[0])+" "+
			str(d[1])+" "+
			str(d[2])+" "+
			str(d[3])+" "+
			str(d[4])+"\n"
			)
	return

if __name__ == '__main__':
	main()
