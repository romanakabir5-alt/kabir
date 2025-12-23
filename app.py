from flask import Flask, Response, request
from livedronemirror import detection_stream, heatmap_stream
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "NeoInnovations Drone Detection Service"

@app.route("/detection")
def detection():
    stream_url = request.args.get("url")
    if not stream_url:
        return "Please provide a URL parameter: ?url=RTMP_URL", 400
    return Response(
        detection_stream(stream_url),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/heatmap")
def heatmap():
    stream_url = request.args.get("url")
    if not stream_url:
        return "Please provide a URL parameter: ?url=RTMP_URL", 400
    return Response(
        heatmap_stream(stream_url),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
