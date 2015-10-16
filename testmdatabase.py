import mdatabase
import datetime


def main():
	i = datetime.datetime.now()
	print( mdatabase.insert_new_gps( "asdf",
					123.0,
 					321.0, 
					i.date(), 
					i.time() ) ) 




