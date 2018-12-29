
from keras.models import Sequential
from keras.layers import Conv2D

"""
Conv2D(filters=, kernel_size=, strides=, padding=, activation=, input_shape=)
- strides, default = 1
- padding, valid or same, default = valid 
- input_shape, tuple specifying the height, width, and depth of the input
"""

# Example #1
model = Sequential()
model.add(Conv2D(filters=16, kernel_size=2, strides=2, padding='valid', activation='relu', input_shape=(200, 200, 1)))
Conv2D(filters=32, kernel_size=3, padding='same', activation='relu')
Conv2D(64, (2, 2), activation='relu')