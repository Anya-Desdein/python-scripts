# Multi-Camera Streaming Server (Flask + OpenCV)

This project provides a lightweight camera streaming server built with Flask and OpenCV. It supports both single and multi-camera setups and is intended for use on systems like Raspberry Pi with USB cameras.

The **enable_uvc_quick_fix_bandwidth.sh** script limits the bandwidth per camera, preventing a single device from monopolizing the connection.

## Features

- Stream one or more camera feeds over HTTP as MJPEG
- Simple Flask-based web interface with auto-generated endpoints
- Camera indices are loaded from `CAMERA_IDX` from `.env` file
- Includes `.sh` script to configure required video driver quirk

## Requirements

- Python 3
- Flask
- OpenCV (`cv2`)
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
pip install flask opencv-python python-dotenv
# Optional: add gunicorn
pip install gunicorn
```

### 3. Enable UVC bandwidth quirk

You might need escalated privileges to write to /etc/modprobe.d/.
```bash
./enable_uvc_quick_fix_bandwidth.sh
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

```bash
python stream.py
```

Or use Gunicorn, which supports multiple simultaneous viewers per stream. Recommended for use with **single-process multi-threaded** mode.

```bash
gunicorn --threads <thread_count> --bind <host:port> stream:app
```
