import tensorflow as tf
import cv2
import numpy as np
from constants import THRESHOLD_PARAM, BLUR_KERNEL_SIZE, MAX_IMG_DIM


def load_img(img_path, channels_no=3):
    img = tf.io.read_file(img_path)
    img = tf.image.decode_image(img, channels=channels_no)
    img = tf.image.convert_image_dtype(img, tf.float32)

    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = MAX_IMG_DIM / long_dim

    new_shape = tf.cast(shape * scale, tf.int32)

    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]

    return img


def refine_mask(image, mask):
    mask_rgb = cv2.cvtColor(mask[0], cv2.COLOR_RGB2BGR)
    mask_grayscale = cv2.cvtColor(mask_rgb, cv2.COLOR_BGR2GRAY)
    mask_grayscale = cv2.medianBlur(mask_grayscale, BLUR_KERNEL_SIZE)
    _, thresh = cv2.threshold(mask_grayscale, 0, THRESHOLD_PARAM, cv2.THRESH_BINARY)
    thresh_rsz = cv2.resize(thresh, (image[0].shape[1],
                                     image[0].shape[0]), 
                                     interpolation= cv2.INTER_LANCZOS4)

    return thresh_rsz


def clip_0_1(image):
    return tf.clip_by_value(image, clip_value_min=0.0, clip_value_max=1.0)


def gram_matrix(input_tensor):
    result = tf.linalg.einsum('bijc,bijd->bcd', input_tensor, input_tensor)
    input_shape = tf.shape(input_tensor)
    num_locations = tf.cast(input_shape[1]*input_shape[2], tf.float32)

    return result/(num_locations)


def vgg_layers(vgg_model, layer_names):
    """ Creates a VGG model that returns a list of intermediate output values."""
    vgg_model.trainable = False
    outputs = [vgg_model.get_layer(name).output for name in layer_names]
    vgg_model = tf.keras.Model([vgg_model.input], outputs)

    return vgg_model


def high_pass_x_y(image):
    x_var = image[:, :, 1:, :] - image[:, :, :-1, :]
    y_var = image[:, 1:, :, :] - image[:, :-1, :, :]

    return x_var, y_var


def total_variation_loss(image):
    x_deltas, y_deltas = high_pass_x_y(image)

    return tf.reduce_sum(tf.abs(x_deltas)) + tf.reduce_sum(tf.abs(y_deltas))


def patch_image(content_image, image_mask, res_image, mode=0):
    res_image_np = res_image[0].numpy()
    content_image_np = content_image[0].numpy()
    if image_mask is not None:
        image_mask_np = image_mask[0].numpy()
        image_mask_np = np.squeeze(image_mask_np)
        image_mask_np = image_mask_np * 255
        mask_binary = image_mask_np > 1

        if mode==1:
            combined_image_np = np.where(mask_binary[..., None], res_image_np, content_image_np)
        else:
            combined_image_np = np.where(mask_binary[..., None], content_image_np, res_image_np)
    else:
        combined_image_np = res_image_np

    return combined_image_np
