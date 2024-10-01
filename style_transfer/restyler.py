import os
from utils import clip_0_1, load_img, patch_image
from style_transfer.style_content_model import  StyleContentModel
from constants import STYLE_LAYERS, CONTENT_LAYERS, STYLE_WEIGHT, CONTENT_WEIGHT, TOTAL_VARIATION_WEIGHT, STEPS_PER_EPOCH
import tensorflow as tf
from keras import optimizers, applications

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DEFAULT_BASE_NST_MODEL = 'vgg_model_nst3.keras'


class Restyler:
    def __init__(self, model_path=f'{DIR_PATH}/models/{DEFAULT_BASE_NST_MODEL}', model_name='vgg19'):
        self.base_model_path = model_path
        self.base_model_name = model_name
        self.base_model = applications.VGG19(include_top=False, weights='imagenet')
        self.base_model.trainable = False
        self.base_model.save(self.base_model_path)
        self.content_image = None
        self.mask_image = None
        self.style_image = None
        self.style_layers = STYLE_LAYERS
        self.content_layers = CONTENT_LAYERS
        self.style_weight = STYLE_WEIGHT
        self.content_weight = CONTENT_WEIGHT
        self.steps_per_epoch = STEPS_PER_EPOCH
        self.restyling_progress = 0
        self.style_targets = None 
        self.content_targets = None
        self.total_variation_weight = TOTAL_VARIATION_WEIGHT
        self.extractor = StyleContentModel(self.base_model, self.style_layers, self.content_layers)
        self.optimizer = optimizers.Adam(learning_rate=0.02, beta_1=0.99, epsilon=1e-1)


    def add_content_image(self, content_image_path):
        self.content_image = load_img(content_image_path)
        self.content_image_tf = tf.Variable(self.content_image)
        self.content_targets = self.extractor(self.content_image)['content']


    def add_style_image(self, style_image_path):
        self.style_image = load_img(style_image_path)
        self.style_targets = self.extractor(self.style_image)['style']
        

    def add_mask_image(self, mask_image_path):
        self.mask_image = load_img(mask_image_path, 1) if mask_image_path is not None else None


    def style_content_loss(self, outputs):
        style_outputs = outputs['style']
        content_outputs = outputs['content']
        style_loss = tf.add_n([tf.reduce_mean((style_outputs[name] - self.style_targets[name])**2)
                            for name in style_outputs.keys()])
        style_loss *= self.style_weight / len(self.style_layers)

        content_loss = tf.add_n([tf.reduce_mean((content_outputs[name] - self.content_targets[name])**2)
                                for name in content_outputs.keys()])
        content_loss *= self.content_weight / len(self.content_layers)
        loss = style_loss + content_loss

        return loss


    def train_step_total_var_loss(self):
        with tf.GradientTape() as tape:
            outputs = self.extractor(self.content_image_tf)
            loss = self.style_content_loss(outputs)
            loss += self.total_variation_weight * tf.image.total_variation(self.content_image_tf)

        grad = tape.gradient(loss, self.content_image_tf)
        self.optimizer.apply_gradients([(grad, self.content_image_tf)])
        self.content_image_tf.assign(clip_0_1(self.content_image_tf))


    def restyle(self, train_iter_no, invert_mode):
        self.restyling_progress = 0
        epochs = train_iter_no
        for n in range(epochs):
            for m in range(self.steps_per_epoch):
                self.restyling_progress += (100 //(epochs * self.steps_per_epoch))
                self.train_step_total_var_loss()
            res_image = self.content_image_tf

        res_image = patch_image(self.content_image, self.mask_image, res_image, mode=invert_mode)

        return res_image
