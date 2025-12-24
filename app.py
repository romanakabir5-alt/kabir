from flask import Flask, Response, render_template
from livedronemirror import generate_streams
import os

app = Flask(__name__)

# This route serves the HTML page
@app.route("/")
def index():
    return render_template("index.html")

# Normal detection stream
@app.route("/detection")
def detection():
    det_stream, _ = generate_streams()
    return Response(
        det_stream,
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

# Heatmap stream
@app.route("/heatmap")
def heatmap():
    _, heat_stream = generate_streams()
    return Response(
        heat_stream,
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

# Health check
@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
