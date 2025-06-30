#!/usr/bin/python3
import numpy as np
import sys

from flask import Flask, Response
import cv2

app = Flask(__name__)

if sys.argv.__len__() < 2:
  camid = 0
else:
  camid = int(sys.argv[1])

cap = cv2.VideoCapture(camid)

def generate_frames():
  while True:
    success, frame = cap.read()
    if not success:
      break
    _, buffer = cv2.imencode('.jpg', frame)

    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

app.run(host='0.0.0.0', port=5000)
