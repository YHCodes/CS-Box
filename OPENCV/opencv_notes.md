

#### Smoothing Images


#### Eroding and Dilating
最常用的两种形态学操作: Erosion(侵蚀) 、Dilation(扩大, 膨胀)

作用 :
- Removing noise
- Isolation of individual elements and joining disparate elements in an image.
- Finding of intensity bumps or holes in an image

区别:
- Dilation
    - computes a **local maximum** over the area of given kernel.
- Erosion
    - computes a **local minimum** over the area of given kernel.




#### More Morphology Transformations

**1. Opening** :  Useful for removing small objects (it is assumed that the objects are bright on a dark foreground)

**2. Closing**: Useful to remove small holes (dark regions).

**3. Morphological Gradient** : Useful for finding the outline of an object

**4. Top Hat** : It is the difference between an input image and its opening.

**5. Black Hat** : It is the difference between the closing and its input image

