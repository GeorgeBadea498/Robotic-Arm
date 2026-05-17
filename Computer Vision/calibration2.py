import cv2

def mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Clicked Coordinates -> X: {x} , Y: {y}")

cap = cv2.VideoCapture('http://192.168.8.103:4747/video')

if not cap.isOpened():
    print("Camera not opened")
    exit()

cv2.namedWindow('Calibration Window')
cv2.setMouseCallback('Calibration Window', mouse_click)

print("Click on the video window to get coordinates. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break
        
    cv2.imshow('Calibration Window', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()