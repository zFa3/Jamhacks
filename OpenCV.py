import cv2
from Graphy import graph
import BodyDetection
from face_recognition import FaceRecognition
from time import perf_counter

capture = cv2.VideoCapture(0)

delay_time = 2 # seconds

face_tracker = FaceRecognition()
time1 = None

# for loop
while capture.isOpened():

    success, frame = capture.read()
    frame = cv2.flip(frame, 1)

    if not success: continue

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    if time1 is None:
        time1 = perf_counter()
    elif perf_counter() - time1 >= delay_time:
        if not BodyDetection.is_person_in_frame(frame):
            break
        cv2.imwrite("./test_images/api_frame.png", frame)
        print("HELLO")
        time1 = perf_counter()
    print(face_tracker.tilt)

    face_tracker.set_cvframe(rgb_frame)
    final_frame = face_tracker.add_overlay(rgb_frame)
    face_tracker.save_information(rgb_frame)

    cv2.imshow('DriverAssist', final_frame)
    cv2.waitKey(1)

graph(face_tracker.right_pan)

capture.release()
cv2.destroyAllWindows()