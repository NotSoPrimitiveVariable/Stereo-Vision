from datetime import datetime

import cv2 as cv

webcam = cv.VideoCapture(2, cv.CAP_V4L2)  # use the /dev/videoX index, not an arbitrary OpenCV index

fourcc = cv.VideoWriter.fourcc(*'MJPG')
webcam.set(cv.CAP_PROP_FOURCC, fourcc)  # must come before width/height/fps
webcam.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
webcam.set(cv.CAP_PROP_FRAME_HEIGHT, 800)
webcam.set(cv.CAP_PROP_FPS, 100)

start = datetime.now()
frame_number = 0

print("Actual FOURCC:", int(webcam.get(cv.CAP_PROP_FOURCC)))
print("Actual size:", webcam.get(cv.CAP_PROP_FRAME_WIDTH), webcam.get(cv.CAP_PROP_FRAME_HEIGHT))
print("Actual FPS reported:", webcam.get(cv.CAP_PROP_FPS))

while True:
    ret, frame = webcam.read()
    if not ret:
        break
    else:
        frame_number += 1

    cv.imshow("Webcam", frame)
    now = datetime.now()
    time_difference = now - start

    fps = frame_number / (time_difference.seconds + .00001)
    print("fps: {}", fps)
    if cv.waitKey(1) & 0xFF == ord("q"):
        break

webcam.release()
cv.destroyAllWindows()
