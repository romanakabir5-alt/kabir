from flask import Flask, Response, request, render_template
from livedronemirror import detection_stream, heatmap_stream
import os

app = Flask(__name__)

# Home page: accepts RTMP URL
@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

# Normal detection stream
@app.route("/detection")
def detection():
    rtmp_url = request.args.get("url")
    if not rtmp_url:
        return "Please provide RTMP URL as ?url=RTMP_URL", 400
    return Response(
        detection_stream(rtmp_url),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

# Heatmap stream
@app.route("/heatmap")
def heatmap():
    rtmp_url = request.args.get("url")
    if not rtmp_url:
        return "Please provide RTMP URL as ?url=RTMP_URL", 400
    return Response(
        heatmap_stream(rtmp_url),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
