from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
# app = Flask(__name__)

app=Flask(__name__, static_url_path='', static_folder="static/")

# socketio.run(app, host='0.0.0.0')

# app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

        #   if __name__ == '__main__':
socketio.run(app, host='0.0.0.0')

@app.route("/")
def index():
    print('djhfjd')
    return render_template('index.html')

@socketio.on('/image')
def image(data_image):
    sbuf = StringIO()
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

    # base64 encode
    stringData = base64.b64encode(imgencode).decode('utf-8')
    b64_src = 'data:image/jpg;base64,'
    stringData = b64_src + stringData

    # emit the frame back
    # emit('response_back', stringData)
    