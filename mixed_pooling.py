import tensorflow as tf
import keras as K


class MixedPooling(K.layers.Layer):
    def __init__(self, p=0.5, **kwargs):
        super(MixedPooling, self).__init__(**kwargs)
        self.p = 0

    def call(self, inputs, **kwargs):
        return self.p * tf.reduce_max(inputs, axis=-1) + (1 - self.p) * tf.reduce_mean(inputs, axis=-1)

    def compute_output_shape(self, input_shape):
        # output_shape = self.call(tf.zeros(input_shape))
        # return output_shape.shape
        return input_shape[0], input_shape[1]

    def get_config(self):
        base_config = super(MixedPooling, self).get_config()
        return dict(list(base_config.items()))
