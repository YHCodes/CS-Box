[TOC]

### Optimizers



**parameters common to all keras optimizers**

`clipnorm` and `clipvalue`

```python
from keras import optimizers

# All parameters gradients will be clipped to a maximum norm of 1
sgd = optimizers.SGD(lr=0.01, clipnorm=1.)

# All parameters gradients will be clipped to 
# a maximum value of 0.5 and
# a minimum value of -0.5
sgd2 = optimizers.SGD(lr=0.01, clipvalue=0.5)
```



- **SGD** : support for momentum
- **RMSprop** : good choice for RNNs, 推荐使用默认参数
- **Adagrad** : 推荐使用默认参数
- **Adadelta** :
- **Adam**
- **Adamax**
- **Nadam**

**Reference:**

[optimizers](https://keras.io/optimizers/)

### Resources

[keras.io](https://keras.io/)



### 

