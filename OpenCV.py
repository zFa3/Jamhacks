import cv2

capture = cv2.VideoCapture(0)

while capture.isOpened():
    successful, frame = capture.read()
    frame = cv2.flip(frame, 1)

    if not successful: continue # frame not recieved

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    cv2.imshow('DriverAssist', frame)

    if cv2.waitKey(1) == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
