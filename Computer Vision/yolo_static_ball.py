import os
import sys
import cv2
import importlib
import serial
import time 
import numpy as np

try:
    ultralytics = importlib.import_module('ultralytics')
    YOLO = ultralytics.YOLO
except ImportError:
    print("Missing dependency: install ultralytics with 'pip install ultralytics'")
    sys.exit(1)

model = YOLO('best.pt')

try:
    ser = serial.Serial('COM18', 9600, timeout=1)
    time.sleep(2)
    print("Serial connection established")
except serial.SerialException:
    print("Failed to connect to the robot. Please check the connection and try again.")
    ser = None

def send_command(command):
    print(f"Command: {command}")
    if ser is not None:
        ser.write((command + '\n').encode('utf-8'))

cap = cv2.VideoCapture('http://192.168.8.103:4747/video')
if not cap.isOpened():
    print("Camera not opened")
    exit()

counter = 0
last_x = 0
last_y = 0
robot_busy = False
waiting_for_ball_removal = False 

ZONE_X1 = 677
ZONE_Y1 = 257
ZONE_X2 = 763
ZONE_Y2 = 345

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read frame")
        break
        
    alpha = 1.5 
    beta = 60 
    enhanced_frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
        
    results = model(enhanced_frame, conf=0.25, iou=0.5, verbose=False)
    best_box = None
    best_conf = 0
    
    for box in results[0].boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        center_x = int((x1 + x2) / 2)
        center_y = int((y1 + y2) / 2)
        
        if ZONE_X1 < center_x < ZONE_X2 and ZONE_Y1 < center_y < ZONE_Y2:
            conf = float(box.conf[0])
            if conf > best_conf:
                best_conf = conf
                best_box = box
            
    if best_box is not None:
        if robot_busy == False and waiting_for_ball_removal == False:
            cls_id = int(best_box.cls[0])
            class_name = model.names[cls_id]

            bx1, by1, bx2, by2 = best_box.xyxy[0]
            b_center_x = int((bx1 + bx2) / 2)
            b_center_y = int((by1 + by2) / 2)
            
            diff_x = abs(b_center_x - last_x)
            diff_y = abs(b_center_y - last_y)
            
            if diff_x < 10 and diff_y < 10:
                counter += 1
            else:
                counter = 0 
                last_x = b_center_x
                last_y = b_center_y
                    
            if counter == 5:
                send_command(f"PICK {class_name}") 
                robot_busy = True
                waiting_for_ball_removal = True
                counter = 0
    else:
        if waiting_for_ball_removal == True:
            print("Table is empty. Ready for the next ball...")
            waiting_for_ball_removal = False
        counter = 0
                
    if robot_busy == True and ser is not None:
         try:
              if ser.in_waiting > 0:
                    response = ser.readline().decode('utf-8').strip()
                    if response:
                        print(f"Robot response: {response}")
                        if response == "DONE":
                            robot_busy = False
         except serial.SerialException as e:
              print(f"Serial error: {e}")
              
    annotated_frame = results[0].plot()
    
    cv2.rectangle(annotated_frame, (ZONE_X1, ZONE_Y1), (ZONE_X2, ZONE_Y2), (255, 0, 0), 2)
    cv2.putText(annotated_frame, "Holder Zone", (ZONE_X1, ZONE_Y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
    
    cv2.imshow('YOLO Live Camera (Preprocessed)', annotated_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
if ser is not None:
    ser.close()