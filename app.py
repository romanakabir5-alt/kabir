import os
from flask import Flask, Response
from livedronemirror import LiveDroneMirror
import cv2

app = Flask(__name__)
mirror = LiveDroneMirror()
frames = mirror.get_processed_frames()

# Use dynamic PORT for Railway
PORT = int(os.environ.get("PORT", 5000))

def generate_detection():
    while True:
        det_frame, _ = next(frames)
        ret, buffer = cv2.imencode('.jpg', det_frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +
               buffer.tobytes() + b'\r\n')

def generate_heatmap():
    while True:
        _, heat_frame = next(frames)
        ret, buffer = cv2.imencode('.jpg', heat_frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +
               buffer.tobytes() + b'\r\n')

@app.route("/")
def detection_stream():
    return Response(generate_detection(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/heatmap")
def heatmap_stream():
    return Response(generate_heatmap(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
