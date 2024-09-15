import tensorflow as tf
import matplotlib.pyplot as plt
import cv2
import numpy as np
from constants import THRESHOLD_PARAM, BLUR_KERNEL_SIZE


def load_img(img_path):
    max_dim = 512
    img = tf.io.read_file(img_path)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)

    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = max_dim / long_dim

    new_shape = tf.cast(shape * scale, tf.int32)

    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]

    return img


def img_show(image, title=None):
    if len(image.shape) > 3:
        image = tf.squeeze(image, axis=0)

    plt.imshow(image)

    if title:
        plt.title(title)


def refine_mask(image, mask):
    mask_rgb = cv2.cvtColor(mask[0], cv2.COLOR_RGB2BGR)
    mask_grayscale = cv2.cvtColor(mask_rgb, cv2.COLOR_BGR2GRAY)
    mask_grayscale = cv2.medianBlur(mask_grayscale, BLUR_KERNEL_SIZE)
    _, thresh = cv2.threshold(mask_grayscale, 0, THRESHOLD_PARAM, cv2.THRESH_BINARY)
    thresh_rsz = cv2.resize(thresh, (image[0].shape[1],
                                     image[0].shape[0]), 
                                     interpolation= cv2.INTER_LANCZOS4)

    return thresh_rsz

def inverting_mask(mask, inverse=False):
    patch = None
    if inverse:
        mask_neg = 1 - mask
        patch = np.where(mask_neg > 0)
    else:
        patch = np.where(mask > 1)

    return patch