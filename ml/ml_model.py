import pandas as pd
from sklearn.svm import OneClassSVM
import joblib

DATASET_FILE = r"C:\Users\ASUS\Downloads\Mini project 1---S5\new keylog\ml\anomaly.xlsx" 
MODEL_FILE = r"anomaly_detector_oneclass.pkl" 

# Load dataset
data = pd.read_excel(DATASET_FILE)

data['word'] = data['word'].astype(str) 
word_lengths = data['word'].apply(len).values.reshape(-1, 1)  
model = OneClassSVM(kernel="rbf", nu=0.1, gamma="auto")
model.fit(word_lengths)

joblib.dump(model, MODEL_FILE)
print(f"Model trained on anomalous words and saved to {MODEL_FILE}.")