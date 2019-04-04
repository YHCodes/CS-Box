[TOC]

# Mathematical Expression Detection and Segmentation in Document Images



## Inbox

> Basically, our goal is to organize the world's information and to make it universally accessible and useful. 



### 2.2.1 Text Line Finding

- **Horizontal Projection Profile**
  - 是用来确定文本图片倾斜角度的最简单的方法
  - 当文本的倾斜角度为0时，水平投影的向量是最大振幅和频率 (maximum amplitude and frequency)，because the number of co-linear black pixels is maximized in this condition.
- **Hough Transform**
  - 特征提取技术
  - 检测：1）文本图片的倾斜角度 2）检测任何数学上易处理的形状
- **Geometric Distribution of Connected Components**
- **Curved Text Line Detection**



### 2.3.2 Preprocessing

#### Noise Removal: Dealing with Half-tones

#### Background and Foreground Separation 

- use thresholding techniques like Otsu's method 
-  find the outline of characters through edge detection



### 2.3.3 Document Structure Analysis 

#### Document Physical Structure Analysis 

- **Top-Down Physical Structure Analysis** 
  - X-Y Cut Algorithm
  - Run-Length Smoothing Algorithm (RLSA).
  - Template Techniques
- **Bottom-Up Physical Structure Analysis**
  - Connected Component Analysis
  - Document Spectrum Analysis (“Docstrum”). 
  - Voronoi Diagram
  - Run Length Smearing Algorithm (RLSA). 
  - Multiresolution Morophology
- **Hybrid Physical Structure Analysis** 
  - Shape-directed Cover Algorithm
  - White space cover algorithm by Breuel
  - OCRopus Open Source OCR System
  - Tesseract Layout Analysis Module
- **Document Logical Structure Analysis **
  - Page Classification 
  - Zone Classification 
  - Type-specific Classification
    - Mathematical Expression Detection



## 3 Method 

P90



**Merge Decision**:

- **Vertical Merges.**
- **Horizontal Merges.**





### 3.4 Component Design 

#### 3.4.1 Groundtruth Dataset Generation 

#### 3.4.2 MEDS Module



