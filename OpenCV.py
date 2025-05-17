import cv2
import time as tm

capture = cv2.VideoCapture(0)

while capture.isOpened():
    successful, frame = capture.read()
    frame = cv2.flip(frame, 1)

    if not successful: continue # frame not recieved

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)