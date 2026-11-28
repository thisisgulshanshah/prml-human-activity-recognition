# PRML Project: Human Activity Recognition (HAR)

**Course:** Pattern Recognition & Machine Learning (PRML)  
**Team Members:**
- Rudransh Mishra (25AI1019)
- Sahitya Panwar (25AI1042)
- Gulshan Kumar Shah (25AI1019)  
**Institute:** Gati Shakti Vishwavidyalaya, Vadodara (B.Tech AI&DS, 3rd Sem)  
**Dataset:** UCI Human Activity Recognition with Smartphones (Kaggle version)

## 📊 Project Overview

This project implements a complete ML pipeline for **multiclass classification** of human activities using smartphone sensor data.

- **Samples:** 10,299 (7,352 train / 2,947 test)
- **Features:** 561 sensor features (accelerometer, gyroscope)
- **Classes:** 6 activities
  - WALKING
  - WALKING_UPSTAIRS
  - WALKING_DOWNSTAIRS
  - SITTING
  - STANDING
  - LAYING

## 🏗️ Project Structure

```
AIML-PROJECT/
├── data/
│   ├── train.csv          # Training data (to be added)
│   ├── test.csv           # Test data (to be added)
│   └── processed_data.pkl # Generated after EDA
├── notebooks/
│   ├── 01_eda.ipynb       # Exploratory Data Analysis
│   ├── 02_clustering.ipynb # K-Means & DBSCAN
│   └── 03_modeling.ipynb  # Classification models & ensembles
├── src/
│   └── streamlit_app.py   # Interactive demo app
├── models/
│   ├── clustering_results.pkl
│   └── modeling_results.pkl
├── presentation/
│   └── (generated plots)
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Add Data
Place `train.csv` and `test.csv` in the `data/` folder.

The dataset should have:
- 561 feature columns + 1 target column (activity)
- Train: 7,352 rows
- Test: 2,947 rows

Or download automatically:
```bash
python download_data.py
```

### 3. Run Notebooks (in order)
```bash
# Start Jupyter
jupyter notebook notebooks/

# Run in order:
# 1. 01_eda.ipynb
# 2. 02_clustering.ipynb
# 3. 03_modeling.ipynb
# 4. 04_pca_feature_selection.ipynb
# 5. 05_ensemble_evaluation.ipynb
```

### 4. Launch Demo
```bash
streamlit run src/streamlit_app.py
```

## 📈 ML Pipeline

### 1. Exploratory Data Analysis
- Class distribution analysis
- Feature statistics
- Correlation analysis (sample)
- Missing value check

### 2. Unsupervised Learning
- **K-Means:** Elbow method + Silhouette score for optimal K
- **DBSCAN:** K-distance graph for eps tuning
- Cluster visualization with PCA

### 3. Supervised Learning

#### Baseline Models (All 561 Features)
| Model | Type |
|-------|------|
| Naive Bayes | GaussianNB |
| Logistic Regression | Multiclass, max_iter=2000 |
| SVM | RBF & Polynomial kernels |
| Decision Tree | Gini criterion |
| KNN | k=1,3,5 + Weighted (distance) |
| Random Forest | 100 estimators |
| AdaBoost | 100 estimators |

#### Feature Selection
- **Random Forest feature importance** (Gini-based): k=50,100,150,200,300
- **RFE** (Recursive Feature Elimination) with Random Forest

#### PCA
- 95% variance retention
- Model comparison on PCA features
- Logistic Regression comparison across all features, RF top 100, RFE top 100 and PCA, with fold-local preprocessing.

#### Evaluation
- **Stratified 5-Fold Cross-Validation**
- Metrics: Accuracy, Precision (macro), Recall (macro), F1 (macro)
- Confusion Matrix

#### Ensembles
- **Hard Voting:** Majority class voting
- **Soft Voting:** Average predicted probabilities
- Both voting ensembles include Logistic Regression alongside the existing estimators.

## 📊 Expected Results

The pipeline generates:
1. EDA visualizations → `presentation/`
2. Clustering comparison plots
3. Model performance tables (CV + Test)
4. Confusion matrix for best model
5. Trained models saved in `models/`
6. Interactive Streamlit demo

## 🎯 Endsem Topics Covered

- ✅ Error vs Complexity, Bias-Variance Tradeoff
- ✅ Overfitting/Underfitting
- ✅ Naive Bayes (Gaussian)
- ✅ SVM (Max margin, RBF/Poly kernels, Primal/Dual)
- ✅ Decision Tree (Gini, Information Gain)
- ✅ KNN & Weighted KNN
- ✅ Ensembles (Bagging, Random Forest, AdaBoost, Hard/Soft Voting)
- ✅ PCA
- ✅ K-Means (Elbow, Silhouette)
- ✅ DBSCAN

## 📝 Presentation (12 Slides)

1. Problem Statement
2. Motivation
3. Dataset
4. Approaches: Unsupervised & Feature Engineering
5. Approaches: Evaluation & Ensemble Methods
6. Complete Pipeline
7. Experimental Results: Feature Impact
8. Experimental Results: CV & Ensembles
9. Challenges Faced
10. Major Learnings
11. Live Demo & GitHub Link
12. Thank You & Q&A

## 🔗 Links

- **GitHub:** [Add your repo link]
- **Demo:** Run `streamlit run src/streamlit_app.py`
- **Dataset:** [UCI HAR Dataset](https://archive.ics.uci.edu/ml/datasets/human+activity+recognition+using+smartphones)

## 📄 License

Academic project for PRML course.

Logistic Regression evaluation results and plots are generated when the updated notebooks are executed; no new accuracy values are asserted here.
