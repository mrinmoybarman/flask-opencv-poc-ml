from flask import Flask, render_template
from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit
import sys
import io
import base64
from PIL import Image 
import cv2 
import numpy as np
import imutils


app = Flask(__name__)
CORS(app) 


socketio=SocketIO(app, cors_allowed_origins='*')

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route('/about')
def about():
    return 'about Hello world app !'

@app.route('/test', methods=['POST','GET']) 
def authenticate():
    # data = authentication()
    # return jsonify(data)
    post_data = request.get_json()    
    return jsonify(post_data)


@socketio.on('image')
def image(data_image):
    # identify the user 
    

    # print(data_image)
    
    sbuf = io.StringIO()
    sbuf.write(data_image)

    # decode and convert into image
    b = io.BytesIO(base64.b64decode(data_image))
    pimg = Image.open(b)

    ## converting RGB to BGR, as opencv standards
    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

    # Process the image frame
    frame = imutils.resize(frame, width=700)
    frame = cv2.flip(frame, 1)
    imgencode = cv2.imencode('.jpg', frame)[1]

    # internal logic from nayanjit

    # base64 encode
    stringData = base64.b64encode(imgencode).decode('utf-8')
    b64_src = 'data:image/jpg;base64,'
    stringData = b64_src + stringData 

    # i can response back any command to the front end if needed
    emit('command', 1) 

    # distanse 

    # landmark detection

    # video recording



    # 1 means user should come closer

    # print(stringData)
    # emit the frame back
    emit('response_back', stringData)
