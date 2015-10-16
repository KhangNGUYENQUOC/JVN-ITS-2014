__author__ = 'Phoe2'
from flask import Flask, request , redirect , url_for
import werkzeug
from werkzeug.wrappers import Response ,Request
import json
import os

app = Flask(__name__)


UPLOAD_FOLDER = '/DataPath'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'json'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def hello_world():
    return 'Home page, with nothing to show'



@app.route('/file_upload', methods = ['POST','GET'])
def fileupload():
    if request.method == 'POST':
         file = request.get_data()
         return 'catch file, but stuck!'
             #request.files()
         #file = request.files['file']
         # Check if the file is one of the allowed types/extensions
         # if file and allowed_file(file.filename):
         #    return 'File and allowed'
         #     # Make the filename safe, remove unsupported chars
         #     #filename = werkzeug.secure_filename(file.filename)
         #     # Move the file form the temporal folder to
         #     # the upload folder we setup
         #    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
         #     # Redirect the user to the uploaded_file route, which
         #     # will basicaly show on the browser the uploaded file
         #    return (redirect(url_for('uploaded_file', filename=filename)) )
         #    #return 'post'


@app.route('/raw_data_upload', methods=[ 'POST', 'GET'])
def rawdataupload():
    if request.method == 'POST':
        myData = request.get_data()
        #get raw data here!
        myObject = myData


        #myJsonData = json.load(myData)



        return 'Nhan duoc roi :v'
    else:
        if request.method == 'GET':
            return '"GET" but this is the raw data upload section! '



if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 22)
    #app.run(debug='true')
    #app.run()
