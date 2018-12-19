#!/usr/bin/env python
# encoding:utf-8
import numpy as np
import tensorflow as tf
import os
import tensorflow.examples.tutorials.mnist.input_data as input_data

def main():
    mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
    print mnist.train.images
    print mnist.train.labels
    print mnist.train.images.shape
    print mnist.train.labels.shape










if __name__ == '__main__':
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    old_v = tf.logging.get_verbosity()
    tf.logging.set_verbosity(tf.logging.ERROR)
    main()
    tf.logging.set_verbosity(old_v)
