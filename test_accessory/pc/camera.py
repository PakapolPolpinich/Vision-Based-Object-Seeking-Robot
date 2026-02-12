import cv2
import os
from datetime import datetime

# Path to data/vision
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")) #file a path to the root directory
save_dir = os.path.join(ROOT, "data", "vision")
os.makedirs(save_dir, exist_ok=True)

# open camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

print("Press 'c' to capture image")
print("Press 'q' to quit")
count = 1
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    cv2.imshow("Webcam", frame)

    key = cv2.waitKey(1) & 0xFF
    
    # push c -> capture
    if key == ord('c'):
       # timestamp = datetime.now().strftime("%Y%m%d_%H%M%s")
        filename = f"ver2_bicycle_{count}.jpg"
        filepath = os.path.join(save_dir, filename)
        cv2.imwrite(filepath, frame) #save image
        print(f"Saved: {filepath}")
        count += 1
    # push q เ-> quit
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
