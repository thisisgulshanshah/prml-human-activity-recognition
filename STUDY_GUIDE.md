# 📘 PRML Complete Project Study & Viva Guide
## Human Activity Recognition with Smartphones (UCI HAR)

**Team Members:**
- Rudransh Mishra (25AI1019)
- Sahitya Panwar (25AI1042)
- Gulshan Kumar Shah (25AI1019)

**Course:** Pattern Recognition & Machine Learning (PRML)  
**Institute:** Gati Shakti Vishwavidyalaya (GSV), Vadodara  
**Semester:** 3rd Semester, B.Tech AI & Data Science  

---

## 🌟 1. The Big Picture (What is this project in simple words?)

Imagine you have a smartphone in your pocket. As you walk, climb stairs, sit on a chair, stand, or lie down on a bed, the phone's internal sensors (**accelerometer** and **gyroscope**) record motion and rotation 50 times every second.

### The Problem:
Can an AI algorithm look **only** at these sensor numbers and accurately tell what physical activity you were doing?

### The Solution:
We built an end-to-end Machine Learning pipeline that takes 561 statistical sensor features per time window and classifies the person's motion into one of **6 activities**:
1. `WALKING`
2. `WALKING_UPSTAIRS`
3. `WALKING_DOWNSTAIRS`
4. `SITTING`
5. `STANDING`
6. `LAYING`

Our Champion Ensemble model achieves **96.84% accuracy** on 2,947 completely unseen test samples!

---

## 📊 2. The Dataset (UCI HAR)

- **Total Samples:** 10,299 instances
- **Train Split:** 7,352 samples (71.4%)
- **Test Split:** 2,947 samples (28.6%)
- **Number of Features:** 561 numerical features
- **Missing Values:** 0 (Pristine dataset, no missing or null values)
- **Values Range:** All features are pre-normalized between `[-1.0, +1.0]`.

### Where do 561 features come from?
The raw smartphone sensors generate 3D acceleration $(a_x, a_y, a_z)$ and 3D angular velocity $(\omega_x, \omega_y, \omega_z)$.
Engineers separated these into:
1. **Body motion** (caused by human movement)
2. **Gravity component** (constant downward gravitational pull)

From these signals, mathematical functions were calculated over sliding time windows of 2.56 seconds:
- **Time domain features** (start with `t`): Mean, standard deviation, max, min, signal magnitude area (SMA), entropy, auto-regression coefficients.
- **Frequency domain features** (start with `f`, calculated via Fast Fourier Transform / FFT): Energy bands, frequency skewness, kurtosis, spectral peak coordinates.

Total combinations $= 561$ features!

---

## 🔬 3. The ML Pipeline Step-by-Step

### 📍 Step 1: Exploratory Data Analysis (EDA)
**Notebook:** `notebooks/01_eda_detailed.ipynb`

- **Class Balance:** We plotted the histogram of the 6 classes. Each class has roughly 1,000 to 1,400 samples. It is well-balanced, meaning no class is ignored.
- **Dynamic vs Static Split:**
  - *Dynamic* (Walking, Upstairs, Downstairs): High acceleration variance and energy.
  - *Static* (Sitting, Standing, Laying): Near-zero acceleration variance; gravity vector dominates.
- **Multicollinearity:** Many sensor features have a correlation $r > 0.90$. If two sensors measure the same movement, their data is redundant. This proves why **Dimensionality Reduction** is necessary!

---

### 📍 Step 2: Unsupervised Learning (Clustering)
**Notebook:** `notebooks/02_clustering.ipynb`
*Requirement from Professor: "K-Means (find best k) and DBSCAN"*

#### A. K-Means Clustering
- **What it does:** Groups unlabeled data points into $k$ clusters based on Euclidean distance to cluster centroids.
- **Finding Optimal $k$:**
  1. **Elbow Method:** We plotted inertia (sum of squared distances to closest centroid) for $k=2$ to $10$. An "elbow" inflection appeared at $k=6$.
  2. **Silhouette Score:** Measures how close each point is to its own cluster versus neighboring clusters (ranges from -1 to +1). It confirmed $k=6$ as the natural clustering structure.
- **Cluster Validation:**
  - **Adjusted Rand Index (ARI) = 0.448**: Measures cluster similarity against true activity labels, corrected for chance.
  - **Normalized Mutual Information (NMI) = 0.562**: Information shared between clusters and true labels.

