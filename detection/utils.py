import cv2
import face_recognition
import datetime
import os
import time
from .email_utils import send_email_alert
from faces.models import Face
from django.conf import settings
from detection.models import Detection
from django.core.files import File

FACE_TOLERANCE = 0.6
PROCESS_EVERY_N_FRAMES = 3
EMAIL_COOLDOWN = 60


def load_known_faces(user):
    known_encodings = []
    known_names = []
    for face in Face.objects.filter(user=user, is_active=True):
        image_path = face.image.path
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_encodings.append(encodings[0])
            known_names.append(face.name)
    return known_encodings, known_names


def save_detection_frame(frame):
    os.makedirs(settings.MEDIA_ROOT / 'detections', exist_ok=True)
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'detections/detected_{timestamp}.jpg'
    filepath = settings.MEDIA_ROOT / filename
    cv2.imwrite(str(filepath), frame)
    return filename


def process_camera(camera, user):
    known_encodings, known_names = load_known_faces(user)
    if not known_encodings:
        print('No known faces for user.')
        return
    cap = cv2.VideoCapture(f'http://{camera.ip_address}:{camera.port}/video')
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    if not cap.isOpened():
        print(f'Could not connect to camera {camera.name}')
        return
    last_email_time = None
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            time.sleep(1)
            continue
        frame_count += 1
        if frame_count % PROCESS_EVERY_N_FRAMES != 0:
            continue
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
        if not face_locations:
            continue
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        for i, face_encoding in enumerate(face_encodings):
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=FACE_TOLERANCE)
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            name = "Unknown"
            confidence = 0.0
            if True in matches:
                best_match_index = face_distances.argmin()
                name = known_names[best_match_index]
                confidence = 1 - face_distances[best_match_index]
                now = datetime.datetime.now()
                if not last_email_time or (now - last_email_time).total_seconds() > EMAIL_COOLDOWN:
                    image_rel_path = save_detection_frame(frame)
                    send_email_alert(
                        image_path=settings.MEDIA_ROOT / image_rel_path,
                        detection_name=name,
                        current_time=now,
                        user=user
                    )
                    last_email_time = now
                # Save detection in DB
                detection = Detection.objects.create(
                    camera=camera,
                    detected_face=Face.objects.filter(user=user, name=name).first(),
                    status='completed',
                    confidence_score=confidence,
                    image=image_rel_path,
                    notification_sent=True
                )
            else:
                # Save unknown detection if needed
                pass
    cap.release()