import os
from utils import load_img, refine_mask
import tensorflow as tf
from keras.models import load_model
from constants import SEG_DEF_HEIGHT, SEG_DEF_WIDTH, SEG_DEFAULT_MODEL, SEG_DEFAULT_MODEL_DIR

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


class Segmentator:

    def __init__(self, model_path=f'{DIR_PATH}/models/{SEG_DEFAULT_MODEL}', model_name='UNet'):
        self.model_path = model_path
        self.model_name = model_name
        self.image_resolution = (SEG_DEF_HEIGHT, SEG_DEF_WIDTH)
        self.model = None
        self.source_image = None


    def to_str(self):
        return f'Model path {self.model_path}\n Model name {self.model_name} \n \
            Default image resolution for segmentation {self.image_resolution}'
    

    def load_model(self):
        self.model = load_model(self.model_path, compile=False)


    def set_source_image(self, image_path):
        self.source_image = load_img(image_path)


    def segment_image(self):
        image_rsz = tf.image.resize(self.source_image, self.image_resolution)
        mask = self.model.predict(image_rsz)
        refined_mask = refine_mask(self.source_image, mask)

        return refined_mask
