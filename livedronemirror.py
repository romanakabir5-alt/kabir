import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # YOLOv8 Nano model

def detection_stream(rtmp_url):
    cap = cv2.VideoCapture(rtmp_url)
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        results = model(frame)
        # Draw boxes
        for r in results:
            boxes = r.boxes.xyxy
            for box in boxes:
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
        _, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

def heatmap_stream(rtmp_url):
    cap = cv2.VideoCapture(rtmp_url)
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        heatmap = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
        _, jpeg = cv2.imencode('.jpg', heatmap)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
