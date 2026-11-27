"""
Download UCI HAR Dataset directly from UCI repository if local files not found.
This is a backup in case the Kaggle files aren't available.
"""
import os
import requests
import zipfile
import io
import shutil

# UCI HAR Dataset URL
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00240/UCI%20HAR%20Dataset.zip"

data_dir = '/Users/thisisgulshanshah/Documents/programming/Vibe Codedd/free-claude-code/AIML-PROJECT/data'

print("Checking for existing data...")

# Check if train.csv and test.csv already exist
train_path = os.path.join(data_dir, 'train.csv')
test_path = os.path.join(data_dir, 'test.csv')

if os.path.exists(train_path) and os.path.exists(test_path):
    print("Data files already exist!")
    exit(0)

print("Downloading UCI HAR Dataset...")
try:
    response = requests.get(url, stream=True)
    response.raise_for_status()

    print("Extracting...")
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        z.extractall(data_dir)

    print("Extracted. Processing...")

    # The UCI HAR dataset has train/X_train.txt, train/y_train.txt, etc.
    # We need to combine them into CSV format
    import numpy as np
    import pandas as pd

    # Read feature names
    features_path = os.path.join(data_dir, 'UCI HAR Dataset', 'features.txt')
    features = pd.read_csv(features_path, sep='\\s+', header=None, names=['idx', 'name'])
    feature_names = features['name'].tolist()

    # Read activity labels
    activity_path = os.path.join(data_dir, 'UCI HAR Dataset', 'activity_labels.txt')
    activities = pd.read_csv(activity_path, sep='\\s+', header=None, names=['idx', 'activity'])

    # Read train data
    X_train = pd.read_csv(
        os.path.join(data_dir, 'UCI HAR Dataset', 'train', 'X_train.txt'),
        sep='\\s+', header=None, names=feature_names
    )
    y_train = pd.read_csv(
        os.path.join(data_dir, 'UCI HAR Dataset', 'train', 'y_train.txt'),
        sep='\\s+', header=None, names=['activity_idx']
    )
    y_train['activity'] = y_train['activity_idx'].map(dict(zip(activities['idx'], activities['activity'])))

    # Read test data
    X_test = pd.read_csv(
        os.path.join(data_dir, 'UCI HAR Dataset', 'test', 'X_test.txt'),
        sep='\\s+', header=None, names=feature_names
    )
    y_test = pd.read_csv(
        os.path.join(data_dir, 'UCI HAR Dataset', 'test', 'y_test.txt'),
        sep='\\s+', header=None, names=['activity_idx']
    )
    y_test['activity'] = y_test['activity_idx'].map(dict(zip(activities['idx'], activities['activity'])))

    # Combine
    train_df = pd.concat([X_train, y_train[['activity']]], axis=1)
    test_df = pd.concat([X_test, y_test[['activity']]], axis=1)

    # Save as CSV
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)

    print(f"Saved train.csv: {train_df.shape}")
    print(f"Saved test.csv: {test_df.shape}")

    # Clean up extracted folder
    shutil.rmtree(os.path.join(data_dir, 'UCI HAR Dataset'))

    print("Done!")

except Exception as e:
    print(f"Error: {e}")
    print("Please manually place train.csv and test.csv in the data folder")