import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("I can't open camera")
    exit()

print("Camera opened. If you want exit, you press q")
while True:
    ret, frame = camera.read()
    if not ret:
        print("I can't read the image of camera")
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x,y,w,h) in faces:
        cv2.rectangle(gray, (x,y), (x+w, y+h), (0,0,255), 4)
        cv2.putText(gray, "Person",  (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
    
    cv2.imshow("Faces", gray)
    if cv2.waitKey(1) & 0xFF == 113:
        break


camera.release()
cv2.destroyAllWindows()