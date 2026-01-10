import os
import argparse
import cv2

parser = argparse.ArgumentParser()
parser.add_argument("--name", required=True, help="Person name")
parser.add_argument("--out", default="data/enroll", help="Output folder")
parser.add_argument("--max", type=int, default=20, help="Max images")
args = parser.parse_args()

person_dir = os.path.join(args.out, args.name)
os.makedirs(person_dir, exist_ok=True)

cap = cv2.VideoCapture(0)
count = 0

print("Press SPACE to capture image, Q to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Enroll Face", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    if key == 32 and count < args.max:  # SPACE key
        img_path = os.path.join(person_dir, f"{args.name}_{count}.jpg")
        cv2.imwrite(img_path, frame)
        print(f"[INFO] Saved {img_path}")
        count += 1

    if count >= args.max:
        break

cap.release()
cv2.destroyAllWindows()
