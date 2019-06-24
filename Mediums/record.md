「」
2019/6/24

### [Comprehensive Introduction to Autoencoders](https://towardsdatascience.com/generating-images-with-autoencoders-77fd3a8dd368)

Denoising Autoencoders : 在训练之前为
Sparse Autoencoders
Contractive Autoencoders



### [What is a variational autoencoder?](https://jaan.io/what-is-variational-autoencoder-vae-tutorial/)

- [github, 474 - implementation](https://github.com/altosaar/variational-autoencoder)
- [Glossary](https://jaan.io/what-is-variational-autoencoder-vae-tutorial/#glossary)


- design complex 「generative models」 of data, and fit them to large datasets.


consist:

- 「**Encoder**」: The Encoder compresses data into a 「latent space」
- 「**Decoder**」: The Decoder reconstructs the data given the hidden representation.
- 「**Loss function**」: neagtive log-likelihood with a regularizer.

### [Up-sampling with Transposed Convolution](https://towardsdatascience.com/up-sampling-with-transposed-convolution-9ae4f2df52d0)



[distill - Deconvolution and Checkerboard Artifacts ](https://distill.pub/2016/deconv-checkerboard/)



The Need for Up-sampling

- 当我们使用神经网络去生成图片时，从低分辨率到到高分辨率的生成通常涉及到 Up-sampling



Up-samping 常用的方法

1. Nearest neighbor interpolation
2. Bi-linear interpolation
3. Bi-cubic interpolation



Why Transposed Convolution?



如果希望网络自己学会 Up-Sampling , 不使用预设 Interpolation 方法， 可以参考下面论文

[论文 - A guide to convolution arithmetic for deep learning](https://arxiv.org/abs/1603.07285)



应用：

[DCGAN](https://arxiv.org/pdf/1511.06434v2.pdf) 采用 randomly sampled values 来生成 full-size images.

[semantic segmentation](https://people.eecs.berkeley.edu/~jonlong/long_shelhamer_fcn.pdf) 在endoer使用卷积层来提取特征, 然后在 decoder 恢复至原图。

 

Convolution Operation

- forms a many-to-one relationship



Transposed Convolution

- one-to-many relationship
- 「convolution matrix」: an rearranged kernel weights
  - 例子：输入 4x4， 输出 2x2
  - kernel: 3x3  -> 4 x 16 (rearranged)
  - input: 4x4 -> 16 x 1 (rearranged)
  - (4 x 16) *  (16 x 1) -> (4 x 1)
- 「transposed convolution matrix」
  - 例子：输入 2x2 , 输出 4x4
  - C(4 x16)  C.T(16 x 4)
  - input: 4 x 1
  - C.T(16 x 4) * (4 x 1) -> (16, 1)



transposed convolution 不是卷积，

![img](https://cdn-images-1.medium.com/max/1000/1*ql2ZxrS_h8D7KHNCrGndug.png)



![img](https://cdn-images-1.medium.com/max/1000/1*JDAuBt3aS9mz3aQQ7JKYKA.png)


### [What is the meaning of latent space?](https://www.quora.com/What-is-the-meaning-of-latent-space)

- 「latent」means 「hidden」
- the 「latent space」is the space where your features lie.
