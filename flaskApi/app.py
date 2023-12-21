# app.py

from flask import Flask, jsonify
import joblib
import pandas as pd
import subprocess

app = Flask(__name__)

@app.route('/', methods=["GET"])
def home():
    return "Welcome to the Flask App!"

@app.route('/predict', methods=["POST"])
def predict():
    uploaded_file = request.files['file']
    df = pd.read_csv(uploaded_file)
    df = data_validation(df)
    
    with open("model.pkl", 'rb') as file:
        classifier = joblib.load(file)

    predictions_test = classifier.predict(df)

    df['Predicted Flower Type'] = predictions_test
    return df.to_json(orient="split")

@app.route('/runcurl', methods=["GET"])
def run_curl_script():
    subprocess.run(["./curlrequirements.sh"])
    
 
    df_x_test = pd.read_csv("X_test.csv")
    return "curlrequirements.sh executed successfully. X_test processed."

def data_validation(df):
    return df

if __name__ == '__main__':
    app.run(debug=True, port=5002)
