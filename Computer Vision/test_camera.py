import cv2 as cv
cap=cv.VideoCapture(0)
if not cap.isOpened():
    print("Camera not opened")
    exit()
while True:
    ret, frame = cap.read()
    if not ret:
        print("failed to read frame")
        break
    cv.imshow('camera test', frame)
    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()