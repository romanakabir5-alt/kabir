import cv2
import numpy as np
from ultralytics import YOLO
import threading
import time

class DetectionStream:
    def __init__(self):
        self.stream_url = None
        self.lock = threading.Lock()
        self.cap = None
        self.model = YOLO("yolov8n.pt")  # small YOLOv8 model
        self.current_frame = None

    def set_stream(self, url):
        """
        Set the stream URL and restart capture
        """
        with self.lock:
            self.stream_url = url
            if self.cap:
                self.cap.release()
            self.cap = cv2.VideoCapture(self.stream_url)
            threading.Thread(target=self.update_frames, daemon=True).start()

    def update_frames(self):
        while True:
            if not self.cap or not self.cap.isOpened():
                time.sleep(1)
                continue
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.1)
                continue
            self.current_frame = frame

    def detection_stream(self):
        while True:
            if self.current_frame is None:
                time.sleep(0.1)
                continue
            frame = self.current_frame.copy()
            results = self.model(frame)[0]
            for box in results.boxes.xyxy:
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            ret, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

    def heatmap_stream(self):
        while True:
            if self.current_frame is None:
                time.sleep(0.1)
                continue
            frame = self.current_frame.copy()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            heatmap = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
            ret, jpeg = cv2.imencode('.jpg', heatmap)
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
