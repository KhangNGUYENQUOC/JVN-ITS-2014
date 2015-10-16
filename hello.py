__author__ = 'Phoe2'
from flask import Flask, request , redirect , url_for
import werkzeug
from werkzeug.wrappers import Response ,Request
import json
import os
import mysql
import mysql.connector
from mysql.connector import Error
import BusMongoLoader as BML
import mdatabase
import flask
import datetime

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

UPLOAD_FOLDER = '/DataPath'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'json'])

returnString = ''

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def hello_world():
	return flask.render_template('index.html')
	#return 'Home page, with nothing to show'



@app.route('/get_color', methods=['GET'])
def getcolor():
	#mstr='{"userId": 1,"id": 1,  "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit","body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"}'
	return str("FF0000")         
	#return (mstr)



@app.route('/get_heatmap_data',methods=['GET','POST'])
def getheatmapdata():
	start = int(1422723602 + 60*60*9)
	end = start + 60*0 + 1
	data = BML.LoadAllBusData(start,end)
	#print data[0]
	ret_data =  json.dumps(data) 
	#print ret_data[0]
	#print len(data) 
	#return str(ret_data)
	return ret_data
	#print str(jsonify(**data) )
	#return jsonify(**data)
	#return jsonify(ret_data)



@app.route('/raw_data_upload', methods=[ 'POST', 'GET'])
def rawdataupload():
    if request.method == 'POST':
        myData = request.get_data()
        #get raw data here!
        #returnString = 'Nhan duoc roi'
        myObject = myData
	#return myData
	

	i = datetime.datetime.now()
	print "-----------------------------------------------------------------------"
	print "New data upload at: 		" + str(i)
	
	#return str( i )

	#save raw data to file for backup
	dir = 'temporatorydata/' + str( i.date() )+ '/'
	if not os.path.exists(dir):
		os.makedirs(dir)

	filename = 'temporatorydata/'+str(i.date())+'/'+str(i.time())+'.json'
	#print str(filename)
	a = open( filename , 'w')
	a.write( myObject + '\n')
	a.close()
	
	#return str(i)
	#return myObject
	returnStr = mdatabase.insert_new_JSON_data(filename) 
	print str(returnStr)        




        ############################################
	#parse JSON data
	#f=open(filename, 'r')
	#dataJSON = json.load(f)
	#f.close()
	#numberOfJsonItem = len(dataJSON)
	#return str ( dataJSON ) 
	#return str ( len(dataJSON) )
	#returnString = ' ' + numberOfJsonItem
	
	#print len(dataJSON)
	#return returnString	
	
	#for index in dataJSON:
		#do the task for each item of the JSON array here
		#print index['deviceID']
	#	curDeviceID = str ( index['deviceID'] ) 
	#	curLong = float (index['longitude'] )
	#	curLatt = float (index['latitude'] )
		#print curLatt
	#	curSampleDate = str (index['sampleDate'] ) + ""
		
		#print( curSampleDate)

	#	temp = datetime.datetime.strptime(	curSampleDate, "%Y-%m-%d %H:%M:%S")
		#print( index['sampleDate'] )
	#	returnStr = mdatabase.insert_new_gps( 	curDeviceID,
	#						curLong,
	#						curLatt,
	#						temp.date(),
	#						temp.time())
		
		#returnStr hold the result of database query action.
		#should print it out to see the result.
        ###############################################
	
	if returnStr=="true":
		log = "Data saved into database"
		print "--------------------------------------------------------------"
	else:
		log = "Something wrong happened with database"
		print "**************************************************************"
	return str( log	 )

	

	#go to database - insert new data
        #returnString =  mdatabase.insert_new_gps(1,1,1,1)
	
	
	#insert prototype: ("asdf",
	#		123.0,
	#		312.0,
	#		i.date()
	#		i.time() )


        #myJsonData = json.load(myData)

    

        #return returnString + " " + returnStr
    else:
        if request.method == 'GET':
            return '"GET" but this is the raw data upload section! '



if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5005)
    #app.run(debug='true')
    #app.run()
