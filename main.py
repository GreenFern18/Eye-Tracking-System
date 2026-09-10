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

import cv2                # OpenCV - camera access and window display.
import mediapipe as mp    # MediaPipe - face and iris landmark detection.

# setup ------------------------------------------------------------------

# MediaPipe's face mesh solution. We create it once and reuse it every frame.
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,                    # Detect at most 1 face per frame.
    refine_landmarks=True,              # Required to get iris landmarks.
    min_detection_confidence=0.5,       # Minimum confidence to accept a face.
    min_tracking_confidence=0.5,        # Minimum confidence to keep tracking.
)

# Open the default webcam (0).
camera = cv2.VideoCapture(0)

# Use a modest 640x480 resolution: fast to process, plenty for tracking.
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# MediaPipe landmark indices for the two iris centers.
LEFT_IRIS = 468                  # Iris center, one eye.
RIGHT_IRIS = 473                 # Iris center, other eye.

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

    # Run face mesh detection on this frame.
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        # There is a face - work with the first (and only) one.
        landmarks = results.multi_face_landmarks[0].landmark
        h, w = frame.shape[:2]          # Frame height/width in pixels.

        # Find both iris centers and mark them on the image.
        iris_points = []                      # (normalized_x, normalized_y, px_x, px_y)
        for idx in (LEFT_IRIS, RIGHT_IRIS):
            lm = landmarks[idx]                # This iris's landmark.
            x = int(lm.x * w)                  # Iris X in pixels.
            y = int(lm.y * h)                  # Iris Y in pixels.
            iris_points.append((lm.x, lm.y, x, y))
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
face_mesh.close()
cv2.destroyAllWindows()
print("Done.")
