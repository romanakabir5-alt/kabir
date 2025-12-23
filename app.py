from flask import Flask, Response, request
from livedronemirror import generate_stream, generate_heatmap
import os

app = Flask(__name__)

@app.route("/detection")
def detection():
    url = request.args.get("stream")
    return Response(generate_stream(url), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/heatmap")
def heatmap():
    url = request.args.get("stream")
    return Response(generate_heatmap(url), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
