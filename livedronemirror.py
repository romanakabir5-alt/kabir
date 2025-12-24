import cv2
import numpy as np

# IVS playback URL
IVS_URL = "https://ccf34ee45c75.ap-south-1.playback.live-video.net/api/video/v1/ap-south-1.770493140660.channel.DGNRwz1CnPIK.m3u8"

def generate_streams():
    cap = cv2.VideoCapture(IVS_URL)

    def generate_normal():
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    def generate_heatmap():
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            # Simple heatmap effect (red overlay)
            heat = cv2.applyColorMap(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cv2.COLORMAP_JET)
            _, buffer = cv2.imencode('.jpg', heat)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    return generate_normal(), generate_heatmap()
