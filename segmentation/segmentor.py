import os
from utils import load_img
import tensorflow as tf
import cv2
from keras.models import load_model, img_show, refine_mask


DEF_HEIGHT, DEF_WIDTH = 128, 128


class Segmentator:

    def __init__(self, model_path='models/UNet_model.h5', model_name='UNet'):
        self.model_path = model_path
        self.model_name = model_name
        self.image_resolution = (DEF_WIDTH, DEF_HEIGHT)
        self.model = None
        self.source_image = None

    def to_str(self):
        return f'Model path {self.model_path}\n Model name {self.model_name} \n 
                 Default image resolution for segmentation {self.image_resolution}'
    
    def load_model(self):
        self.model = load_model(self.model_path)

    def set_source_image(self, image_path):
        self.source_image = load_img(image_path)

    def segment_image(self):
        image_rsz = tf.image.resize(self.source_image, self.image_resolution)
        mask = self.model.predict(image_rsz)
        refined_mask = refine_mask(self.source_image, mask)

        return refined_mask
