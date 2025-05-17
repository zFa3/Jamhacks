# install all the dependancies
import cv2
from Graphy import graph
import FaceDetected
import api_call
import requests
import json
from face_recognition import FaceRecognition
from time import perf_counter

with open("web_data_viewer/sent_data.json", "w") as file:
    file.write(r"{}")

# the url for the esp cam
url = "http://10.37.123.227/control"
params = {
    'var': 'framesize',
    'val': '11'
    # SVGA corresponds to 10 ( increases the resolutions )
}

response = requests.get(url, params=params)

# Replace with the ESP32-CAM's IP address and port
esp_cam_ip = "10.37.123.227"
esp_cam_port = "81"
esp_cam_stream_url = f"http://{esp_cam_ip}:{esp_cam_port}/stream"

# Capture the stream from the ESP32-CAM
capture = cv2.VideoCapture(esp_cam_stream_url)

face_tracker = FaceRecognition()

delay_time = 5 # seconds 
time1 = None
cnt = 0

ping_api = False # TODO CHANGE

# for loop
while capture.isOpened():

    success, frame = capture.read()
    frame = cv2.flip(frame, 1)

    if not success: continue

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    if time1 is None:
        time1 = perf_counter()
    elif perf_counter() - time1 >= delay_time:
        if not FaceDetected.is_face_in_frame(frame):
            cnt += 1
        cv2.imwrite("./test_images/api_frame.png", frame)
        if ping_api:
            print(api_call.APICall.make_call("api_frame.png"))
        time1 = perf_counter()
    if cnt == 2:
        break
    print(face_tracker.tilt)

    face_tracker.set_cvframe(rgb_frame)
    final_frame = face_tracker.add_overlay(rgb_frame)
    face_tracker.save_information(rgb_frame)

    cv2.imshow('DriverAssist', final_frame)
    if cv2.waitKey(1) == ord('q'):
        break

# graph(face_tracker.left_pan)
# print(face_tracker.prune_data(face_tracker.left_pan))
to_dump_data = {}
to_dump_data["left_pan"] = face_tracker.prune_data(face_tracker.left_pan)
with open("web_data_viewer/sent_data.json", "w") as file:
    json.dump(to_dump_data, file)

capture.release()
cv2.destroyAllWindows()