"""
main.py - Eye_Tracking_2.0 entry point.

Milestone 1: look at the webcame, find both irises, and
print their normalized coordinates (0.0 - 1.0) to the console.
Mouse movement with the eyes comes in Milestone 2.

Run:
    python main.py
Quit:
    Press "q" in the window (or Ctrl+C in the terminal).
"""

import cv2                # OpenCV — camera access and window display.
import mediapipe as mp    # MediaPipe — face and iris landmark detection.

# setup ------------------------------------------------------------------

# MediaPipe's face mesh solution. We create it once and reuse it every frame.
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,                    # Detect at most 1 face per frame.
    refine_landmarks=True,              # Required to get iris landmarks.
    min_detection_confidence=0.5,       # Minimum confidence to accept a face.
    min_tracking_confidence=0.5,        # Minimum confidence to keep tracking.
)