import urllib
from time import sleep


def main():
	rnum = 1 
	
	f = open('BusRoad.txt','w')
	
	
	for i in range(1,200):
		rnum = i
		print( str(i) )
		truestring = "true"
		url1 = "http://mapbus.ebms.vn/ajax.aspx?action=GetFullRoute&rid=" + str(rnum) + "&isgo=" + truestring
		
		falsestring = "false"
		url2 = "http://mapbus.ebms.vn/ajax.aspx?action=GetFullRoute&rid=" + str(rnum) + "&isgo=" + falsestring
		
		res1 = urllib.urlopen(url1)
		
		res2 = urllib.urlopen(url2)
		
		html1 = res1.read()
		html2 = res2.read()
		f.writelines(html1)
		f.writelines(html2)
		sleep(0.5)
		
	f.close()
		
if __name__ == '__main__':
	main()