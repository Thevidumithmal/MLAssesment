#!/bin/bash

# This script is used to test the Flask application using curl.

# Set the URL for your Flask app
FLASK_APP_URL="http://localhost:5002"

# Endpoint for the home route
HOME_ENDPOINT="${FLASK_APP_URL}/"

# Endpoint for the predict route
PREDICT_ENDPOINT="${FLASK_APP_URL}/predict"

# Path to the CSV file for testing predictions
CSV_FILE_PATH="c:\Users\User\Desktop\model-deployment-with-docker-live-demo\Model deployment with Docker Live Demo\data\X_train.csv"

# Test the home route
echo "Testing the home route..."
curl -X GET "${HOME_ENDPOINT}"

# Test the predict route with a sample CSV file
echo "Testing the predict route with a sample CSV file..."
curl -X POST -F "file=@${CSV_FILE_PATH}" "${PREDICT_ENDPOINT}"

# Add more test cases or endpoints as needed

# Note: Adjust the paths and URLs based on your project structure and deployment configuration.
