## Computer Vision Module

This directory contains the core intelligence of the robotic sorting system, leveraging Deep Learning and Real-Time Object Detection to classify and locate target objects.

### Key Components
* *yolo_static_ball.py*: The main execution script handling real-time camera feed preprocessing (contrast & brightness enhancement via OpenCV), custom YOLO inference, Region of Interest (ROI) safety masking, and hardware-software synchronization via PySerial.
* *best.pt*: The custom-trained Convolutional Neural Network (CNN) weights file optimized for detecting and classifying the specific colored targets.
* *train.py*: The deep learning training pipeline script demonstrating dataset optimization, model training, and data augmentation configurations.
* *calibration2.py*: A dedicated computer vision utility tool using mouse callbacks to dynamically calibrate and define the exact pixel coordinate boundaries of the pickup holder.

### Technical Features Included
1. *Adaptive Preprocessing*: Dynamic contrast ($\alpha$) and brightness ($\beta$) scaling to eliminate environmental illumination and shadow issues in the pickup zone.
2. *ROI Safety Masking*: Software-level spatial filtering that ignores any background noise or false positives outside the operational workspace.
3. *Closed-Loop Hardware Synchronization*: A robust state-machine synchronization layout that manages serial communications and awaits mechanical hardware feedback (DONE signal) before initiating the next detection cycle.
4. test_camera.py: A simple sanity-check script to verify the IP webcam connection and hardware setup before running the heavy AI models.
