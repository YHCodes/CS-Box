[TOC]

# Neural Networks



## 2. Implementing Gradient Descent

### 2.1 Mean Squared Error Function

> is the mean of the squares of the differences between the predictions and the labels.

### 2.2 Gradient Descent

神经网络的输出需要尽可能接近真实值，可以用SSE来进行衡量。

我们的目标是寻找神经网络的最优权值

(1) The Sum of Squared Errors, SSE 误差平方和

​	$E=\frac{1}{2}\sum_{\mu}\sum_{j}\left[y_{j}^{\mu}-\hat{y}_{j}^{\mu}\right]^{2}$

- first, take the sum over all output units $j$
- and another sum over all data points $\mu$
-  The square ensures the error is always **positive** and larger errors are penalized more than smaller errors

(2) 已知神经网络的输出

​	 $\hat{y}^{\mu}_j = f(\sum_i w_{ij}x^{\mu}_{i})$

可以得知，SSE取决于 $w_{ij}$

​	$E = \frac{1}{2} \sum_{\mu} \sum_{j} \left[y^{\mu}_{j} - f(\sum_{i}w_{ij}x^{\mu}_{i})\right]^2$

我们的目标：**寻找 $w_{ij}$ 使得 $E$ 最小**, 

方法：Gradient Descent

### 2.3 Gradient Descent: The Math

已知， $\hat{y} = f(h)$  where  $h = \sum_{i}w_{i}x_{i}$

​	$\frac{\part E}{\part w_{i}} = \frac{\part}{\part w_{i}} \frac{1}{2} (y - \hat{y})^2$

​		$= -(y - \hat{y}) \frac{\part{\hat{y}}}{\part w_{i}} =  -(y - \hat{y}) f^{\prime}(h)x_{i}$ 

​	$\Delta w = \eta (y - \hat{y}) f^{\prime}(h)x_{i}$



**ERROR TERM:**

​	$\delta = (y - \hat{y}) f^{\prime}(h)$

**Weight update:**

​	$w_{i} = w_{i} + \eta \delta x_{i}$	

**IF MULTIPLE OUTPUT UNITS:**

​	$\delta_{j} = (y_{j} - \hat{y_{j}}) f^{\prime}(h_{j})$

​	$\Delta w_{ij} = \eta * \delta_{j}*x_{i}$

### 2.4 Gradient Descent: The Code

```python
import numpy as np

def sigmoid(x):
    """
    Calculate sigmoid
    """
    return 1/(1+np.exp(-x))

def sigmoid_prime(x):
    """
    # Derivative of the sigmoid function
    """
    return sigmoid(x) * (1 - sigmoid(x))

learnrate = 0.5
x = np.array([1, 2. 3, 4])
y = np.array(0.5)

# Initial weights
w = np.array([0.5, -0.5, 0.3, 0.1])

### Calculate one gradient descent step for each weight
### Note: Some steps have been consilated, so there are
###       fewer variable names than in the above sample code

# TODO: Calculate the node's linear combination of inputs and weights
h = np.dot(x, w)

# TODO: Calculate output of neural network
nn_output = sigmoid(h)

# TODO: Calculate error of neural network
error = y - nn_output

# TODO: Calculate the error term
#       Remember, this requires the output gradient, which we haven't
#       specifically added a variable for.
error_term = error * sigmoid_prime(h)

# TODO: Calculate change in weights
del_w = learnrate * error_term * x

print('Neural Network output:')
print(nn_output)
print('Amount of Error:')
print(error)
print('Change in Weights:')
print(del_w)
```

### 2.5 Implementing Gradient Descent

**Implementing the hidden layer**

multiple input units and multiple hidden units, the weights between them will require two indices: $w_{ij}$ where $i$ denotes input units and $j$ are the hidden units.

**Weights matrix**:

- Each **row** in the matrix will correspond to the weights **leading out** of a **single input unit**
- Each **column** will correspond to the weights **leading in** to a **single hidden unint**.

![](pics/weights_matrix.png)

**initialize weights:**

```python
n_records, n_inputs = features.shape
n_hidden = 2
weights_input_to_hidden = np.random.normal(0, n_inputs**-0.5, size=(n_inputs, n_hidden))
```

**calculate hidden layer:**

$h_{1} = x_{1}w_{11} + x_{2}w_{21} + x_{3}w_{31}$

`hidden_inputs  = np.dot(inputs, weights_input_to_hidden)`

**Making a column vector:**

-  `arr.T` : transpose
  - but for a 1D array, the transpose will return a row vector.
  - alternatively, create arrays with two diemensions, then use `arr.T` to get the column vector.
- `arr[:, None]`: create a column vector

**Quiz:**

implement a forward pass through a 4x3x2 network, with sigmoid activation functions for both layers. Things to do:

- Calculate the input to the hidden layer.
- Calculate the hidden layer output.
- Calculate the input to the output layer.
- Calculate the output of the network.

```python
import numpy as np

def sigmoid(x):
    """
    Calculate sigmoid
    """
    return 1/(1+np.exp(-x))

# Network size
N_input = 4
N_hidden = 3
N_output = 2

np.random.seed(42)
# Make some fake data
X = np.random.randn(4)

weights_input_to_hidden = np.random.normal(0, scale=0.1, size=(N_input, N_hidden))
weights_hidden_to_output = np.random.normal(0, scale=0.1, size=(N_hidden, N_output))


# TODO: Make a forward pass through the network
hidden_layer_in = np.dot(X, weights_input_to_hidden)
hidden_layer_out = sigmoid(hidden_layer_in)

print('Hidden-layer Output:')
print(hidden_layer_out)

output_layer_in = np.dot(hidden_layer_out, weights_hidden_to_output)
output_layer_out = sigmoid(output_layer_in)

print('Output-layer Output:')
print(output_layer_out)
```

