import os
import subprocess
from flask import Flask, send_file

app = Flask(__name__)

def capture_image():
    command = ["fswebcam", "--no-banner", "--quiet", "--resolution", "960x720", "/home/pi/hallen/output.png"]
    subprocess.run(command, check=True)

@app.route('/')
def serve_image():
    capture_image()
    return send_file('/home/pi/hallen/output.png', mimetype='image/png')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
