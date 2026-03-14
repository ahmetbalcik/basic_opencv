import cv2
import numpy as np

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("I can't open camera")
    exit()
while True:
    ret, frame = camera.read()
    if not ret:
        print("I can't read the image of camera")
        break
    cv2.imshow("Live Camera", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break


camera.release()
cv2.destroyAllWindows()