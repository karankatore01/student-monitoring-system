import cv2
import numpy as np
import mediapipe as mp
import time

mp_face = mp.solutions.face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=2,
    refine_landmarks=True
)

gaze_start_time = None

def analyze_frame(frame):
    global gaze_start_time

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = mp_face.process(rgb)

    data = {
        "faces": 0,
        "gaze": "Center",
        "emotion": "Focused",
        "proctor_alert": False
    }

    if not result.multi_face_landmarks:
        data["proctor_alert"] = True
        return data

    faces = len(result.multi_face_landmarks)
    data["faces"] = faces

    if faces > 1:
        data["proctor_alert"] = True
        return data

    landmarks = result.multi_face_landmarks[0].landmark


    left_eye = landmarks[33]
    right_eye = landmarks[263]
    nose = landmarks[1]

    if nose.x < left_eye.x:
        gaze = "Left"
    elif nose.x > right_eye.x:
        gaze = "Right"
    else:
        gaze = "Center"

    data["gaze"] = gaze

    now = time.time()
    if gaze != "Center":
        if gaze_start_time is None:
            gaze_start_time = now
        elif now - gaze_start_time >= 4:
            data["proctor_alert"] = True
    else:
        gaze_start_time = None

    brow_left = landmarks[70].y
    brow_right = landmarks[300].y
    mouth_left = landmarks[61].y
    mouth_right = landmarks[291].y

    brow_furrow = abs(brow_left - brow_right) < 0.01
    
    smile = mouth_left < 0.45 and mouth_right < 0.45

    if brow_furrow and not smile:
        data["emotion"] = "Confused"
    elif smile:
        data["emotion"] = "Happy"
    else:
        data["emotion"] = "Focused"

    return data
