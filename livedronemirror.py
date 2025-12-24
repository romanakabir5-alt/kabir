import cv2
import time
import numpy as np
from ultralytics import YOLO
from threading import Lock

# ================= CONFIG =================
IVS_PLAYBACK_URL = "https://ccf34ee45c75.ap-south-1.playback.live-video.net/api/video/v1/ap-south-1.770493140660.channel.DGNRwz1CnPIK.m3u8"

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(IVS_PLAYBACK_URL)

lock = Lock()
last_frame = None
last_heatmap = None

# ================= FRAME LOOP =================
def update_frames():
    global last_frame, last_heatmap

    while True:
        ret, frame = cap.read()
        if not ret:
            time.sleep(0.1)
            continue

        results = model(frame, conf=0.4, verbose=False)

        annotated = frame.copy()
        heatmap = np.zeros(frame.shape[:2], dtype=np.float32)

        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls = int(box.cls[0])

                # Allowed classes
                if cls in [0, 1, 2, 3, 5, 7]:
                    cv2.rectangle(annotated, (x1, y1), (x2, y2), (0,255,0), 2)
                    heatmap[y1:y2, x1:x2] += 1

        heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
        heatmap = cv2.applyColorMap(heatmap.astype(np.uint8), cv2.COLORMAP_JET)

        with lock:
            last_frame = annotated
            last_heatmap = heatmap

# ================= STREAM GENERATORS =================
def mjpeg_stream(getter):
    while True:
        with lock:
            frame = getter()
        if frame is None:
            time.sleep(0.05)
            continue

        _, jpeg = cv2.imencode(".jpg", frame)
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" +
            jpeg.tobytes() +
            b"\r\n"
        )

def detection_stream():
    return mjpeg_stream(lambda: last_frame)

def heatmap_stream():
    return mjpeg_stream(lambda: last_heatmap)

# ================= START BACKGROUND THREAD =================
import threading
threading.Thread(target=update_frames, daemon=True).start()
