import cv2, time, os
import datetime
import face_recognition
from threading import Thread
from django.conf import settings
from .utils import encode_known_faces
from .email_utils import send_alert

def process_camera(camera, user):
    encodings = encode_known_faces(user)
    cap = cv2.VideoCapture(camera.ip_address)
    last_sent = None

    while True:
        ret, frame = cap.read()
        if not ret:
            time.sleep(2)
            continue

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        locations = face_recognition.face_locations(rgb)
        encs = face_recognition.face_encodings(rgb, locations)

        for face_encoding, face_location in zip(encs, locations):
            for name, known_enc in encodings.items():
                matches = face_recognition.compare_faces([known_enc], face_encoding, tolerance=0.6)
                if True in matches:
                    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    path = f"media/detections/{user.username}_{ts}.jpg"
                    os.makedirs("media/detections", exist_ok=True)
                    cv2.imwrite(path, frame)
                    if not last_sent or (datetime.datetime.now() - last_sent).total_seconds() > 60:
                        send_alert(f"🚨 Alert: {name} detected!",
                                   f"{name} was detected on camera {camera.name}",
                                   user.email,
                                   path)
                        last_sent = datetime.datetime.now()