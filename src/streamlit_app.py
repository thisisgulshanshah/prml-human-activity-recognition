import os
import streamlit as st
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# Set layout
st.set_page_config(
    page_title="Human Activity Recognition | PRML Console",
    page_icon="🏃",
    layout="wide"
)

# Robust path handling
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'processed_data.pkl')
MODELS_PATH = os.path.join(PROJECT_ROOT, 'models', 'final_evaluation_results.pkl')
PLOTS_DIR = os.path.join(PROJECT_ROOT, 'presentation')

st.title("🏃 Human Activity Recognition (HAR) — PRML Demo Console")
st.markdown("### Multiclass Classification & Latent Space Decomposition")
st.markdown("`Team: Gulshan Kumar Shah` | `Dataset: UCI HAR (10,299 Samples, 561 Features, 6 Classes)`")
st.markdown("---")

@st.cache_resource
def load_data_and_models():
    if not os.path.exists(DATA_PATH):
        return None, None
    data = joblib.load(DATA_PATH)
    results = None
    if os.path.exists(MODELS_PATH):
        results = joblib.load(MODELS_PATH)
    return data, results

data, results = load_data_and_models()

if data is None:
    st.warning("⚠️ Processed dataset not found! Please run `notebooks/01_eda_detailed.ipynb` first to generate `data/processed_data.pkl`.")
else:
    X_train, y_train, X_test, y_test = data

    tab1, tab2, tab3, tab4 = st.tabs([
        "🎲 Live Activity Classifier",
        "📊 Benchmark Comparison",
        "🔬 Latent Feature Space",
        "📑 Presentation & Slides"
    ])

    # TAB 1: Live Interactive Inference
    with tab1:
        st.subheader("🎯 Real-Time Sensor Sample Inference")
        st.write("Pick a test sample from the holdout dataset (2,947 unseen observations) and run real-time inference.")

        col_ctrl, col_info = st.columns([1, 2])
        with col_ctrl:
            sample_idx = st.slider("Select Sample Index (0 to 2,946)", 0, len(X_test)-1, 42)
            predict_btn = st.button("🚀 Classify Sensor Sample", type="primary")

        with col_info:
            ground_truth = y_test.iloc[sample_idx]
            st.info(f"**Ground-Truth Activity Label:** `{ground_truth}`")
            st.caption(f"Dimensionality: 561 Triaxial Accelerometer & Gyroscope engineered variables.")

        if predict_btn or True:
            sample_vector = X_test.iloc[sample_idx:sample_idx+1]

            if results and 'champion_model' in results:
                scaler = results['scaler']
                le = results['label_encoder']
                model = results['champion_model']
                model_name = results['champion_name']

                scaled_sample = scaler.transform(sample_vector)
                pred_idx = model.predict(scaled_sample)[0]
                pred_label = le.inverse_transform([pred_idx])[0]

                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    if pred_label == ground_truth:
                        st.success(f"### Predicted: `{pred_label}` ✅\n**Model:** {model_name} (Matches True Label!)")
                    else:
                        st.warning(f"### Predicted: `{pred_label}` ⚠️\n**Model:** {model_name} (Ground Truth: `{ground_truth}`)")

                with res_col2:
                    if hasattr(model, 'predict_proba'):
                        probs = model.predict_proba(scaled_sample)[0]
                        prob_df = pd.DataFrame({'Activity': le.classes_, 'Confidence': probs}).sort_values('Confidence', ascending=False)
                        st.write("**Class Probability Distribution:**")
                        st.bar_chart(prob_df.set_index('Activity'))
            else:
                st.info("💡 Run `notebooks/05_ensemble_evaluation.ipynb` to serialize the trained Champion Ensemble model.")
                st.write("Feature vector preview (First 10 values):")
                st.dataframe(sample_vector.iloc[:, :10])

    # TAB 2: Benchmark Comparison
    with tab2:
        st.subheader("📊 Cross-Validation & Test Benchmarks")
        if results and 'final_table' in results:
            st.dataframe(results['final_table'], use_container_width=True)
        else:
            st.write("Benchmark table will display here once `05_ensemble_evaluation.ipynb` finishes.")

        benchmark_img = os.path.join(PLOTS_DIR, '13_final_ensemble_benchmark.png')
        if os.path.exists(benchmark_img):
            st.image(benchmark_img, caption="Champion Ensemble vs Base Estimators", use_container_width=True)

    # TAB 3: Latent Feature Space (PCA)
    with tab3:
        st.subheader("🔬 2D Latent Space Projection (PCA)")
        pca_img = os.path.join(PLOTS_DIR, '04_pca_latent_space.png')
        if os.path.exists(pca_img):
            st.image(pca_img, caption="561 Features Projected onto Top 2 Principal Components", use_container_width=True)
        else:
            st.info("Run `01_eda_detailed.ipynb` to generate PCA latent space projection visualization.")

    # TAB 4: Presentation & Learning
    with tab4:
        st.subheader("📑 12-Slide Endsem Presentation Summary")
        slides_path = os.path.join(PROJECT_ROOT, 'presentation', 'slides_content.md')
        if os.path.exists(slides_path):
            with open(slides_path, 'r') as f:
                st.markdown(f.read())
        else:
            st.write("Slide content file available in `presentation/slides_content.md`")
