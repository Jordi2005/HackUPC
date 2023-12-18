import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input, decode_predictions
from tensorflow.keras.utils import load_img, img_to_array
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
from PIL import Image  

# Load the pre-trained VGG16 model
model = VGG16()

def predict_image(img_path):
    # Load and preprocess the image for VGG16
    img = Image.open(img_path)
    
    # Remove the alpha channel if it exists
    if img.mode == 'RGBA':
        img = img.convert('RGB')

    # Resize the image to (224, 224) 
    img = img.resize((224, 224))

    # Convert the image to a NumPy array
    img_array = np.array(img)

    # Normalize the pixel values to be in the range [0, 1]
    img_array = img_array / 255.0

    # Add a batch dimension to match the expected input shape of (None, 224, 224, 3)
    img_array = np.expand_dims(img_array, axis=0)


    # Get predictions
    predictions = model.predict(img_array)

    # Decode and print the top-3 predicted classes
    decoded_predictions = decode_predictions(predictions, top=1)[0]
    print("Predictions:")
    for i, (imagenet_id, label, score) in enumerate(decoded_predictions):
        print(f"{i + 1}: {label} ({score:.2f})")
    
    return label, score
 
 