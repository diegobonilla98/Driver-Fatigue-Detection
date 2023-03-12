import time
import cv2
import matplotlib.pyplot as plt
import mediapipe as mp
import plotly.express as px
import numpy as np
from scipy.spatial.distance import euclidean


# 200Mb RAM
#

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh


LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]

blink_on = False
blink_time = 0
yawn_on = False
yawn_time = 0

drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture(0)

with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:
    while cap.isOpened():
        frame_time = time.time()
        success, image = cap.read()

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_face_landmarks:
            points = np.array([[r.x, r.y, r.z, i] for i, r in enumerate(results.multi_face_landmarks[0].landmark)])

            mouth_ratio = euclidean(points[13, :3], points[14, :3]) / euclidean(points[78, :3], points[324, :3])
            right_eye_ratio = euclidean(points[159, :3], points[145, :3]) / euclidean(points[33, :3], points[133, :3])
            left_eye_ratio = euclidean(points[386, :3], points[374, :3]) / euclidean(points[362, :3], points[263, :3])

            frame_delay = time.time() - frame_time
            if right_eye_ratio < 0.3 or left_eye_ratio < 0.3:
                if not blink_on:
                    blink_on = True
                    blink_time = time.time()
                else:
                    if time.time() - blink_time - frame_delay > 3.:
                        print("Red alert!")
            else:
                if blink_on:
                    blink_time_ = time.time() - blink_time - frame_delay
                    if blink_time_ > 0.02:
                        # print(f"Blink time: {int(blink_time_ * 1000.)} ms.")
                        blink_on = False
                        if blink_time_ > 0.5:
                            print("Are you tired?")

            if mouth_ratio > 0.2:
                if not yawn_on:
                    yawn_on = True
                    yawn_time = time.time()
            else:
                if yawn_on:
                    yawn_time_ = time.time() - yawn_time - frame_delay
                    if 4.500 > yawn_time_ > 1.500:
                        # print(f"Yawn time: {int(yawn_time_ * 1000.)} ms.")
                        yawn_on = False
                        if yawn_time_ > 2.:
                            print("Are you tired?")

            # for x, y, z, idx in points:
            #     if idx in [159, 145, 33, 133]:
            #         color = (0, 255, 0)
            #     elif idx in [386, 374, 362, 263]:
            #         color = (0, 0, 255)
            #     else:
            #         color = (255, 0, 0)
            #     x = int(x * image.shape[1])
            #     y = int(y * image.shape[0])
            #     cv2.circle(image, (x, y), 2, color, -1, cv2.LINE_AA)

        cv2.imshow('MediaPipe Face Mesh', cv2.flip(image, 1))
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break

cap.release()
