# Advanced Keylogger  

This project is an advanced keylogger that captures keystrokes, takes screenshots, logs system activity, and encrypts data. It also integrates a machine learning model for anomaly detection.  

## **Features**  
- **Records Keystrokes**: Logs all keystrokes in real-time.  
- **Screenshots**: Takes periodic screenshots.  
- **System Monitoring**: Logs system info (CPU, memory, active window, etc.).  
- **Encryption**: Encrypts logs for security.  
- **Email Reports**: Sends log files via email.  
- **Machine Learning**: Detects anomalies using an SVM model.  

---

## **Installation & Setup**  

### **1. Clone the Repository**  
- git clone https://github.com/mounesh0711/Keylogger.git
- cd Keylogger

### 2. Install Dependencies
Ensure you have Python installed (recommended Python 3.8+).
#pip install -r requirements.txt

### 3. Train & Prepare the ML Model
Before running the keylogger, train the machine learning model:
#python ml_model.py
This step ensures that the anomaly detection system is ready.

### 4. Run the Keylogger
Start the keylogger application:
#python keylogger.py

### 5. Start Logging
Once the program starts, click the "Start Keylogger" button in the UI to begin monitoring.

### 6. Stop Logging
Click the "Stop Keylogger" button to terminate all logging processes and stop the keylogger.

#####  Security & Legal Warning
## This keylogger is for educational purposes only. Using it without user consent is illegal.
