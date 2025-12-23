import cv2
import numpy as np
from ultralytics import YOLO

CLASSES = {0: "Person", 1: "Bicycle", 2: "Car", 3: "Motorbike", 5: "Bus", 7: "Truck", 16: "Animal"}

class LiveDroneMirror:
    def __init__(self):
        # Dummy black frame for cloud deployment
        self.frame = np.zeros((480, 640, 3), dtype=np.uint8)
        self.model = YOLO("yolov8n.pt")  # auto-download model
        self.heatmap = np.zeros((480, 640), dtype=np.float32)

    def get_processed_frames(self):
        while True:
            frame = self.frame.copy()
            results = self.model(frame, conf=0.4, classes=list(CLASSES.keys()))
            det_frame = frame.copy()
            heat_frame = frame.copy()
            for r in results:
                for box in r.boxes:
                    cls_id = int(box.cls[0])
                    label = CLASSES.get(cls_id, "Object")
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cx, cy = (x1 + x2)//2, (y1 + y2)//2
                    cv2.rectangle(det_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(det_frame, label, (x1, y1-8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    cv2.circle(self.heatmap, (cx, cy), 25, 1, -1)

            self.heatmap = cv2.GaussianBlur(self.heatmap, (0, 0), 15)
            heat_norm = cv2.normalize(self.heatmap, None, 0, 255, cv2.NORM_MINMAX)
            heat_color = cv2.applyColorMap(heat_norm.astype(np.uint8), cv2.COLORMAP_JET)
            heat_frame = cv2.addWeighted(heat_frame, 0.6, heat_color, 0.4, 0)
            yield det_frame, heat_frame
