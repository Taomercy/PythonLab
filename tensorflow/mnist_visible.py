#!/usr/bin/env python
# encoding:utf-8
import numpy as np
import tensorflow as tf
import os
import tensorflow.examples.tutorials.mnist.input_data as input_data
from PIL import Image
import matplotlib.pyplot as plt


def main():
    mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
    batch_xs, batch_ys = mnist.train.next_batch(1)
    batch_xs = batch_xs.reshape(28, 28)
    plt.figure("Image")
    plt.imshow(batch_xs)
    plt.axis('on')
    plt.title('image')
    plt.show()
    print(batch_ys)
    print(mnist.label)


if __name__ == '__main__':
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    old_v = tf.logging.get_verbosity()
    tf.logging.set_verbosity(tf.logging.ERROR)
    main()
    tf.logging.set_verbosity(old_v)
