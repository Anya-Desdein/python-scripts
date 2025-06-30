# Multi-Camera Streaming Server (Flask + OpenCV)

This project provides a lightweight camera streaming server built with Flask and OpenCV. It supports both single and multi-camera setups and is intended for use on systems like Raspberry Pi 4 with USB cameras.

### Two Versions: Single-Camera and Multi-Camera

- `stream_camera.py` — for streaming a **single camera**.

- `stream_camera2.py` — for streaming any number of cameras by configuring them via a `.env` file
The recommended deployment is with **Gunicorn using a single process and multiple threads**. Due to limitations of the Linux video subsystem, camera devices such as `/dev/video*` **cannot be reliably accessed from multiple processes simultaneously**. Running the server in multi-process mode will typically result in only one camera functioning correctly.

## Features

- Stream one or more camera feeds over HTTP as MJPEG
- Simple Flask-based web interface with auto-generated endpoints
- Camera indices are loaded from `CAMERA_IDX` from `.env` file
- Gunicorn support for scalable threaded deployment
- Includes `.sh` script to configure required video driver quirk

## Requirements

- Python 3
- Flask
- OpenCV (`cv2`)
- NumPy
- `python-dotenv`
- `gunicorn` (only required if you want to handle multiple simultaneous viewers)

You can install the dependencies inside a virtual environment.

## Setup Instructions

### 1. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install flask opencv-python numpy python-dotenv
# Optional: add gunicorn
pip install gunicorn
```

### 3. Enable UVC bandwidth quirk

```bash
sudo bash enable_uvc_quick_fix_bandwidth.sh
```

Or, manually create the file /etc/modprobe.d/uvcvideo.conf and add:

```bash
options uvcvideo quirks=128
```

### 4. Set camera indices in .env

Create a .env file in the project root with the following format:

```bash
CAMERA_IDX=0,1,2
```

This determines which video devices (e.g., /dev/video0, /dev/video1, etc.) will be opened and streamed.

### 5. Run with Flask or Gunicorn

#### Single-camera mode (stream_camera.py)

Use this to stream a single camera directly using Flask:

```bash
python stream_camera.py <camera_id>
```

#### Multi-camera mode (stream_camera2.py)

Stream multiple cameras, supports multiple simultaneous viewers per stream. Recommended for use with **Gunicorn in single-process multi-threaded** mode.

```bash
gunicorn --threads <thread_count> --bind <host:port> stream_camera2:app
```