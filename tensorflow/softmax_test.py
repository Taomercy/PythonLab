#!/usr/bin/env python
# encoding:utf-8
import numpy as np
import tensorflow as tf
import os
import tensorflow.examples.tutorials.mnist.input_data as input_data

def main():
    sess = tf.InteractiveSession()
    mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
    x = tf.placeholder("float", [None, 784], name='x')
    y_ = tf.placeholder("float", [None,10], name='y_')

    W = tf.Variable(tf.zeros([784,10]), name='W')
    b = tf.Variable(tf.zeros([10]), name='b')

    init = tf.initialize_all_variables()
    sess.run(init)

    y = tf.nn.softmax(tf.matmul(x, W) + b)

    with tf.name_scope("cross-entropy-model"):
        cross_entropy = -1*tf.reduce_sum(y_*tf.log(y))
        tf.summary.scalar("cross-entropy", cross_entropy)

    #for tensor board
    merged = tf.summary.merge_all()
    writer = tf.summary.FileWriter('/tmp/tensorflow', sess.graph)

    train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
    for i in range(1000):
        batch_xs, batch_ys = mnist.train.next_batch(100)
        sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
        summary, _ = sess.run([merged, train_step], {x: batch_xs, y_: batch_ys})
        writer.add_summary(summary, i)

    correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction , "float"))
    print accuracy.eval(feed_dict={x: mnist.test.images, y_: mnist.test.labels})






if __name__ == '__main__':
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    old_v = tf.logging.get_verbosity()
    tf.logging.set_verbosity(tf.logging.ERROR)
    main()
    tf.logging.set_verbosity(old_v)
