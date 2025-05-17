import cv2
from face_recognition import FaceRecognition

capture = cv2.VideoCapture(0)

face_tracker = FaceRecognition()

# for loop
while capture.isOpened():

    success, frame = capture.read()
    frame = cv2.flip(frame, 1)

    if not success: continue

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    final_frame = face_tracker.add_overlay(rgb_frame)

    cv2.imshow('DriverAssist', final_frame)

    if cv2.waitKey(1) == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
