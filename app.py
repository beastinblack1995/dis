from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
from PIL import Image  , ImageOps
import cv2
import io
from flask import Flask, render_template, Response
import cv2
import cv2
import numpy as np
import face_recognition as face_rec
from base64 import b64encode
import io
from PIL import Image  
import os
from datetime import  datetime
from flask import Flask, render_template, request, redirect, flash, url_for

import urllib.request
import base64
from werkzeug.utils import secure_filename

import os
path = 'employee images'
employeeImg = []
employeeName = []
myList = os.listdir(path)
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def resize(img, size) :
    width = int(img.shape[1]*size)
    height = int(img.shape[0] * size)
    dimension = (width, height)
    return cv2.resize(img, dimension, interpolation= cv2.INTER_AREA)



def findEncoding(images) :
    imgEncodings = []
    for img in images :
        img = resize(img, 0.50)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodeimg = face_rec.face_encodings(img)[0]
        imgEncodings.append(encodeimg)
    return imgEncodings
def MarkAttendence(name):
    with open('attendence.csv', 'r+') as f:
        myDatalist =  f.readlines()
        nameList = []
        for line in myDatalist :
            entry = line.split(',')
            nameList.append(entry[0])

        if name not in nameList:
            now = datetime.now()
            timestr = now.strftime('%H:%M')
            f.writelines(f'\n{name}, {timestr}')
            statment = str('welcome to seasia' + name)

for cl in myList :
    curimg = cv2.imread(f'{path}/{cl}')
    employeeImg.append(curimg)
    employeeName.append(os.path.splitext(cl)[0])

EncodeList = findEncoding(employeeImg)

 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    print(file)
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        frame = cv2.imread('static/uploads/' + filename)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        frame = face_rec.load_image_file('static/uploads/'+filename)

        frame = img_to_array(frame)


        facesInFrame = face_rec.face_locations(frame)
        encodeFacesInFrame = face_rec.face_encodings(frame, facesInFrame)
            

        for encodeFace, faceloc in zip(encodeFacesInFrame, facesInFrame) :
            matches = face_rec.compare_faces(EncodeList, encodeFace)
            facedis = face_rec.face_distance(EncodeList, encodeFace)
            print(facedis)
            if min(facedis) < 0.5:
                matchIndex = np.argmin(facedis)

                print(matchIndex)


                name = employeeName[matchIndex].upper()
                y1, x2, y2, x1 = faceloc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                cv2.rectangle(frame, (x1, y2-25), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                #MarkAttendence(name)
                
        
        
        
        
        
        
        
        
        
        
        
        
        
        cv2.imwrite('static/uploads/pred_' + filename, frame)
        
        
        
        
        
        
        
        
        
        print(image)
        
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        print(filename)
        return render_template('index.html', filename=  filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    print('hi')
    return redirect(url_for('static', filename='uploads/pred_' + filename), code=301)

 
if __name__ == "__main__":
    app.run()
