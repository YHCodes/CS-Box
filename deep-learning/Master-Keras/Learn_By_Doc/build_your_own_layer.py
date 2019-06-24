import numpy as np
import tensorflow as tf
from tensorflow.keras import layers

# https://keras.io/zh/layers/writing-your-own-keras-layers/

### 自定义层
# tf.keras.layers.Layer 进行子类化并实现以下方法来创建自定义层
# build : 创建层的权重, 使用 add_weight 方法添加权重
# call: 定义前向传播
# compute_output_shape: 指定在给定输入形状的情况下如何计算层的输出形状。
#           或者，可以通过实现 get_config 方法和 from_config 类方法序列化层。
class MyLayer(layers.Layer):
    def __init__(self, output_dim, **kwargs):
        self.output_dim = output_dim
        super(MyLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        shape = tf.TensorShape((input_shape[1], self.output_dim))

        # 为该层创建一个可训练的权重
        self.kernel = self.add_weight(name='kernel1',
                                      shape=shape,
                                      initializer='uniform',
                                      trainable=True)
        # 一定要在最后调用它
        super(MyLayer, self).build(input_shape)

    def call(self, inputs):
        return tf.matmul(inputs, self.kernel)

    def compute_output_shape(self, input_shape):
        shape = tf.TensorShape(input_shape).as_list()
        shape[-1] = self.output_dim
        return tf.TensorShape(shape)

    def get_config(self):
        base_config = super(MyLayer, self).get_config()
        base_config['output_dim'] = self.output_dim
        return base_config

    @classmethod
    def from_config(cls, config):
        return cls(**config)


# 创造虚拟数据
train_x = np.random.random((1000, 72))
train_y = np.random.random((1000, 10))

val_x = np.random.random((200, 72))
val_y = np.random.random((200, 10))

model = tf.keras.Sequential(
    [
        MyLayer(10),
        layers.Activation('softmax')
    ]
)

model.compile(optimizer=tf.keras.optimizers.RMSprop(0.001),
              loss=tf.keras.losses.categorical_crossentropy,
              metrics=['accuracy'])

#model.fit(train_x, train_y, batch_size=16, epochs=5)

# 回调
callbacks = [
    tf.keras.callbacks.EarlyStopping(patience=2, monitor='val_loss'),
    tf.keras.callbacks.TensorBoard(log_dir='./logs')
]

model.fit(train_x,
          train_y,
          batch_size=16,
          epochs=5,
          callbacks=callbacks,
          validation_data=(val_x, val_y))
