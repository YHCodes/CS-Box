# Kalman Filter

Three major components of autonomous driving are 

1. localization (where am I)
2. perception (what is around me)
3. control (how to drive around)



**Sensors**:

| 传感器  | 优点                                                  | 缺点                                                         |
| ------- | ----------------------------------------------------- | ------------------------------------------------------------ |
| Cameras | High Resolution                                       | cannot detect speed and distance easily;  vulnerable to bad weather and environmental factors. |
| LiDAR   | create a nice 3-D map                                 | huge and expensive;  vulnerable to bad weather and environmental factors. |
| RADAR   | works better in bad conditions and detects speed well | low resolution                                               |

> Kalman filter is designed to fuse sensor readings to make more accurate predictions than each individual sensor alone





What is a *Kalman Filter* and What Can It Do?

- A Kalman Filter is an **optimal estimator** - ie infers parameters of interest from indirect, inaccurate and uncertain observations.
- It is **recursive** so that new measurements can be processed as they arrive.




When Kalman filter is explained as a Bayes filter,  the belief is also called **prior** and the final prediction is called **posterior**.

To track a moving car, we repeat a 2-step procedure:

1. **Predict**: Apply a dynamic model to our belief to predict what is next.
2. **Update**: Take a measurement to update our prediction.




### Resource

[kalman basics](http://biorobotics.ri.cmu.edu/papers/sbp_papers/integrated3/kleeman_kalman_basics.pdf)

[我所理解的卡尔曼滤波, 简书](https://www.jianshu.com/p/d3b1c3d307e0)

[meidum](https://medium.com/@jonathan_hui/self-driving-object-tracking-intuition-and-the-math-behind-kalman-filter-657d11dd0a90)