#### B. DBSCAN (Density-Based Spatial Clustering of Applications with Noise)
- **What it does:** Groups points in dense regions and labels outliers/isolated points as noise (-1).
- **Tuning `eps` (Epsilon):** We plotted the **5-NN distance graph** (distance of every point to its 5th nearest neighbor sorted in ascending order). The "knee" of the curve identified $\varepsilon = 15.0$ and `min_samples = 5`.
- **Finding:** In 561 dimensions, Euclidean distances concentrate (curse of dimensionality). DBSCAN detected core clusters and isolated sensor noise.

---

### 📍 Step 3: Feature Selection & PCA (Dimensionality Reduction)
**Notebook:** `notebooks/04_pca_feature_selection.ipynb`
*Requirement from Professor: "Model with all features, then feature selection, then PCA model"*

| Approach | Features Count | CV Accuracy | Key Takeaway |
|---|---|---|---|
| **All Features (Baseline)** | 561 | **96.25%** | Baseline accuracy, but slow training |
| **SelectKBest (ANOVA F-test)** | 100 | **95.80%** | **82.2% reduction in features** with only 0.45% accuracy drop! |
| **PCA (95% Variance)** | 102 | **95.40%** | **81.8% compression**, eliminates multicollinearity |

- **SelectKBest:** Computes ANOVA F-statistic between each individual feature and the target class, keeping only the top 100 most informative features.
- **PCA (Principal Component Analysis):** Finds orthogonal eigenvectors (axes of maximum variance). The first 102 components capture 95% of all information in the original 561 features!
- **Engineering Advantage:** Using 100 features speeds up prediction time by ~5×, making it possible to run smoothly on a smartwatch or phone battery.

---

### 📍 Step 4: Supervised Learning (11 Models Benchmarked)
**Notebook:** `notebooks/03_modeling.ipynb`
*Evaluated using Stratified 5-Fold Cross-Validation*

1. **Gaussian Naive Bayes (78.3%):** Assumes features are independent given the class. Drops in performance because sensor features are highly correlated.
2. **Decision Tree (87.2%):** Uses Gini Impurity to split data recursively. Fast, but prone to high variance (overfitting).
3. **KNN ($k=1, 3, 5$):**
   - $k=1$: 90.1% (Sensitive to noisy outliers)
   - $k=3$: 91.2%
   - $k=5$: 91.5%
4. **Weighted KNN ($k=3, 5$) (92.4%):** Weights neighbors inversely by distance $w_i = \frac{1}{d(x, x_i)}$. Gives closer neighbors more voting power, beating standard KNN!
5. **Random Forest (93.8%):** Ensemble of 100 decision trees trained on random subsets of data and features (Bagging). Reduces variance without increasing bias.
6. **AdaBoost (54.1%):** Iteratively adjusts weights of misclassified samples. Sensitive to noisy multiclass sensor data.
7. **SVM (RBF Kernel) (96.5% - Best Individual Model!):** Uses the Kernel Trick $K(x, x') = \exp(-\gamma ||x - x'||^2)$ to project non-linear boundaries into infinite dimensions and find the maximum margin hyperplane.

---

### 📍 Step 5: Ensemble Architectures (Hard vs Soft Voting)
**Notebook:** `notebooks/05_ensemble_evaluation.ipynb`
*Requirement from Professor: "Hard Voting, Soft Voting vs Individual Models"*

We combined the top 4 diverse classifiers:
1. SVM (RBF Kernel)
2. Random Forest (100 Trees)
3. Weighted KNN ($k=5$)
4. AdaBoost

#### Hard Voting (96.71% Test Accuracy)
- Each model outputs a single class label.
- The ensemble picks the class with the **majority of votes**:
  $$\hat{y} = \text{mode}\{C_1(x), C_2(x), C_3(x), C_4(x)\}$$

#### Soft Voting (96.84% Test Accuracy — CHAMPION 🏆)
- Each model outputs class probabilities ($P(\text{Walking}), P(\text{Sitting}), \dots$).
- The ensemble sums the probabilities and picks the argmax:
  $$\hat{y} = \arg\max \sum_{i=1}^M P_i(y = c \mid x)$$
- **Why Soft Voting won:** If SVM is 95% confident of "Sitting" and two weaker models barely vote for "Standing" with 51% confidence, Soft Voting trusts the high-confidence SVM prediction!

---

### 📍 Step 6: Final Test Set Evaluation (2,947 Unseen Samples)

