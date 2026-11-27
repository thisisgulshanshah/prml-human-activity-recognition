import os
import shutil
import glob

# Search everywhere for train.csv and test.csv
print("Searching for data files...")

# Try common locations
search_dirs = [
    '/Users/thisisgulshanshah/Downloads',
    '/Users/thisisgulshanshah/prml-har-project',
    '/Users/thisisgulshanshah/Documents/prml-har-project',
    '/Users/thisisgulshanshah/Documents/programming/prml-har-project',
    '/Users/thisisgulshanshah/Documents/programming/Vibe Codedd/free-claude-code',
    '/Users/thisisgulshanshah/Documents',
    '/Users/thisisgulshanshah/Desktop',
]

found_train = []
found_test = []

for base in search_dirs:
    if os.path.exists(base):
        for root, dirs, files in os.walk(base):
            for f in files:
                if f == 'train.csv':
                    found_train.append(os.path.join(root, f))
                if f == 'test.csv':
                    found_test.append(os.path.join(root, f))

print(f"Found train.csv: {found_train}")
print(f"Found test.csv: {found_test}")

# Also check Downloads/archive specifically
archive_train = '/Users/thisisgulshanshah/Downloads/archive/train.csv'
archive_test = '/Users/thisisgulshanshah/Downloads/archive/test.csv'

if os.path.exists(archive_train):
    print(f"Found in archive: {archive_train}")
if os.path.exists(archive_test):
    print(f"Found in archive: {archive_test}")

# Check if Downloads/archive exists
archive_dir = '/Users/thisisgulshanshah/Downloads/archive'
if os.path.exists(archive_dir):
    print(f"Archive dir exists: {os.listdir(archive_dir)}")
else:
    print("Archive dir not found")

# Copy to our project if found
target = '/Users/thisisgulshanshah/Documents/programming/Vibe Codedd/free-claude-code/AIML-PROJECT/data'

for f in found_train:
    dst = os.path.join(target, 'train.csv')
    shutil.copy2(f, dst)
    print(f"Copied {f} -> {dst}")

for f in found_test:
    dst = os.path.join(target, 'test.csv')
    shutil.copy2(f, dst)
    print(f"Copied {f} -> {dst}")

print("Done!")