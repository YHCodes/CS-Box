import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers.core import Dense, Dropout


def plot_points(data):
    X = np.array(data[['gre', 'gpa']])
    y = np.array(data['admit'])
    admitted = X[np.argwhere(y == 1)]
    rejected = X[np.argwhere(y == 0)]
    plt.scatter([s[0][0] for s in rejected], [s[0][1] for s in rejected], s=25, color='red', edgecolors='k')
    plt.scatter([s[0][0] for s in admitted], [s[0][1] for s in admitted], s=25, color='cyan', edgecolors='k')
    plt.xlabel('Test (GRE)')
    plt.ylabel('Grades (GPA)')


"""
1. Loading the data
"""
data = pd.read_csv('student_data.csv')
print(data[:5])

"""
2. One-hot encoding the rank
"""
one_hot_data = pd.concat([data, pd.get_dummies(data['rank'], prefix='rank')], axis=1)
one_hot_data = one_hot_data.drop('rank', axis=1)
print(one_hot_data[:5])

"""
3. Scaling the data
"""
processed_data = one_hot_data[:]
processed_data['gre'] = one_hot_data['gre']/800
processed_data['gpa'] = one_hot_data['gpa']/4.0
print(processed_data[:5])

"""
4. Splitting the data into Training and Testing
"""
sample = np.random.choice(processed_data.index, size=int(len(processed_data)*0.9), replace=False)
train_data, test_data = processed_data.iloc[sample], processed_data.drop(sample)
print('Number of training samples is', len(train_data))
print('Number of testing samples is', len(test_data))
print(train_data[:5])
print(test_data[:5])

"""
5. Splitting the data into features and targets (labels)
"""
features = np.array(train_data.drop('admit', axis=1))
targets = np.array(to_categorical(train_data['admit'], 2))
features_test = np.array(test_data.drop('admit', axis=1))
targets_test = np.array(to_categorical(test_data['admit'], 2))
print(features[:3])
print(targets[:3])

"""
6. Defining the model architecture
"""
model = Sequential()
model.add(Dense(128, activation='relu', input_shape=(6,)))
model.add(Dropout(0.2))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(2, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
model.summary()

"""
7.Training the model
"""
model.fit(features, targets, epochs=500, batch_size=32, verbose=0)

"""
8.Scoring the model
"""
score = model.evaluate(features, targets)
print('\n Training Accuracy:', score[1])
score = model.evaluate(features_test, targets_test)
print('\n Testing Accuracy:', score[1])
