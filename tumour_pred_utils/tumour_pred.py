from PIL import Image
import numpy as np
import io
import matplotlib.pyplot as plt
import streamlit as st
from keras.models import load_model

model = load_model('tumour_pred_utils/modelICP75.h5')


def process_image(image_data):
    img = Image.open(io.BytesIO(image_data))
    img = img.resize((75,75))
    img_array = np.array(img)
    img_array = img_array/255.0
    return img_array.reshape(1,75,75,3)


def predict_cancer(image_data):
    processed_image = process_image(image_data)
    prediction = model.predict(processed_image)
    return prediction

def gradient_color(value, min_value, max_value, cmap='RdYlGn_r'):
    norm_value = (value - min_value) / (max_value - min_value)
    cmap = plt.get_cmap(cmap)
    rgba_color = cmap(norm_value)
    hex_color = "#{:02x}{:02x}{:02x}".format(
        int(rgba_color[0] * 255),
        int(rgba_color[1] * 255),
        int(rgba_color[2] * 255)
    )
    return hex_color
