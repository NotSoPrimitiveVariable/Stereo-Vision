import cv2 as cv

webcam = cv.VideoCapture(0)

while True:
    ret, frame = webcam.read()

    if not ret:
        break

    cv.imshow(frame)

    if cv.waitKey(1) & 0xFF == ord("q"):
        break
webcam.release()
cv.destroyAllWindows()
