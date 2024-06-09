import tensorflow as tf
import keras as K


class L1Pooling(K.layers.Layer):
    def __init__(self, **kwargs):
        super(L1Pooling, self).__init__(**kwargs)

    def call(self, inputs, **kwargs):
        return tf.reduce_sum(tf.abs(inputs), axis=-1)

    def compute_output_shape(self, input_shape):
        return input_shape[0], input_shape[1]

    def get_config(self):
        return super(L1Pooling, self).get_config()

    @classmethod
    def from_config(cls, config):
        return cls(**config)
