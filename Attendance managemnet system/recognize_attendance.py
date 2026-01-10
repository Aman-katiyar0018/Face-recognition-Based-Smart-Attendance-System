import cv2
import pickle
import csv
import face_recognition
from datetime import datetime
import numpy as np

ENCODING_PATH = "encodings/encodings.pkl"
CSV_PATH = "attendance.csv"
TOLERANCE = 0.5

with open(ENCODING_PATH, "rb") as f:
    data = pickle.load(f)

known_encodings = data["encodings"]
known_names = data["labels"]

cap = cv2.VideoCapture(0)
marked = set()

print("[INFO] Starting attendance system...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    locations = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, locations)

    for encoding, (top, right, bottom, left) in zip(encodings, locations):
        distances = face_recognition.face_distance(known_encodings, encoding)
        min_dist = np.min(distances)

        if min_dist < TOLERANCE:
            idx = np.argmin(distances)
            name = known_names[idx]

            if name not in marked:
                marked.add(name)
                with open(CSV_PATH, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        name,
                        f"{min_dist:.4f}"
                    ])
                print(f"[INFO] Attendance marked for {name}")

            color = (0, 255, 0)
        else:
            name = "Unknown"
            color = (0, 0, 255)

        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("Attendance", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
