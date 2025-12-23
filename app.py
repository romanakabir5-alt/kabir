from flask import Flask, Response, request, jsonify
from livedronemirror import DetectionStream
import os

app = Flask(__name__)
stream_processor = DetectionStream()

@app.route("/set_stream", methods=["POST"])
def set_stream():
    """
    Set the RTMP or video stream URL dynamically.
    """
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    stream_processor.set_stream(url)
    return jsonify({"status": "Stream URL updated"}), 200

@app.route("/detection")
def detection():
    """
    Returns detection video feed
    """
    return Response(
        stream_processor.detection_stream(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/heatmap")
def heatmap():
    """
    Returns heatmap video feed
    """
    return Response(
        stream_processor.heatmap_stream(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
