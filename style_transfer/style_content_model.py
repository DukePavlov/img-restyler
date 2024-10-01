from utils import vgg_layers, gram_matrix
import tensorflow as tf


class StyleContentModel(tf.keras.models.Model):
    def __init__(self, base_model, style_layers, content_layers):
        super(StyleContentModel, self).__init__()
        self.model = base_model
        self.vgg = vgg_layers(self.model, style_layers + content_layers)
        self.style_layers = style_layers
        self.content_layers = content_layers
        self.num_style_layers = len(style_layers)
        self.vgg.trainable = False


    def call(self, inputs):
        "Expects float input in [0,1]"
        inputs = inputs * 255.0
        preprocessed_input = tf.keras.applications.vgg19.preprocess_input(inputs)
        outputs = self.vgg(preprocessed_input)
        style_outputs, content_outputs = (outputs[:self.num_style_layers], 
                                          outputs[self.num_style_layers:])

        style_outputs = [gram_matrix(style_output)
                            for style_output in style_outputs]

        content_dict = {content_name: value
                        for content_name, value
                        in zip(self.content_layers, content_outputs)}

        style_dict = {style_name: value
                        for style_name, value
                        in zip(self.style_layers, style_outputs)}

        return {'content': content_dict, 
                'style': style_dict}
    