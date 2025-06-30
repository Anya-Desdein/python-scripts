#!/usr/bin/python3
import sys
from flask import Flask, Response, render_template
import cv2

app = Flask(__name__)

if sys.argv.__len__() < 2:
  camid = 0
else:
  camid = int(sys.argv[1])

cap = cv2.VideoCapture(camid)


@app.route('/')
def index():
    return render_template('index.html')


def generate_frames():
  while True:
    success, frame = cap.read()
    if not success:
      break
    _, buffer = cv2.imencode('.jpg', frame)

    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/live_cam')
def live_cam():
    return Response(generate_frames(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

app.run(host='0.0.0.0', port=5000)
