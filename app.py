from flask import Flask, Response
from livedronemirror import detection_stream, heatmap_stream
import os

app = Flask(__name__)

@app.route("/")
def detection():
    return Response(
        detection_stream(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/heatmap")
def heatmap():
    return Response(
        heatmap_stream(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