### 2.6 Backprogation

To update the weights to hidden layers using gradient descent, you need to know how much error each of the hidden units contributed to the final output.



For example, in the output layer, you have errors $\delta^o_k$ attributed to each output unit $k$.

Then, the error attributed to hidden unit $j$ is the output errors, scaled by the weights between the output and hidden layers(and the gradient):

​	$\delta^h_j = \sum W_{jk} \delta^o_k f^\prime(h_j)$

The gradient descent step:

​	$\Delta w_{ij} = \eta\delta^h_j x_i$

The weight steps are equal to the step size *times* the output error of the layer *times* the values of the inputs to that layer:

​	$\Delta w_{pq} = \eta \delta_{output}V_{in}$



**Backpropagation exercise**

Now you're going to implement the backprop algorithm for a network trained on the graduate school admission data. You should have everything you need from the previous exercises to complete this one.

Your goals here:

- Implement the forward pass.
- Implement the backpropagation algorithm.
- Update the weights.

```python
import pandas as pd

admissions = pd.read_csv('binary.csv')

# Make dummy variables for rank
data = pd.concat([admissions, pd.get_dummies(admissions['rank'], prefix='rank')], axis=1)
data = data.drop('rank', axis=1)

# Standarize features
for field in ['gre', 'gpa']:
    mean, std = data[field].mean(), data[field].std()
    data.loc[:,field] = (data[field]-mean)/std
    
# Split off random 10% of the data for testing
np.random.seed(21)
sample = np.random.choice(data.index, size=int(len(data)*0.9), replace=False)
data, test_data = data.ix[sample], data.drop(sample)

# Split into features and targets
features, targets = data.drop('admit', axis=1), data['admit']
features_test, targets_test = test_data.drop('admit', axis=1), test_data['admit']
```



```python
# backprop.py
import numpy as np
from data_prep import features, targets, features_test, targets_test

np.random.seed(21)

def sigmoid(x):
    """
    Calculate sigmoid
    """
    return 1 / (1 + np.exp(-x))


# Hyperparameters
n_hidden = 2  # number of hidden units
epochs = 900
learnrate = 0.005

n_records, n_features = features.shape
last_loss = None
# Initialize weights
weights_input_hidden = np.random.normal(scale=1 / n_features ** .5,
                                        size=(n_features, n_hidden))
weights_hidden_output = np.random.normal(scale=1 / n_features ** .5,
                                         size=n_hidden)

for e in range(epochs):
    del_w_input_hidden = np.zeros(weights_input_hidden.shape)
    del_w_hidden_output = np.zeros(weights_hidden_output.shape)
    for x, y in zip(features.values, targets):
        ## Forward pass ##
        # TODO: Calculate the output
        hidden_input = np.dot(x, weights_input_hidden)
        hidden_output = sigmoid(hidden_input)

        output = sigmoid(np.dot(hidden_output,
                                weights_hidden_output))

        ## Backward pass ##
        # TODO: Calculate the network's prediction error
        error = y - output

        # TODO: Calculate error term for the output unit
        output_error_term = error * output * (1 - output)

        ## propagate errors to hidden layer

        # TODO: Calculate the hidden layer's contribution to the error
        hidden_error = np.dot(output_error_term, weights_hidden_output)

        # TODO: Calculate the error term for the hidden layer
        hidden_error_term = hidden_error * hidden_output * (1 - hidden_output)

        # TODO: Update the change in weights
        del_w_hidden_output += output_error_term * hidden_output
        del_w_input_hidden += hidden_error_term * x[:, None]

    # TODO: Update weights
    weights_input_hidden += learnrate * del_w_input_hidden / n_records
    weights_hidden_output += learnrate * del_w_hidden_output / n_records

    # Printing out the mean square error on the training set
    if e % (epochs / 10) == 0:
        hidden_output = sigmoid(np.dot(x, weights_input_hidden))
        out = sigmoid(np.dot(hidden_output,
                             weights_hidden_output))
        loss = np.mean((out - targets) ** 2)

        if last_loss and last_loss < loss:
            print("Train loss: ", loss, "  WARNING - Loss Increasing")
        else:
            print("Train loss: ", loss)
        last_loss = loss

# Calculate accuracy on test data
hidden = sigmoid(np.dot(features_test, weights_input_hidden))
out = sigmoid(np.dot(hidden, weights_hidden_output))
predictions = out > 0.5
accuracy = np.mean(predictions == targets_test)
print("Prediction accuracy: {:.3f}".format(accuracy))
```

### Resources

[Why Momentum Really Works, from distill](https://distill.pub/2017/momentum/)

[可汗学院](https://www.khanacademy.org/math/)

[Yes, you should understand backprop](https://medium.com/@karpathy/yes-you-should-understand-backprop-e2f06eab496b#.vt3ax2kg9)

[a lecture from Stanford's CS231n course](https://www.youtube.com/watch?v=59Hbtz7XgjM)





 

​	



