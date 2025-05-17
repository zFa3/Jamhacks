import cv2
import time as tm

capture = cv2.VideoCapture(0)

while capture.isOpened():
    successful, frame = capture.read()
    frame = cv2.flip(frame, 1)

    