#!/usr/bin/python3
from flask import Flask, Response, render_template
import cv2

from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv();

idx_from_env = os.getenv("CAMERA_IDX", "")
camera_indxes = [int(i.strip()) for i in idx_from_env.split(",") if i.strip().isdigit()]

cameras = []
camera_endpoints = []

for idx in camera_indxes:
    cap = cv2.VideoCapture(idx)
    cameras.append(cap)

    if cap.isOpened():
        print(f"Camera {idx} opened")
    else:
        print(f"Opening camera failed for {idx} idx")

    path = f"cam/id{idx}"
    camera_endpoints.append(path)

def generate_frames(cap):
  while True:
    success, frame = cap.read()
    if not success:
      break
    _, buffer = cv2.imencode('.jpg', frame)

    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')


@app.route("/cam/id<int:cam_id>")
def stream(cam_id):
    path = f"cam/id{cam_id}"
    idx = camera_endpoints.index(path)
    cap = cameras[idx]

    return Response(generate_frames(cap), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html', camera_endpoints=camera_endpoints)

app.run(host='0.0.0.0', port=5000)
