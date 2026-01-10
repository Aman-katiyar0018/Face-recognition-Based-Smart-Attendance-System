import os
import cv2
import pickle
import face_recognition

dataset_dir = "data/enroll"
encoding_file = "encodings/encodings.pkl"

os.makedirs("encodings", exist_ok=True)

known_encodings = []
known_labels = []

print("[INFO] Encoding faces...")

for person in os.listdir(dataset_dir):
    person_path = os.path.join(dataset_dir, person)

    if not os.path.isdir(person_path):
        continue

    for img_name in os.listdir(person_path):
        img_path = os.path.join(person_path, img_name)

        image = cv2.imread(img_path)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        boxes = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, boxes)

        for enc in encodings:
            known_encodings.append(enc)
            known_labels.append(person)

data = {"encodings": known_encodings, "labels": known_labels}

with open(encoding_file, "wb") as f:
    pickle.dump(data, f)

print("[INFO] Encoding complete. Saved to encodings.pkl")
