import tensorflow as tf
from tensorflow.keras import layers
import numpy as np

# model = tf.keras.Sequential([
#     tf.keras.layers.Dense(64, activation='relu'),
#     tf.keras.layers.Dense(10, activation='softmax')
# ])
#
# model.compile(optimizer=tf.keras.optimizers.Adam(0.001),
#               loss=tf.keras.losses.categorical_crossentropy,
#               metrics=[tf.keras.metrics.categorical_accuracy])

### 模型子类化
# 在 init 方法中创建层并将它们设置为类实例的属性
# 在 call 方法中定义前向传播
class MyModel(tf.keras.Model):
    def __init__(self, num_classes=10):
        super(MyModel, self).__init__(name='my_model')
        self.num_classes = num_classes
        self.layer1 = layers.Dense(32, activation='relu')
        self.layer2 = layers.Dense(num_classes, activation='softmax')

    def call(self, inputs):
        h1 = self.layer1(inputs)
        out = self.layer2(h1)
        return out

    def compute_output_shape(self, input_shape):
        shape = tf.TensorShape(input_shape).as_list()
        shape[-1] = self.num_classes
        return tf.TensorShape(shape)


# 创造虚拟数据
train_x = np.random.random((1000, 72))
train_y = np.random.random((1000, 10))

model = MyModel(num_classes=10)

model.compile(optimizer=tf.keras.optimizers.RMSprop(0.001),
              loss=tf.keras.losses.categorical_crossentropy,
              metrics=[tf.keras.metrics.categorical_accuracy])

model.fit(train_x, train_y, batch_size=16, epochs=5)

model.save_weights('./weights/model')
model.load_weights('./weights/model')
model.save_weights('./models/model.h5')
model.load_weights('./models/model.h5')

# import json
# import pprint
# json_str = model.to_json()
# pprint.pprint(json.loads(json_str))
# fresh_model = tf.keras.models.model_from_json(json_str)
