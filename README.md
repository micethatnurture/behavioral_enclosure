# 🐭 Mouse Maternal Behavior Video Recording (Raspberry Pi) 🎥  

This repository contains a **Python-based video recording system** designed to run on a **Raspberry Pi** for **continuous 24/7 monitoring of mouse maternal behavior**. The system captures and saves high-quality video while embedding timestamps.

## 🔥 Features  
✅ **Continuous Video Capture** – Records 24/7 and saves video in `.mkv` format with timestamps.  
✅ **Automatic File Rotation** – Creates a new video file **every 3 hours** to manage storage efficiently.  
✅ **Timestamp Logging** – Saves frame-by-frame timestamps in a `.txt` file for behavioral tracking.  
✅ **Optimized Performance** – Uses **multithreading** to maintain real-time capture without frame drops.  
✅ **Live Streaming** – Streams video frames over **ZeroMQ (ZMQ)** for remote monitoring.  
✅ **Resilient Operation** – Designed for **long-term stability** with automatic error handling.  

---

## 🛠 Installation & Setup  

### **📌 Requirements**
- Raspberry Pi (tested on **Raspberry Pi 4**)
- **Python 3.6+**
- **Required Libraries**:  
  Install dependencies using:
  ```bash
  pip install opencv-python numpy pyzmq
