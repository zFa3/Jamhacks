import cv2
from face_recognition import FaceRecognition
from time import perf_counter

capture = cv2.VideoCapture(0)

delay_time = 2

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
        cv2.imwrite("./test_images/api_frame.png", frame)
        print("HELLO")
        time1 = perf_counter()

    final_frame = face_tracker.add_overlay(rgb_frame)

    cv2.imshow('DriverAssist', final_frame)

    if cv2.waitKey(1) == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
