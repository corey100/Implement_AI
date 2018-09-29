#!/usr/bin/env python
from flask import Flask, render_template, Response
from training import train_set, get_result
from extractFaces import clean_face

# emulated camera
from webcamvideostream import webcamvideostream

import cv2

app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    counter =0
    while True:
        counter +=1
        frame = camera.read()
        if(counter == 10): 
            grayscale = clean_face(frame)
            counter = 0
    
        ret, jpeg = None, None
        try:
            ret, jpeg = cv2.imencode('.jpg', frame)
        except:
            pass
        # print("after get_frame")
        if jpeg is not None:
            yield make_frame(jpeg)
        else:
            print("frame is none")

def make_frame(jpeg):
    return (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(webcamvideostream().start()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    # start with training the set
    #train_set()

    # Run
    app.run(host='0.0.0.0', port=5010, debug=True, threaded=True)