import cv2
import os

# Constants
SAMPLES_DIR = os.path.join("backend", "auth", "samples")
CASCADE_PATH = os.path.join("backend", "auth", "haarcascade_frontalface_default.xml")
NUM_SAMPLES = 100
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Initialize camera
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(3, FRAME_WIDTH)
cam.set(4, FRAME_HEIGHT)

# Load Haar cascade
if not os.path.exists(CASCADE_PATH):
    raise FileNotFoundError(f"Haar cascade not found at: {CASCADE_PATH}")
detector = cv2.CascadeClassifier(CASCADE_PATH)

# Get user ID
face_id = input("Enter a numeric user ID here: ").strip()
if not face_id.isdigit():
    raise ValueError("User ID must be a number.")

print("[INFO] Taking samples. Look at the camera...")

# Sample count
count = 0

while True:
    ret, img = cam.read()
    if not ret:
        print("[ERROR] Failed to grab frame from camera.")
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        count += 1

        # Draw rectangle
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Save cropped face
        filename = f"face.{face_id}.{count}.jpg"
        path = os.path.join(SAMPLES_DIR, filename)
        cv2.imwrite(path, gray[y:y + h, x:x + w])

        # Show live image
        cv2.imshow('Face Capture', img)

    # Break on ESC or when enough samples are collected
    k = cv2.waitKey(100) & 0xFF
    if k == 27 or k == ord('q'):  # ESC or 'q'
        print("[INFO] Capture stopped by user.")
        break
    elif count >= NUM_SAMPLES:
        print("[INFO] Sample collection complete.")
        break

# Clean up
cam.release()
cv2.destroyAllWindows()
print("[INFO] Program terminated successfully.")
