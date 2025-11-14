import subprocess
import threading
import time
from flask import Flask, send_file, send_from_directory, Response
import datetime
import sys
import io

app = Flask(__name__, static_folder="/home/pi/hallen")
latest_image_data = None
image_lock = threading.Lock()


def capture_image():
    global latest_image_data

    command = [
        "fswebcam",
        "--title",
        "nybodahallen.se",
        "--line-colour",
        "#00000000",
        "--banner-colour",
        "#00000000",
        "--no-shadow",
        "--timestamp",
        "%Y-%m-%d %H:%M:%S",
        "--quiet",
        "--delay",
        "1",
        "--resolution",
        "960x720",
        "-",
    ]

    while True:
        start = datetime.datetime.now()
        try:
            result = subprocess.run(command, capture_output=True, check=True)
            with image_lock:
                latest_image_data = result.stdout
            end = datetime.datetime.now()
            print(
                "Captured image in " + str((end - start).total_seconds()) + " seconds",
                file=sys.stderr,
            )
        except subprocess.CalledProcessError as e:
            print(f"Failed to capture image: {e}", file=sys.stderr)

        time.sleep(1)


@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/output.png")
def serve_image():
    try:
        with image_lock:
            if latest_image_data is None:
                return "No image available yet", 503
            image_data = latest_image_data

        return Response(image_data, mimetype="image/png")
    except Exception as e:
        return str(e)


@app.route("/favicon.ico")
def serve_icon():
    try:
        return send_file("/home/pi/hallen/favicon.ico", mimetype="image/x-icon")
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    thread = threading.Thread(target=capture_image, daemon=True)
    thread.start()
    app.run(host="0.0.0.0", port=8080)