| Metric | Champion Value | Meaning |
|---|---|---|
| **Test Accuracy** | **96.84%** | Out of 2,947 unseen test tests, 2,854 were predicted correctly! |
| **Macro Precision** | **96.95%** | When the model predicts an activity, it is right 97% of the time. |
| **Macro Recall** | **96.82%** | Out of all actual activities performed, 97% were caught. |
| **Macro F1-Score** | **96.88%** | Harmonic mean of precision and recall across all 6 classes. |

---

## 👥 4. Team Presentation Strategy (Who Speaks on What?)

Divide the 12 slides among the 3 team members so everyone looks confident and well-prepared:

### 👤 Member 1: Gulshan Kumar Shah (Slides 1 to 4)
- **Slide 1:** Problem Statement & Project Goals
- **Slide 2:** Motivation, Real-world Healthcare Applications, PRML Syllabus Connections
- **Slide 3:** Dataset Characteristics (10,299 samples, 561 features, sensor anatomy)
- **Slide 4:** Unsupervised Learning (K-Means optimal $k=6$, Elbow & Silhouette, DBSCAN $\varepsilon$ tuning)

### 👤 Member 2: Rudransh Mishra (Slides 5 to 8)
- **Slide 5:** Evaluation Strategy (Stratified 5-Fold Cross-Validation, Metrics)
- **Slide 6:** Complete 5-Stage System Pipeline Architecture
- **Slide 7:** Dimensionality Reduction Results (All 561 Features vs SelectKBest 100 vs PCA 95% Variance)
- **Slide 8:** Supervised Models Benchmark (SVM vs Random Forest vs KNN vs AdaBoost)

### 👤 Member 3: Sahitya Panwar (Slides 9 to 12)
- **Slide 9:** Engineering Challenges Overcome (Multicollinearity, Static posture ambiguity, High-D DBSCAN)
- **Slide 10:** Major Theoretical Learnings (Kernel trick, Bias-Variance tradeoff, Ensemble variance reduction)
- **Slide 11:** Live Demonstration on Streamlit & Public GitHub Repository
- **Slide 12:** Summary, Conclusion & Answering Professor's Questions

---

## ❓ 5. Professor's Expected Questions & Exact Answers

### Q1: "Why did you choose this dataset over common ones like Iris or Titanic?"
> *"Sir, most benchmark datasets in college labs have fewer than 10 features. The UCI HAR dataset has 561 features and 10,299 rows. This allowed us to practically test **the curse of dimensionality**, compare **filter feature selection against PCA**, and observe how complex non-linear models behave on real-world high-dimensional sensor data."*

### Q2: "Why did SVM with RBF Kernel beat Decision Trees and Naive Bayes?"
> *"Sir, Naive Bayes assumes independent features, which failed because triaxial sensor data is heavily correlated. Decision Trees create orthogonal axis-aligned splits, which struggle with continuous motion boundaries. SVM with RBF projects the 561-D data into a reproducing kernel Hilbert space to find the optimal maximum-margin hyperplane that separates non-linear motion vectors."*

### Q3: "What is the difference between Hard Voting and Soft Voting in your ensemble?"
> *"Sir, Hard Voting is majority rule: each classifier casts 1 integer vote. Soft Voting sums the predicted posterior probabilities across all models and chooses the highest average probability. Soft Voting performed better (96.84% vs 96.71%) because it accounts for model confidence."*

### Q4: "How did you prove that $k=6$ is optimal in K-Means without cheating from the labels?"
> *"Sir, in Notebook 02, we hid all class labels and ran K-Means purely unsupervised for $k \in [2, 10]$. We plotted the **Inertia Elbow curve** and computed **Silhouette Coefficients**. Both diagnostics confirmed an optimal inflection point at $k=6$, proving that the sensor data naturally clusters into the 6 physical activity patterns."*

### Q5: "Why did you use Stratified K-Fold instead of standard K-Fold?"
> *"Sir, in standard K-Fold, random splitting can cause certain folds to have fewer samples of minority classes (like Walking Downstairs). Stratified K-Fold guarantees that every single fold preserves the exact 6-class percentage distribution, eliminating evaluation bias."*

### Q6: "Why did PCA need 102 components for 95% variance?"
> *"Sir, because sensor signals across 3 axes contain both high-frequency noise and redundant correlations. The top 102 principal components capture 95% of total signal energy while discarding the remaining 459 noisy dimensions. This reduces model complexity by ~82% while keeping accuracy above 95.4%."*
