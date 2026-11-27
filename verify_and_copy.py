import os
import shutil

print("=== VERIFYING DATA LOCATIONS ===\n")

# Check 1: Downloads/archive
path1 = '/Users/thisisgulshanshah/Downloads/archive'
if os.path.exists(path1):
    print(f"✓ Downloads/archive exists: {os.listdir(path1)}")
    for f in ['train.csv', 'test.csv']:
        fp = os.path.join(path1, f)
        if os.path.exists(fp):
            size = os.path.getsize(fp) / 1024 / 1024
            print(f"  ✓ {f} ({size:.1f} MB)")
        else:
            print(f"  ✗ {f} NOT FOUND")
else:
    print(f"✗ Downloads/archive NOT FOUND")

# Check 2: prml-har-project
path2 = '/Users/thisisgulshanshah/prml-har-project'
if os.path.exists(path2):
    print(f"\n✓ prml-har-project exists: {os.listdir(path2)}")
    data_path = os.path.join(path2, 'data')
    if os.path.exists(data_path):
        print(f"  data/: {os.listdir(data_path)}")
        for f in ['train.csv', 'test.csv']:
            fp = os.path.join(data_path, f)
            if os.path.exists(fp):
                size = os.path.getsize(fp) / 1024 / 1024
                print(f"  ✓ {f} ({size:.1f} MB)")
            else:
                print(f"  ✗ {f} NOT FOUND")
else:
    print(f"\n✗ prml-har-project NOT FOUND")

# Check 3: Documents/prml-har-project
path3 = '/Users/thisisgulshanshah/Documents/prml-har-project'
if os.path.exists(path3):
    print(f"\n✓ Documents/prml-har-project exists: {os.listdir(path3)}")
else:
    print(f"\n✗ Documents/prml-har-project NOT FOUND")

# Target directory
target = '/Users/thisisgulshanshah/Documents/programming/Vibe Codedd/free-claude-code/AIML-PROJECT/data'
os.makedirs(target, exist_ok=True)

print(f"\n=== COPYING TO TARGET: {target} ===")

# Copy from Downloads/archive if exists
src_train = '/Users/thisisgulshanshah/Downloads/archive/train.csv'
src_test = '/Users/thisisgulshanshah/Downloads/archive/test.csv'

if os.path.exists(src_train):
    shutil.copy2(src_train, os.path.join(target, 'train.csv'))
    print(f"✓ Copied train.csv from Downloads/archive")
if os.path.exists(src_test):
    shutil.copy2(src_test, os.path.join(target, 'test.csv'))
    print(f"✓ Copied test.csv from Downloads/archive")

# Copy from prml-har-project/data if exists
src_train2 = '/Users/thisisgulshanshah/prml-har-project/data/train.csv'
src_test2 = '/Users/thisisgulshanshah/prml-har-project/data/test.csv'

if os.path.exists(src_train2):
    shutil.copy2(src_train2, os.path.join(target, 'train.csv'))
    print(f"✓ Copied train.csv from prml-har-project/data")
if os.path.exists(src_test2):
    shutil.copy2(src_test2, os.path.join(target, 'test.csv'))
    print(f"✓ Copied test.csv from prml-har-project/data")

# Verify target
print(f"\n=== TARGET CONTENTS ===")
for f in os.listdir(target):
    fp = os.path.join(target, f)
    size = os.path.getsize(fp) / 1024 / 1024
    print(f"  {f} ({size:.1f} MB)")

# Quick data check
if os.path.exists(os.path.join(target, 'train.csv')):
    import pandas as pd
    df = pd.read_csv(os.path.join(target, 'train.csv'))
    print(f"\n=== TRAIN DATA PREVIEW ===")
    print(f"Shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()[:5]}... (total {len(df.columns)})")
    print(f"Target column: {df.columns[-1]}")
    print(f"Classes: {df.iloc[:, -1].unique()}")
    print(f"Class distribution:\n{df.iloc[:, -1].value_counts().sort_index()}")

print("\n=== DONE ===")