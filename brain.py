import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

from os import listdir
from PIL import Image
from io import BytesIO
from keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import decode_predictions


class Brain:
    def __init__(self):
        self.model = VGG16(weights='imagenet')

    def analyze_image(self, url):
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img = img.resize((224, 224))
        img_data = image.img_to_array(img)
        img_data = np.expand_dims(img_data, axis=0)
        img_data = preprocess_input(img_data)
        prediction = self.model.predict(img_data)
        label = decode_predictions(prediction)
        return(label)
