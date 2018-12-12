"""
Mini-batching: 同时只训练数据集的一部分
优点是即使计算机缺少内存也可以训练模型, 付出的代价就是训练不充分
结合SGD非常有用: randomly shuffle the data at the start of each epoch, then create the mini-batches.

first divide your data into batches
 > take advantage of tensorflow's tf.placeholder() function to receive the varying batch sizes.
 >

"""

from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
import numpy as np


def batches(batch_size, features, labels):
    """
    Create batches of features and labels
    :param batch_size: The batch size
    :param features: List of features
    :param labels: List of labels
    :return: Batches of (Features, Labels)
    """
    assert len(features) == len(labels)
    # TODO: Implement batching
    output_batches = []
    sample_size = len(features)
    for start_i in range(0, sample_size, batch_size):
        end_i = start_i + batch_size
        batch = [features[start_i:end_i], labels[start_i:end_i]]
        output_batches.append(batch)
    return output_batches


if __name__ == '__main__':
    learning_rate = 0.001
    n_input = 784   # MNIST data input (img shape: 28*28)
    n_classes = 10  # MNIST total classes (0-9 digits)

    # Import MNIST data
    mnist = input_data.read_data_sets('/datasets/ud730/mnist', one_hot=True)

    # The features are already scaled and the data is shuffled
    train_features = mnist.train.images  # shape=(55000, 784) Type:float32
    test_features = mnist.test.images

    train_labels = mnist.train.labels.astype(np.float32)  # shape=(55000, 10) Type:float32
    test_labels = mnist.test.labels.astype(np.float32)

    # Features and Labels
    features = tf.placeholder(tf.float32, [None, n_input])
    labels = tf.placeholder(tf.float32, [None, n_classes])

    # Weights & bias
    weights = tf.Variable(tf.random_normal([n_input, n_classes]))   # shape=(784, 10) Type:float32
    bias = tf.Variable(tf.random_normal([n_classes]))               # shape=(10,) Type:float32

    # logits = xW + b
    logits = tf.add(tf.matmul(features, weights), bias)

    # Define loss and optimizer
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=labels))
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate).minimize(cost)

    # Calculate accuracy
    correct_prediction = tf.equal(tf.argmax(logits, 1), tf.argmax(labels, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    # TODO: Set batch size
    batch_size = 128
    assert batch_size is not None, 'You must set the batch size'

    init = tf.global_variables_initializer()

    with tf.Session() as sess:
        sess.run(init)

        # TODO: Train optimizer on all batches
        for batch_features, batch_labels in batches(batch_size, train_features, train_labels):
            sess.run(optimizer, feed_dict={features: batch_features, labels: batch_labels})

        # Calculate accuracy for test dataset
        test_accuracy = sess.run(
            accuracy,
            feed_dict={features: test_features, labels: test_labels})

    print('Test Accuracy: {}'.format(test_accuracy))


"""
How many bytes of memory does train_features need?
> 55000*784*32/8 = 172,480,000 (bytes)

How many bytes of memory does train_labels need?
> 55000*10*32/8 = 2,200,000 (bytes)

How many bytes of memory does weights need?
> 784*10*32/8 = 31,360 (bytes)

How many bytes of memory does bias need?
> 10*32/8 = 40 (bytes)

total memory
> 174 megabytes

megabytes, 兆字节, 百万字节, MB
gigabytes, 千兆字节, 
"""



