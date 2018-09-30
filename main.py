#!/usr/bin/env python
from flask import Flask, render_template, Response
from training import train_set, get_result
from extractFaces import clean_face
from movies import getMovies
from speech2text import startcoolmusic

# emulated camera
from webcamvideostream import webcamvideostream
emotions = ["neutral", "anger", "disgust", "happy", "surprise", "sadness"]

import cv2

app = Flask(__name__)
grayscale = None
prediction = 0

# the index page layout
@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


# generator method for buildign a camera display
def gen(camera):
    """Video streaming generator function."""
    count = 0
    while True:
        count += 1
        frame = camera.read()
        if(count == 100):
            global grayscale
            global prediction
            count = 0
            cleanedFrame = clean_face(frame)

            pred, conf = get_result(cleanedFrame)
            prediction = pred

            try:
                font                   = cv2.FONT_HERSHEY_SIMPLEX
                bottomLeftCornerOfText = (10,310)
                fontScale              = 1
                fontColor              = (255,255,255)
                lineType               = 2

                cv2.putText(cleanedFrame, emotions[pred],
                    bottomLeftCornerOfText, 
                    font, 
                    fontScale,
                    fontColor,
                    lineType)
                _, jpegGray = cv2.imencode('.jpg', cleanedFrame)
                grayscale = make_frame(jpegGray)

            except:
                pass

        jpeg = None
        try:
            _, jpeg = cv2.imencode('.jpg', frame)
            
        except:
            pass
        if jpeg is not None:
            yield make_frame(jpeg)

        else:
            print("frame is none")

# This method constructs a frame for display
def make_frame(jpeg):
    return (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

# Get the video feed
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(webcamvideostream().start()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Get the grayscale
@app.route('/creepy_feed')
def gray_scale():
    return Response(grayscale, mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/form-example', methods=['POST']) #allow post requests to be passed
def form_example():
    pass

# Show movies
@app.route('/show_movies')
def show_movies():
    videos = getMovies(emotions[prediction])
    return render_template('movies.html', videos=videos)

if __name__ == '__main__':
    #start the music listener
    startcoolmusic()

    # start with training the set
    train_set()

    
    # Run
    app.run(host='0.0.0.0', port=5010, debug=False, threaded=True)