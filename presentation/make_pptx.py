import os
import sys

try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
except ImportError:
    print("Installing python-pptx...")
    os.system(f"{sys.executable} -m pip install python-pptx")
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color constants
C_DARK = RGBColor(15, 23, 42)
C_BLUE = RGBColor(56, 189, 248)
C_WHITE = RGBColor(248, 250, 252)
C_MUTED = RGBColor(148, 163, 184)

def set_slide_bg(slide):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = C_DARK

def add_header(slide, title_text, slide_num):
    txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.8))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = C_BLUE

    # Slide tag
    tagBox = slide.shapes.add_textbox(Inches(11.0), Inches(0.4), Inches(1.5), Inches(0.5))
    tagP = tagBox.text_frame.paragraphs[0]
    tagP.text = f"Slide {slide_num:02d}/12"
    tagP.font.size = Pt(12)
    tagP.font.color.rgb = C_MUTED

# Slide data definition
slides_data = [
    {
        "title": "Human Activity Recognition with Smartphones",
        "bullets": [
            "PRML End-Semester Capstone Project",
            "Core Objective: Multiclass classification of 6 physical human activities using mobile sensor streams.",
            "High-Dimensional Challenge: 561 engineered triaxial features from accelerometer & gyroscope.",
            "Pipeline: Complete workflow from raw sensor ingestion to champion voting ensemble.",
            "Team: Rudransh Mishra (25AI1019) | Sahitya Panwar (25AI1042) | Gulshan Kumar Shah (25AI1019)",
            "Institute: Gati Shakti Vishwavidyalaya, Vadodara (B.Tech AI&DS, 3rd Sem)"
        ],
        "image": "01_class_distribution.png"
    },
    {
        "title": "Motivation & Theoretical Foundations",
        "bullets": [
            "Pervasive Healthcare: Contactless monitoring for elderly care, ambulatory rehabilitation, and fall detection.",
            "Curse of Dimensionality: Navigating severe multicollinearity in 561 sensor dimensions without overfitting.",
            "Bias-Variance Tradeoff: Evaluating linear baselines vs non-linear kernel SVM vs variance-reducing ensembles.",
            "PRML Topics Implemented: Naive Bayes, Decision Trees, KNN, Random Forest, AdaBoost, PCA, K-Means, DBSCAN."
        ],
        "image": "02_feature_breakdown.png"
    },
    {
        "title": "Dataset Anatomy & Profiling (UCI HAR)",
        "bullets": [
            "Source: UCI Machine Learning Repository / Kaggle Dataset Benchmark.",
            "Sample Count: 10,299 total samples partitioned into 7,352 Train (71.4%) and 2,947 Test (28.6%).",
            "Classes: WALKING, WALKING_UPSTAIRS, WALKING_DOWNSTAIRS, SITTING, STANDING, LAYING.",
            "Feature Engineering: 50Hz triaxial signals passed through Butterworth and median filters into 561 features."
        ],
        "image": "03_dynamic_vs_static.png"
    },
    {
        "title": "Unsupervised Cluster Discovery",
        "bullets": [
            "K-Means Optimization: Elbow Method & Silhouette coefficient verified natural cluster partition at k=6.",
            "Adjusted Rand Index (ARI): 0.448 against ground-truth labels.",
            "Normalized Mutual Information (NMI): 0.562.",
            "DBSCAN Density Clustering: Calibrated using k-distance graph (eps=15.0, min_samples=5) isolating core densities."
        ],
        "image": "08_clustering_comparison.png"
    },
    {
        "title": "Validation Protocol & Ensemble Theory",
        "bullets": [
            "Stratified 5-Fold Cross-Validation: Eliminates sampling bias across imbalanced activity folds.",
            "Evaluation Metrics: Balanced Accuracy, Macro Precision, Macro Recall, and Macro F1-Score.",
            "Hard Voting Ensemble: Majority consensus voting across top base classifiers.",
            "Soft Voting Ensemble: Sum of calibrated posterior class probabilities argmax(Sum P(y|x))."
        ],
        "image": "06_kmeans_elbow_silhouette.png"
    },
    {
        "title": "Complete System Architecture",
        "bullets": [
            "Stage 1: Sensor data loading, missing value audit (0 nulls), feature normalization.",
            "Stage 2: Unsupervised spatial clustering (K-Means k=6 and DBSCAN).",
            "Stage 3: Feature selection (SelectKBest ANOVA) & PCA compression (95% variance).",
            "Stage 4: Stratified 5-Fold Cross-Validation benchmark across 11 classifiers.",
            "Stage 5: Production Streamlit console for interactive test sample inference."
        ],
        "image": "04_pca_latent_space.png"
    },
    {
        "title": "Experimental Results: Compression Trade-Off",
        "bullets": [
            "All 561 Features Baseline: 96.25% Cross-Validation Accuracy.",
            "SelectKBest (ANOVA F-statistic): 100 Features achieves 95.80% Acc (82.2% reduction in features!).",
            "PCA (95% Variance Threshold): 102 Components achieves 95.40% Acc (81.8% reduction!).",
            "Inference Speedup: Model inference accelerated by ~4.8x on mobile hardware."
        ],
        "image": "12_feature_selection_vs_pca.png"
    },
    {
        "title": "Experimental Results: Test Benchmark & Ensembles",
        "bullets": [
            "Champion: Soft Voting Ensemble achieves 96.84% Test Accuracy & 96.88% Macro F1.",
            "Hard Voting Ensemble: 96.71% Test Accuracy.",
            "Best Individual Model: SVM with RBF Kernel (C=10) achieves 96.54% Test Accuracy.",
            "Random Forest: 92.84% | Weighted KNN: 90.74% | AdaBoost: 53.38%."
        ],
        "image": "13_final_ensemble_benchmark.png"
    },
    {
        "title": "Engineering Challenges & Solutions",
        "bullets": [
            "High Dimensionality & Multicollinearity: Severe feature correlation resolved via orthogonal PCA & ANOVA.",
            "Static Posture Ambiguity: Sitting vs Standing exhibits identical gravitational vector; resolved via non-linear SVM RBF.",
            "DBSCAN Distance Concentration: High dimensional Euclidean metric tuned via k-distance knee inflection.",
            "Computational Scalability: Parallelized multi-core training across 5 folds."
        ],
        "image": "10_best_model_confusion_matrix.png"
    },
    {
        "title": "Major Learnings & Conclusions",
        "bullets": [
            "Kernel Power: SVM RBF significantly outperforms linear models (96.5% vs 78%), proving non-linear manifold geometry.",
            "Ensemble Variance Reduction: Soft Voting successfully reduces classification variance and achieves 96.88% F1.",
            "Dimensionality Reduction Efficiency: 82% of sensor bandwidth can be discarded with <0.5% drop in accuracy.",
            "End-to-End Delivery: Complete mastery of pipeline from raw sensor data to interactive demo."
        ],
        "image": "14_champion_confusion_matrix.png"
    },
    {
        "title": "Live Demonstration & Public Repository",
        "bullets": [
            "Public GitHub Repository: https://github.com/thisisgulshanshah/prml-human-activity-recognition",
            "Interactive Streamlit Console: Live test sample prediction and probability gauge.",
            "Automated Reproducibility: 'python download_data.py' fetches official UCI repository data.",
            "Documentation: Full lab report, notebooks 01-05, and presentation figures included."
        ],
        "image": "04_pca_latent_space.png"
    },
    {
        "title": "Thank You & Project Team",
        "bullets": [
            "Team Members:",
            "  • Rudransh Mishra (25AI1019)",
            "  • Sahitya Panwar (25AI1042)",
            "  • Gulshan Kumar Shah (25AI1019)",
            "Program: B.Tech Artificial Intelligence & Data Science | Semester 3",
            "Course: Pattern Recognition & Machine Learning (PRML)",
            "Institute: Gati Shakti Vishwavidyalaya, Vadodara",
            "Questions and Discussion Welcome!"
        ],
        "image": "01_class_distribution.png"
    }
]

blank_layout = prs.slide_layouts[6]

for idx, data in enumerate(slides_data, 1):
    slide = prs.slides.add_slide(blank_layout)
    set_slide_bg(slide)
    add_header(slide, data["title"], idx)

    # Left text box
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(6.5), Inches(5.2))
    tf = tb.text_frame
    tf.word_wrap = True

    for i, bullet in enumerate(data["bullets"]):
        p = tf.add_paragraph() if i > 0 else tf.paragraphs[0]
        p.text = bullet
        p.font.size = Pt(15)
        p.font.color.rgb = C_WHITE if not bullet.startswith("  •") else C_BLUE
        p.space_after = Pt(10)
        p.level = 1 if bullet.startswith("  •") else 0

    # Right image box if exists
    img_path = os.path.join(BASE_DIR, data["image"])
    if os.path.exists(img_path):
        slide.shapes.add_picture(img_path, Inches(7.6), Inches(1.6), width=Inches(5.0))

output_path = os.path.join(BASE_DIR, "presentation.pptx")
prs.save(output_path)
print(f"✅ Generated PowerPoint deck successfully: {output_path}")
