"""
In this quiz you will build a simple multi-layer
feedforward neural network to solve the XOR problem.
"""

import numpy as np
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Activation

# Set random seed
np.random.seed(42)

# Our data
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]]).astype('float32')
y = np.array([[0], [1], [1], [0]]).astype('float32')

# One-hot encoding the output
y = np_utils.to_categorical(y)

# Building the model
xor = Sequential()
xor.add(Dense(8, input_dim=2))
xor.add(Activation("tanh"))
xor.add(Dense(2))
xor.add(Activation("softmax"))

xor.compile(loss="categorical_crossentropy", optimizer="adam", metrics=['accuracy'])

# print the model architecture
xor.summary()

# Fitting the model
history = xor.fit(X, y, epochs=3000, verbose=0)

# Scoring the model
score = xor.evaluate(X, y)
print("\nAccuracy: ", score[-1])

# Checking the predictions
print("\nPredictions:")
print(xor.predict_proba(X))