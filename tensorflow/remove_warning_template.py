#!/usr/bin/env python
# encoding:utf-8
import numpy as np
import tensorflow as tf
import os

def main():
    pass



if __name__ == '__main__':
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    old_v = tf.logging.get_verbosity()
    tf.logging.set_verbosity(tf.logging.ERROR)
    main()
    tf.logging.set_verbosity(old_v)
