import json

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# PRML Project: Human Activity Recognition (HAR)\n",
                "## Exploratory Data Analysis - Professional Report\n",
                "\n",
                "---\n",
                "\n",
                "### Dataset Overview\n",
                "| Attribute | Details |\n",
                "|-----------|---------|\n",
                "| Dataset | UCI HAR Dataset (Kaggle version) |\n",
                "| Samples | 10,299 total (7,352 train / 2,947 test) |\n",
                "| Features | 561 sensor features + 1 target |\n",
                "| Target | 6 Activity Classes |\n",
                "| Task | Multiclass Classification |\n",
                "| Sensors | Smartphone Accelerometer + Gyroscope (50Hz) |\n",
                "\n",
                "### Activities\n",
                "1. WALKING\n",
                "2. WALKING_UPSTAIRS\n",
                "3. WALKING_DOWNSTAIRS\n",
                "4. SITTING\n",
                "5. STANDING\n",
                "6. LAYING\n",
                "\n",
                "---\n",
                "\n",
                "## 1. Setup & Data Loading"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import pandas as pd\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "import warnings\n",
                "import joblib\n",
                "import os\n",
                "\n",
                "warnings.filterwarnings('ignore')\n",
                "\n",
                "plt.style.use('seaborn-v0_8-whitegrid')\n",
                "sns.set_palette('husl')\n",
                "pd.set_option('display.max_columns', 100)\n",
                "pd.set_option('display.max_rows', 100)\n",
                "pd.set_option('display.width', 200)\n",
                "pd.set_option('display.float_format', '{:.4f}'.format)\n",
                "\n",
                "activity_colors = {\n",
                "    'WALKING': '#2E86AB',\n",
                "    'WALKING_UPSTAIRS': '#A23B72',\n",
                "    'WALKING_DOWNSTAIRS': '#F18F01',\n",
                "    'SITTING': '#C73E1D',\n",
                "    'STANDING': '#6A994E',\n",
                "    'LAYING': '#7209B7'\n",
                "}\n",
                "\n",
                "print('Environment ready')\n",
                "print(f'Pandas: {pd.__version__}')"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "train_path = '../data/train.csv'\n",
                "test_path = '../data/test.csv'\n",
                "\n",
                "train_df = pd.read_csv(train_path)\n",
                "test_df = pd.read_csv(test_path)\n",
                "\n",
                "print('=' * 60)\n",
                "print('DATASET OVERVIEW')\n",
                "print('=' * 60)\n",
                "print(f'Train shape: {train_df.shape[0]:,} rows x {train_df.shape[1]} columns')\n",
                "print(f'Test shape:  {test_df.shape[0]:,} rows x {test_df.shape[1]} columns')\n",
                "print(f'Target column: {train_df.columns[-1]}')\n",
                "print(f'Feature columns: {train_df.shape[1] - 1} sensor features')\n",
                "print(f'Memory usage: {train_df.memory_usage(deep=True).sum() / 1024**2:.1f} MB')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 2. Data Quality Assessment"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "print('=' * 60)\n",
                "print('DATA QUALITY REPORT')\n",
                "print('=' * 60)\n",
                "\n",
                "train_missing = train_df.isnull().sum().sum()\n",
                "test_missing = test_df.isnull().sum().sum()\n",
                "print(f'Missing values (Train): {train_missing}')\n",
                "print(f'Missing values (Test):  {test_missing}')\n",
                "\n",
                "train_dupes = train_df.duplicated().sum()\n",
                "test_dupes = test_df.duplicated().sum()\n",
                "print(f'Duplicate rows (Train): {train_dupes}')\n",
                "print(f'Duplicate rows (Test):  {test_dupes}')\n",
                "\n",
                "print('Data Types:')\n",
                "print(train_df.dtypes.value_counts())\n",
                "\n",
                "feature_cols = train_df.columns[:-1]\n",
                "print(f'Numeric features: {len(feature_cols)}')\n",
                "print(f'Target type: {train_df.iloc[:, -1].dtype}')\n",
                "print(f'Unique activities: {train_df.iloc[:, -1].nunique()ifr}')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 3. Target Variable Analysis - Class Distribution"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "y_train = train_df.iloc[:, -1]\n",
                "y_test = test_df.iloc[:, -1]\n",
                "\n",
                "train_dist = y_train.value_counts().sort_index()\n",
                "test_dist = y_test.value_counts().sort_index()\n",
                "\n",
                "dist_df = pd.DataFrame({\n",
                "    'Train_Count': train_dist,\n",
                "    'Train_Pct': (train_dist / len(y_train) * 100).round(2),\n",
                "    'Test_Count': test_dist,\n",
                "    'Test_Pct': (test_dist / len(y_test) * 100).round(2)\n",
                "})\n",
                "dist_df.index.name = 'Activity'\n",
                "print(dist_df)\n",
                "\n",
                "train_balance = train_dist.min() / train_dist.max()\n",
                "test_balance = test_dist.min() / test_dist.max()\n",
                "print(f'Class Balance Ratio (Train): {train_balance:.3f}')\n",
                "print(f'Class Balance Ratio (Test):  {test_balance:.3f}')"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "fig, axes = plt.subplots(2, 2, figsize=(16, 12))\n",
                "fig.suptitle('Activity Class Distribution Analysis', fontsize=16, fontweight='bold', y=1.02)\n",
                "\n",
                "colors = [activity_colors.get(x, '#333333') for x in train_dist.index]\n",
                "bars = axes[0, 0].bar(train_dist.index, train_dist.values, color=colors, edgecolor='white', linewidth=1.5)\n",
                "axes[0, 0].set_title('Train Set Distribution', fontweight='bold', fontsize=12)\n",
                "axes[0, 0].set_ylabel('Number of Samples', fontsize=10)\n",
                "axes[0, 0].tick_params(axis='x', rotation=45)\n",
                "for bar, val in zip(bars, train_dist.values):\n",
                "    axes[0, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20, \n",
                "                    f'{val:,}', ha='center', va='bottom', fontweight='bold')\n",
                "\n",
                "wedges, texts, autotexts = axes[0, 1].pie(train_dist.values, labels=train_dist.index, \n",
                "                                             autopct='%1.1f%%', colors=colors,\n",
                "                                             startangle=90, textprops={'fontsize': 9})\n",
                "axes[0, 1].set_title('Train Set Proportions', fontweight='bold', fontsize=12)\n",
                "\n",
                "colors_test = [activity_colors.get(x, '#333333') for x in test_dist.index]\n",
                "bars = axes[1, 0].bar(test_dist.index, test_dist.values, color=colors_test, edgecolor='white', linewidth=1.5)\n",
                "axes[1, 0].set_title('Test Set Distribution', fontweight='bold', fontsize=12)\n",
                "axes[1, 0].set_ylabel('Number of Samples', fontsize=10)\n",
                "axes[1, 0].tick_params(axis='x', rotation=45)\n",
                "for bar, val in zip(bars, test_dist.values):\n",
                "    axes[1, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,\n",
                "                    f'{val:,}', ha='center', va='bottom', fontweight='bold')\n",
                "\n",
                "x = np.arange(len(train_dist))\n",
                "width = 0.35\n",
                "axes[1, 1].bar(x - width/2, train_dist.values, width, label='Train', color='#2E86AB', alpha=0.8)\n",
                "axes[1, 1].bar(x + width/2, test_dist.values, width, label='Test', color='#A23B72', alpha=0.8)\n",
                "axes[1, 1].set_xticks(x)\n",
                "axes[1, 1].set_xticklabels(train_dist.index, rotation=45, ha='right')\n",
                "axes[1, 1].set_title('Train vs Test Distribution', fontweight='bold', fontsize=12)\n",
                "axes[1, 1].set_ylabel('Number of Samples', fontsize=10)\n",
                "axes[1, 1].legend()\n",
                "\n",
                "plt.tight_layout()\n",
                "os.makedirs('../presentation', exist_ok=True)\n",
                "plt.savefig('../presentation/01_class_distribution.png', dpi=200, bbox_inches='tight')\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 4. Feature Engineering Analysis - Sensor Signal Types"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "feature_names = train_df.columns[:-1].tolist()\n",
                "\n",
                "signal_types = {}\n",
                "for col in feature_names:\n",
                "    if col.startswith('tBodyAcc'):\n",
                "        signal_types[col] = 'Time_Body_Accelerometer'\n",
                "    elif col.startswith('tGravityAcc'):\n",
                "        signal_types[col] = 'Time_Gravity_Accelerometer'\n",
                "    elif col.startswith('tBodyGyro'):\n",
                "        signal_types[col] = 'Time_Body_Gyroscope'\n",
                "    elif col.startswith('fBodyAcc'):\n",
                "        signal_types[col] = 'Freq_Body_Accelerometer'\n",
                "    elif col.startswith('fBodyGyro'):\n",
                "        signal_types[col] = 'Freq_Body_Gyroscope'\n",
                "    elif col.startswith('fBodyAccMag') or col.startswith('fBodyBodyAcc'):\n",
                "        signal_types[col] = 'Freq_Body_Accel_Magnitude'\n",
                "    elif col.startswith('fBodyGyroMag') or col.startswith('fBodyBodyGyro'):\n",
                "        signal_types[col] = 'Freq_Body_Gyro_Magnitude'\n",
                "    else:\n",
                "        signal_types[col] = 'Other'\n",
                "\n",
                "signal_df = pd.Series(signal_types).value_counts()\n",
                "print('Feature Categories:')\n",
                "for cat, count in signal_df.items():\n",
                "    print(f'  {cat}: {count} features')"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "joblib.dump((train_df.iloc[:, :-1], train_df.iloc[:, -1], test_df.iloc[:, :-1], test_df.iloc[:, -1]), '../data/processed_data.pkl')\n",
                "print('Processed data saved successfully!')"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.10.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open('notebooks/01_eda_detailed.ipynb', 'w') as f:
    json.dump(notebook, f, indent=2)

print("Notebook fixed successfully!")
