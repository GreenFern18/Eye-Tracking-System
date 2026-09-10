"""
main.py - Eye_Tracking_2.0 entry point.

Milestone 1: look at the webcam, find both irises, and
print their normalized coordinates (0.0 - 1.0) to the console.
Mouse movement with the eyes comes in Milestone 2.

Run:
    python main.py
Quit:
    Press "q" in the window (or Ctrl+C in the terminal).
"""

import os                     # To build the model file path reliably.
import time                   # To give MediaPipe a timestamp per frame.
import cv2                    # OpenCV - camera access and window display.
import mediapipe as mp        # MediaPipe - face and iris landmark detection.
from mediapipe.tasks import python as mp_tasks        # MediaPipe task options.
from mediapipe.tasks.python import vision             # MediaPipe face landmarker.

# setup ------------------------------------------------------------------

# Path to the MediaPipe face model file (download - see README or chat).
# We build it from this file's folder so it works no matter where you run from.
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "face_landmarker.task")

# Create the face landmarker once and reuse it for every frame.
landmarker = vision.FaceLandmarker.create_from_options(
    vision.FaceLandmarkerOptions(
        base_options=mp_tasks.BaseOptions(model_asset_path=MODEL_PATH),
        num_faces=1,                          # Detect at most 1 face per frame.
    )
)

# Open the default webcam (0).
camera = cv2.VideoCapture(0)

# Use a modest 640x480 resolution: fast to process, plenty for tracking.
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# MediaPipe landmark indices for the two iris centers (478-point face model).
LEFT_IRIS = 474                  # Iris center, one eye.
RIGHT_IRIS = 468                 # Iris center, other eye.

# Print the numbers only every N frames so the console stays readable.
PRINT_EVERY = 10

# main loop ---------------------------------------------------------------

print("Eye tracking active - press 'q' to quit.")
frame_count = 0                  # Counts frames so we can throttle printing.

while True:
    # Read one frame from the camera.
    ok, frame = camera.read()
    if not ok:
        # No frame arrived (camera unplugged or failed) - stop gracefully.
        print("Camera error: no frame received. Exiting.")
        break

    # Mirror the image so it behaves like a mirror (feels natural).
    frame = cv2.flip(frame, 1)

    # MediaPipe expects RGB, but OpenCV gives BGR - convert first.
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Wrap the image for MediaPipe, with a timestamp (ms) that always grows.
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    timestamp_ms = int(time.time() * 1000)

    # Run face detection on this frame.
    results = landmarker.detect_for_video(mp_image, timestamp_ms)

    if results.face_landmarks:
        # There is a face - work with the first (and only) one.
        landmarks = results.face_landmarks[0]
        h, w = frame.shape[:2]          # Frame height/width in pixels.

        # Find both iris centers and mark them on the image.
        iris_points = []                      # (mirrored_x, y, px_x, px_y)
        for idx in (LEFT_IRIS, RIGHT_IRIS):
            lm = landmarks[idx]               # This iris's landmark.
            mx = 1.0 - lm.x                   # Flip X so it matches the mirror view.
            x = int(mx * w)                   # Iris X in pixels.
            y = int(lm.y * h)                 # Iris Y in pixels.
            iris_points.append((mx, lm.y, x, y))
            cv2.circle(frame, (x, y), 4, (0, 255, 0), -1)  # Draw a small green dot on iris.

        # Show live coordinates every few frames (normalized + pixels).
        frame_count += 1
        if frame_count % PRINT_EVERY == 0:
            for i, (nx, ny, px, py) in enumerate(iris_points):
                print(f"eye{i + 1}: x={nx:.3f} y={ny:.3f}  (px {px}, {py})")
    else:
        # No face in this frame - nothing to track right now.
        print("no face detected")

    # Display the frame with the iris dots on it.
    cv2.imshow("Eye Tracking 2.0", frame)

    # Wait ~1 ms and check for the quit key ("q").
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break                            # User pressed 'q' - end the loop.

# cleanup -----------------------------------------------------------------

# Free the camera, the MediaPipe model, and close all windows.
camera.release()
landmarker.close()
cv2.destroyAllWindows()
print("Done.")
