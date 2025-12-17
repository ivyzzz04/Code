# CST2590 – Smart Library System

The Smart Library System is an IoT-integrated project designed to automate and enhance core library functions through sensor-driven detection, actuator response, and real-time data transmission. The system uses a range of components—including PIR sensors, ultrasonic and TCRT5000 detectors, MFRC522 RFID readers, servo motors, and LCD displays—controlled by **three Arduino Uno R3 boards** and unified through an **ESP32 DevKit V1** for cloud communication.

Each Arduino manages a dedicated zone:  
- **Gate System** – Monitors student entry/exit, controls gate movement, tracks occupancy, and displays capacity updates.  
- **Smart Shelf** – Detects book placement/removal, reads RFID tags, validates correct shelving, and updates book status in real-time.  
- **Checkout System** – Handles the book checkout process by mapping RFID UIDs to inventory data and updating borrow/return states.

The ESP32 acts as the central communication bridge, coordinating data from all subsystems and transmitting it to the IoT platform. After testing multiple platforms—including Blynk and ThingSpeak—the system ultimately uses **Google Sheets via webhook integration**, chosen for its reliability, clarity, and ease of data logging.

This repository contains all code and documentation for the complete Smart Library prototype, covering the gate system, smart shelf, checkout station, and IoT integration workflow.


Instructions:
- Download and unzip folder
- Take "Streamlit" folder outside and run "fashboard.py" on terminal:
    streamlit run dashboard.py
- "Arduino" folders are for Arduino IDE codes. 
- "Pyserial_comms" folder is for Gateway's Python code. Make sure to run gatesystem.ino first and then gatesystem.py
