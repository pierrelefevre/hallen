import os
import subprocess
import threading
from flask import Flask, send_file, send_from_directory

app = Flask(__name__, static_folder='/home/pi/hallen')
latest_image_path = "/home/pi/hallen/output.png"

def capture_image():
    command = ["fswebcam", "--title", "nybodahallen.se", "--timestamp", "%Y-%m-%d %H:%M:%S", "--quiet", "--delay", "1", "--resolution", "960x720", latest_image_path]

    while True:
        subprocess.run(command, check=True)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/output.png')
def serve_image():
    try:
        return send_file(latest_image_path, mimetype='image/png')
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    thread = threading.Thread(target=capture_image, daemon=True)
    thread.start()
    app.run(host='0.0.0.0', port=8080)
