from PIL import Image
import numpy as np
import io
import matplotlib.pyplot as plt
import os
import streamlit as st
from tqdm import tqdm
import tensorflow as tf
from keras.models import load_model


model = load_model('tumour_pred_utils/modelICP75.h5')


def process_image(image_data):
    img = Image.open(image_data)
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

def parse_coordinates(filename):
    parts = filename.split('_')
    x = int(parts[-3][1:])
    y = int(parts[-2][1:])
    return x, y

@st.cache_data
def predict_cancer_batch(image_paths):
    predictions = np.zeros((len(image_paths), 2))
    for i, path in enumerate(tqdm(image_paths, desc="Predicting", leave=False)):
        predictions[i] = model.predict(process_image(path))
    return predictions

def get_image_and_heatmap():

    base_dir = os.path.join(os.getcwd(), 'IDC_regular_ps50_idx5\8864')
    image_paths = []
    for class_label in ['0', '1']:
        class_dir = os.path.join(base_dir, class_label)
        for filename in os.listdir(class_dir):
            if filename.endswith('.png'):
                image_paths.append(os.path.join(class_dir, filename))

    batch_predictions = predict_cancer_batch(image_paths)

    # Correctly create a list of labels based on filenames
    image_labels = [1 if 'class1' in path else 0 for path in image_paths]

    # Now filter predictions for "1" labeled images
    cancer_1_predictions = batch_predictions[np.array(image_labels) == 1]

    # Calculate the average probability of cancer for "1" labeled images
    average_probability_1 = np.mean(cancer_1_predictions[:, 1]) if cancer_1_predictions.size > 0 else 0

    # print(f"Probability of tumour presence: {average_probability_1:.2%}")

    max_x = max_y = 0
    for path in image_paths:
        x, y = parse_coordinates(os.path.basename(path))
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    image_size = 50
    grid_width = max_x // image_size + 1
    grid_height = max_y // image_size + 1

    # Initialize an empty white array for the full image
    full_image = np.ones((grid_height * 75, grid_width * 75, 3), dtype=np.uint8) * 255

    # Now let's ensure the images from both '0' and '1' folders are included
    for path, prediction in zip(image_paths, batch_predictions):
        x, y = parse_coordinates(os.path.basename(path))
        grid_x = x // image_size
        grid_y = y // image_size
        img = Image.open(path).resize((75, 75))
        img_array = np.array(img)
        # Assuming the non-tissue background is black, we only copy non-black pixels
        mask = img_array.sum(axis=2) != 0  # Summing the RGB channels; black would sum to 0
        full_image[grid_y*75:(grid_y+1)*75, grid_x*75:(grid_x+1)*75][mask] = img_array[mask]

    # Initialize an empty array for the probability map
    probability_map = np.zeros((grid_height * 75, grid_width * 75), dtype=np.float32)

    for path, prediction in zip(image_paths, batch_predictions):
        x, y = parse_coordinates(os.path.basename(path))
        grid_x = x // image_size
        grid_y = y // image_size
        img = Image.open(path).resize((75, 75))
        full_image[grid_y*75:(grid_y+1)*75, grid_x*75:(grid_x+1)*75] = np.array(img)
        probability_map[grid_y*75:(grid_y+1)*75, grid_x*75:(grid_x+1)*75] = prediction[1]  # Fill in the probability


    return average_probability_1, full_image, probability_map
