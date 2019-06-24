import numpy as np
import tensorflow as tf
from tensorflow.keras import layers


# 创造虚拟数据
train_x = np.random.random((1000, 72))
train_y = np.random.random((1000, 10))
dataset = tf.data.Dataset.from_tensor_slices((train_x, train_y))
dataset = dataset.batch(32).repeat()

val_x = np.random.random((200, 72))
val_y = np.random.random((200, 10))
val_dataset = tf.data.Dataset.from_tensor_slices((val_x, val_y))
val_dataset = val_dataset.batch(32).repeat()

test_x = np.random.random((1000, 72))
test_y = np.random.random((1000, 10))
test_dataset = tf.data.Dataset.from_tensor_slices((test_x, test_y))
test_dataset = test_dataset.batch(32).repeat()













