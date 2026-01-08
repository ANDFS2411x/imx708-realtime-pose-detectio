# IMX708 Real-Time Pose Detection with MediaPipe

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.12-green?style=for-the-badge&logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Latest-orange?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi%204-red?style=for-the-badge&logo=raspberrypi)

**Real-time human pose estimation using Arducam IMX708 camera on Raspberry Pi 4**

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Hardware Requirements](#-hardware-requirements)
- [Software Requirements](#-software-requirements)
- [Installation Guide](#-installation-guide)
- [Usage](#-usage)
- [Troubleshooting](#-troubleshooting)
- [Technical Details](#-technical-details)
- [Credits](#-credits)

---

## 🎯 Overview

This project implements real-time human pose detection using Google's MediaPipe framework on a Raspberry Pi 4 with an Arducam IMX708 camera. The system processes video frames locally and detects 33 body landmarks in real-time, making it suitable for applications in fitness tracking, gesture recognition, and human-computer interaction.

**Key Features:**
- ✅ Real-time pose landmark detection (33 points)
- ✅ Optimized for Raspberry Pi 4 hardware
- ✅ Native support for Arducam IMX708 camera
- ✅ Low-latency processing using V4L2
- ✅ Fully offline processing (no cloud required)

---

## 🛠 Hardware Requirements

| Component | Specification |
|-----------|--------------|
| **Board** | Raspberry Pi 4 (4GB RAM recommended) |
| **Camera** | Arducam IMX708 (connected to CSI port) |
| **OS** | Raspberry Pi OS (64-bit) - Debian 12 (Bookworm) |
| **Storage** | 16GB+ microSD card |

---

## 💻 Software Requirements

- Python 3.11+
- OpenCV 4.12+
- MediaPipe (latest version)
- Picamera2
- libcamera
- V4L2 drivers

---

## 📦 Installation Guide

### Step 1: Verify System Information

Check your Raspberry Pi model and OS version:

```bash
cat /proc/device-tree/model
cat /etc/os-release
lsb_release -a
uname -m
```

**Expected output:**
- Model: Raspberry Pi 4 Model B
- Debian version: 12 (bookworm)
- Architecture: aarch64

---

### Step 2: Update System Packages

```bash
sudo apt update
sudo apt upgrade -y
```

---

### Step 3: Install System Dependencies

Install Python development tools:

```bash
sudo apt install -y python3-pip python3-virtualenv
python3 --version  # Verify Python installation
```

Install camera libraries:

```bash
sudo apt install -y rpicam-apps python3-picamera2 python3-opencv
```

---

### Step 4: Verify Camera Connection

Check if the IMX708 camera is detected:

```bash
rpicam-hello --list-cameras
```

**Expected output:**
```
Available cameras
-----------------
0 : imx708 [4608x2592 10-bit RGGB] (/base/soc/i2c0mux/i2c@1/imx708@1a)
    Modes: 'SRGGB10_CSI2P' : 1536x864 [120.13 fps]
                             2304x1296 [56.03 fps]
                             4608x2592 [14.35 fps]
```

Test camera preview:

```bash
rpicam-still -t 0
```

Press `Ctrl+C` to exit.

---

### Step 5: Create Project Directory

```bash
cd ~/Desktop
mkdir projects
cd projects
```

---

### Step 6: Set Up Python Virtual Environment

Create a virtual environment with system packages:

```bash
python3 -m venv --system-site-packages venv
source venv/bin/activate
```

Your terminal prompt should now show `(venv)`.

---

### Step 7: Install MediaPipe

```bash
pip3 install mediapipe
```

---

### Step 8: Verify Installations

Run verification tests:

```bash
# Test Picamera2
python3 -c "from picamera2 import Picamera2; print('Picamera2 ✅')"

# Test OpenCV
python3 -c "import cv2; print('OpenCV version:', cv2.__version__)"

# Test MediaPipe
python3 -c "import mediapipe as mp; print('MediaPipe version:', mp.__version__)"
```

All three commands should execute without errors.

---

### Step 9: Create the Pose Detection Script

Create a new file called `pose_detection.py`:

```bash
nano pose_detection.py
```

Paste the following code:

```python
import cv2
import mediapipe as mp
import sys

# 1. Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

# 2. Open camera using V4L2 (compatible with libcamera)
print("Starting IMX708 camera...")
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

if not cap.isOpened():
    print("ERROR: Unable to access camera.")
    sys.exit()

# 3. Set standard resolution to avoid reshape errors
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Camera configured. Starting processing...")
print("Press ESC to exit.")

# 4. Main processing loop
while cap.isOpened():
    success, frame = cap.read()
   
    # Skip if frame is invalid
    if not success or frame is None:
        continue

    # Convert BGR to RGB for MediaPipe
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(img_rgb)

    # Draw pose landmarks on frame
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

    # Display output window
    cv2.imshow('MediaPipe Pose - IMX708', frame)
   
    # Exit on ESC key
    if cv2.waitKey(1) & 0xFF == 27:
        break

# 5. Cleanup
cap.release()
cv2.destroyAllWindows()
```

Save and exit (Ctrl+X, then Y, then Enter).

---

## 🚀 Usage

### Running the Program

1. Activate the virtual environment (if not already active):

```bash
cd ~/Desktop/projects
source venv/bin/activate
```

2. Run the pose detection script:

```bash
python3 pose_detection.py
```

3. A window will appear showing the camera feed with pose landmarks overlaid on detected people.

4. **To exit:** Press the `ESC` key.

---

## 🔧 Troubleshooting

### Issue: Camera not detected

**Solution:**
```bash
# Kill any process using the camera
sudo pkill -9 rpicam && sudo pkill -9 libcamera

# Verify camera connection
rpicam-hello --list-cameras
```

---

### Issue: Qt platform plugin error

**Symptoms:**
```
qt.qpa.plugin: Could not load the Qt platform plugin "xcb"
```

**Solution:**
Remove OpenCV from virtual environment and use system version:

```bash
# Activate virtual environment
source venv/bin/activate

# Remove venv OpenCV
rm -rf venv/lib/python3.11/site-packages/cv2
rm -rf venv/lib/python3.11/site-packages/cv2-*.dist-info

# Install system OpenCV
sudo apt install -y python3-opencv
```

---

### Issue: Reshape error

**Symptoms:**
```
cv2.error: ... Bad new number of rows in function 'reshape'
```

**Solution:**
This is already handled in the final code by forcing a standard resolution (640x480) before processing.

---

### Issue: Low FPS / Performance

**Solutions:**
- Reduce `model_complexity` to 0 (already set in the code)
- Lower resolution if needed
- Close other applications to free resources
- Ensure adequate cooling for Raspberry Pi

---

## 📊 Technical Details

### Camera Configuration
- **Resolution:** 640x480 (configurable)
- **API:** V4L2 (Video4Linux2)
- **Format:** BGR888
- **Frame Rate:** ~10-15 FPS on Raspberry Pi 4

### MediaPipe Pose Model
- **Landmarks detected:** 33 body keypoints
- **Model complexity:** 0 (lightweight, optimized for embedded devices)
- **Detection confidence:** 0.5
- **Tracking confidence:** 0.5

### Performance Optimization
- Uses `model_complexity=0` for faster inference
- Static image mode disabled for video processing
- Minimal frame skipping logic for stability

---

## 👨‍💻 Credits

**Made by Andrés Fábregas**

Electronic Engineer · Software Developer

[![Portfolio](https://img.shields.io/badge/Portfolio-byandresfabregas.vercel.app-blue?style=for-the-badge)](https://byandresfabregas.vercel.app/)

---

## 📄 License

This project is open source and available for educational and research purposes.

---

## 🙏 Acknowledgments

- Google MediaPipe team for the pose estimation framework
- Arducam for IMX708 camera support
- Raspberry Pi Foundation
- OpenCV community

---

<div align="center">

**⭐ If you found this project helpful, please consider giving it a star!**

</div>
