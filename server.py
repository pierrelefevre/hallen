import subprocess
import threading
import time
from flask import Flask, send_file, send_from_directory

app = Flask(__name__, static_folder='/home/pi/hallen')
latest_image_path = "/home/pi/hallen/output.png"

def capture_image():
    command = ["fswebcam", "--title", "nybodahallen.se","--line-colour", "#00000000", "--banner-colour", "#00000000", "--font", "/home/pi/hallen/sl.ttf:10", "--no-shadow", "--timestamp", "%Y-%m-%d %H:%M:%S", "--quiet", "--delay", "1", "--resolution", "960x720", latest_image_path]

    while True:
        subprocess.run(command, check=True)
        time.sleep(10)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/output.png')
def serve_image():
    try:
        return send_file(latest_image_path, mimetype='image/png')
    except Exception as e:
        return str(e)
    
@app.route('/favicon.ico')
def serve_icon():
    try:
        return send_file("/home/pi/hallen/favicon.ico", mimetype='image/x-icon')
    except Exception as e:
        return str(e)
    
@app.route('/sl.ttf')
def serve_font():
    try:
        return send_file("/home/pi/hallen/sl.ttf", mimetype='font/ttf')
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    thread = threading.Thread(target=capture_image, daemon=True)
    thread.start()
    app.run(host='0.0.0.0', port=8080)
