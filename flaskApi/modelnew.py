# -*- coding: utf-8 -*-
"""modelNew.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YMPN1g48HuGz7TcR3oO6j0AymjO_QC2Z
"""

!unzip '10.zip'

import os
import cv2
import numpy as np
from tensorflow.keras import layers, models

# Define your neural network model
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(4))  # Assuming you have 4 output coordinates
# Add more layers as needed...

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

def load_data(data_dir, num_coordinates=4):
    images = []
    labels = []

    for image_file in os.listdir(os.path.join(data_dir, 'images')):
        img_path = os.path.join(data_dir, 'images', image_file)
        img = cv2.imread(img_path)
        img = cv2.resize(img, (224, 224))
        images.append(img)

        label_path = os.path.join(data_dir, 'labels', image_file.replace('.jpg', '.txt'))
        with open(label_path, 'r') as file:
            label_str = file.read().strip().split()
            label = list(map(float, label_str[1:]))[:num_coordinates]
            labels.append(label + [0.0] * (num_coordinates - len(label)))

    return np.array(images), np.array(labels)

# Load training data
train_images, train_labels = load_data('10/train')
train_labels = np.array(train_labels)

# Train the model
model.fit(train_images, train_labels, epochs=10, batch_size=32)

def load_test_data(data_dir, num_coordinates=4):
    images = []
    labels = []

    for image_file in os.listdir(os.path.join(data_dir, 'images')):
        img_path = os.path.join(data_dir, 'images', image_file)
        img = cv2.imread(img_path)
        img = cv2.resize(img, (224, 224))
        images.append(img)

        label_path = os.path.join(data_dir, 'labels', image_file.replace('.jpg', '.txt'))
        with open(label_path, 'r') as file:
            label_str = file.read().strip().split()
            label = list(map(float, label_str[1:]))[:num_coordinates]
            labels.append(label + [0.0] * (num_coordinates - len(label)))

    return np.array(images), np.array(labels)

test_images, test_labels = load_test_data('10/test')
test_labels = np.array(test_labels)

test_loss = model.evaluate(test_images, test_labels, batch_size=32)

print(f'Test Loss: {test_loss}')

def load_validation_data(data_dir, num_coordinates=4):
    images = []
    labels = []

    for image_file in os.listdir(os.path.join(data_dir, 'images')):
        img_path = os.path.join(data_dir, 'images', image_file)
        img = cv2.imread(img_path)
        img = cv2.resize(img, (224, 224))
        images.append(img)

        label_path = os.path.join(data_dir, 'labels', image_file.replace('.jpg', '.txt'))
        with open(label_path, 'r') as file:
            label_str = file.read().strip().split()
            label = list(map(float, label_str[1:]))[:num_coordinates]
            labels.append(label + [0.0] * (num_coordinates - len(label)))

    return np.array(images), np.array(labels)

valid_images, valid_labels = load_validation_data('10/valid')
valid_labels = np.array(valid_labels)

validation_loss = model.evaluate(valid_images, valid_labels, batch_size=32)

print(f'Validation Loss: {validation_loss}')

import cv2
import numpy as np

def calculate_iou(box1, box2):
    """
    Calculate IoU (Intersection over Union) for two bounding boxes.
    """
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[0] + box1[2], box2[0] + box2[2])
    y2 = min(box1[1] + box1[3], box2[1] + box2[3])

    intersection = max(0, x2 - x1) * max(0, y2 - y1)
    area_box1 = box1[2] * box1[3]
    area_box2 = box2[2] * box2[3]
    union = area_box1 + area_box2 - intersection

    iou = intersection / union if union > 0 else 0.0
    return iou

predictions = model.predict(test_images)

iou_values = []
for i in range(len(predictions)):
    predicted_box = predictions[i][:4]
    true_box = test_labels[i][:4]

    iou = calculate_iou(predicted_box, true_box)
    iou_values.append(iou)

mean_iou = np.mean(iou_values)

print(f'Mean IoU: {mean_iou}')

accuracy_percentage = mean_iou * 100

print(f'Accuracy: {accuracy_percentage:.2f}%')

!pip install joblib

#Make a model file
import joblib
joblib.dump(model, 'model.pkl')

import cv2
import numpy as np
import joblib

def load_and_preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))
    img = np.expand_dims(img, axis=0)
    return img

def predict_image(model, image_path):
    input_image = load_and_preprocess_image(image_path)
    predictions = model.predict(input_image)
    x, y, width, height = predictions[0]

    return x, y, width, height

loaded_model = joblib.load('/content/model.pkl')

image_path_to_predict = '/content/download.jpg'
predicted_coordinates = predict_image(loaded_model, image_path_to_predict)

print(f'Predicted coordinates: {predicted_coordinates}')