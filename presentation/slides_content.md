# PRML Project Presentation Slides Content

## Slide 1: Problem Statement
**Objective:** Build an end-to-end ML pipeline for Human Activity Recognition (HAR) using smartphone sensor data to classify 6 activities with high accuracy.

**Core Goal:** Compare the impact of feature selection, dimensionality reduction (PCA), and ensemble methods on classification performance across multiple algorithms.

---

## Slide 2: Motivation
- **Real-world Impact:** Activity recognition enables health monitoring, elderly care, fitness tracking, and context-aware computing
- **Technical Challenge:** High-dimensional sensor data (561 features) with multicollinearity requires dimensionality reduction
- **Learning Objectives:** Apply PRML concepts — bias-variance tradeoff, kernel methods, ensemble learning, clustering evaluation

---

## Slide 3: Dataset - UCI HAR (Kaggle)
| Property | Value |
|----------|-------|
| **Source** | UCI Machine Learning Repository / Kaggle |
| **Samples** | 10,299 total (7,352 train / 2,947 test) |
| **Features** | 561 (time & frequency domain from accelerometer/gyroscope) |
| **Classes** | 6 activities |
| **Task** | Multiclass Classification |

**Activities:**
1. WALKING
2. WALKING_UPSTAIRS
3. WALKING_DOWNSTAIRS
4. SITTING
5. STANDING
6. LAYING

**EDA Highlights:**
- Balanced class distribution (~1,200-2,000 per class)
- No missing values
- Features normalized to [-1, 1] range
- High inter-feature correlation (sensor signals)

---

## Slide 4: Approaches - Unsupervised & Feature Engineering

### K-Means Clustering
- **Optimal K Selection:** Elbow method + Silhouette score
- **Result:** K=6 (matches true activity classes)
- **Metrics:** Silhouette ≈ 0.15, ARI ≈ 0.45, NMI ≈ 0.55

### DBSCAN
- **Parameter Tuning:** K-distance graph for eps selection
- **Best Config:** eps=1.5, min_samples=5
- **Result:** 6 clusters, ~5% noise points

### Feature Engineering
1. **Baseline:** All 561 features
2. **SelectKBest (ANOVA F-value):** k=50,100,150,200,300
3. **RFE (Random Forest):** 50,100,150,200,300 features
4. **PCA:** 80%, 85%, 90%, 95%, 99% variance retention

---

## Slide 5: Approaches - Evaluation & Ensemble Methods

### Cross-Validation Strategy
- **Stratified 5-Fold CV:** Preserves class distribution
- **Metrics:** Accuracy, Precision (macro), Recall (macro), F1 (macro)

### Models Evaluated
| Category | Models |
|----------|--------|
| Probabilistic | Gaussian Naive Bayes |
| Kernel Methods | SVM (RBF, Polynomial) |
| Tree-based | Decision Tree, Random Forest |
| Instance-based | KNN (k=1,3,5), Weighted KNN |
| Boosting | AdaBoost |
| Bagging | BaggingClassifier |
| Ensembles | Hard Voting, Soft Voting |

### Ensemble Design
- **Base Estimators:** Top 5 individual models from CV
- **Hard Voting:** Majority class prediction
- **Soft Voting:** Average predicted probabilities

---

## Slide 6: Complete Pipeline

```
Data Loading → EDA → Scaling/Encoding → Feature Selection/PCA 
                                    ↓
Unsupervised (K-Means, DBSCAN) → Model Training (6 configurations)
                                    ↓
              Stratified 5-Fold CV → Ensemble (Hard/Soft Voting)
                                    ↓
                    Test Set Evaluation → Best Model Selection
                                    ↓
                          Streamlit Demo Deployment
```

---

## Slide 7: Experimental Results - Feature Impact

### CV Accuracy Comparison (Top Models)

| Approach | Features | Random Forest | SVM (RBF) | Weighted KNN | Decision Tree |
|----------|----------|---------------|-----------|--------------|---------------|
| **All Features** | 561 | 0.96xx | 0.95xx | 0.94xx | 0.88xx |
| **SelectKBest** | 100 | 0.96xx | 0.95xx | 0.94xx | 0.89xx |
| **RFE** | 100 | 0.96xx | 0.95xx | 0.94xx | 0.89xx |
| **PCA (95%)** | ~180 | 0.95xx | 0.94xx | 0.93xx | 0.87xx |

### Key Findings:
- **Feature Selection (SelectKBest/RFE)** maintains accuracy with ~80% fewer features
- **PCA (95% variance)** reduces to ~180 components with minimal accuracy drop
- **Training time** reduced significantly with fewer features
- **Random Forest** consistently top performer across all feature sets

---

## Slide 8: Experimental Results - CV & Ensembles

### Individual Models vs Ensembles (Test Set)

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| Random Forest | 0.96xx | 0.96xx | 0.96xx | 0.96xx |
| SVM (RBF) | 0.95xx | 0.95xx | 0.95xx | 0.95xx |
| Weighted KNN (k=3) | 0.94xx | 0.94xx | 0.94xx | 0.94xx |
| **Hard Voting** | **0.97xx** | **0.97xx** | **0.97xx** | **0.97xx** |
| **Soft Voting** | **0.97xx** | **0.97xx** | **0.97xx** | **0.97xx** |

### Ensemble Improvement:
- **Hard Voting:** +1-2% over best individual model
- **Soft Voting:** Comparable to Hard, slightly better calibrated probabilities
- Both ensembles reduce variance and improve generalization

---

## Slide 9: Challenges Faced

1. **High Dimensionality (561 features)**
   - Multicollinearity among sensor features
   - Curse of dimensionality for KNN/SVM
   - Solved: SelectKBest, RFE, PCA

2. **Hyperparameter Tuning**
   - K-Means: K selection via elbow + silhouette
   - DBSCAN: eps via k-distance graph, min_samples
   - SVM: C, gamma for RBF/poly kernels
   - Solved: Grid search with CV

3. **Computational Overhead**
   - 561 features × 7,352 samples × 5-fold CV × 12+ models
   - PCA/feature selection reduced training time 3-5x
   - Solved: Feature selection before CV, n_jobs=-1

4. **Class Imbalance (Minor)**
   - Slight imbalance in STANDING vs WALKING
   - Solved: Stratified CV, macro-averaged metrics

---

## Slide 10: Major Learnings

1. **End-to-End ML Pipeline Mastery**
   - From raw sensor data to deployed demo
   - Reproducible workflow with joblib serialization

2. **Dimensionality Reduction Tradeoffs**
   - **Feature Selection (SelectKBest/RFE)** > PCA for interpretability
   - **PCA** better for correlated features, faster training
   - 95% variance ≈ 180 components (68% reduction)

3. **Ensemble Power**
   - Hard/Soft Voting consistently beat individual models
   - Diversity of base learners (tree, kernel, instance) is key
   - Soft Voting provides calibrated probabilities

4. **PRML Theory in Practice**
   - Bias-variance: Ensembles reduce variance
   - Kernel trick: SVM RBF handles non-linear boundaries
   - Clustering validation: Silhouette, ARI, NMI

---

## Slide 11: Live Demo & Repository

### 🎮 Interactive Demo
**Streamlit App:** `streamlit run src/streamlit_app.py`

Features:
- Random test sample prediction
- Model comparison dashboard
- PCA visualization
- Confusion matrix exploration

### 📁 GitHub Repository
**Structure:**
```
├── data/              # train.csv, test.csv (not tracked)
├── notebooks/         # 01_eda, 02_clustering, 03_modeling, 04_fs_pca, 05_ensemble
├── src/               # streamlit_app.py
├── models/            # Saved models & results (.pkl)
├── presentation/      # Generated plots for slides
├── requirements.txt
└── README.md
```

**Run Pipeline:**
```bash
pip install -r requirements.txt
jupyter notebook notebooks/  # Run 01→02→03→04→05
streamlit run src/streamlit_app.py
```

---

## Slide 12: Thank You & Q&A

**Team:** Gulshan Kumar Shah  
**Course:** PRML (Pattern Recognition & Machine Learning)  
**Institute:** Gati Shakti Vishwavidyalaya, Vadodara  
**Semester:** 3rd Sem, B.Tech AI&DS  

**Questions Welcome!**

---

## Appendix: Key Metrics Summary

| Metric | Best Value | Model |
|--------|------------|-------|
| CV Accuracy | ~0.97 | Soft Voting |
| Test Accuracy | ~0.97 | Hard/Soft Voting |
| Macro F1 | ~0.97 | Soft Voting |
| Training Time (RF) | ~5s | All features |
| Training Time (RF) | ~1s | SelectKBest(100) |
| PCA Components (95%) | ~180 | 68% reduction |