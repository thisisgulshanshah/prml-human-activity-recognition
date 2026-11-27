import os

# Just check the Downloads folder
downloads = '/Users/thisisgulshanshah/Downloads'
print("Checking Downloads...")

try:
    contents = os.listdir(downloads)
    print(f"Downloads contents: {contents}")
except Exception as e:
    print(f"Error: {e}")

# Check for archive folder
archive = os.path.join(downloads, 'archive')
if os.path.exists(archive):
    print(f"Archive exists: {os.listdir(archive)}")
    train_path = os.path.join(archive, 'train.csv')
    test_path = os.path.join(archive, 'test.csv')
    if os.path.exists(train_path):
        print(f"train.csv found in archive!")
    if os.path.exists(test_path):
        print(f"test.csv found in archive!")
else:
    print("Archive folder not found in Downloads")

# Check for prml-har-project
prml = '/Users/thisisgulshanshah/prml-har-project'
if os.path.exists(prml):
    print(f"prml-har-project exists: {os.listdir(prml)}")
    data_dir = os.path.join(prml, 'data')
    if os.path.exists(data_dir):
        print(f"data folder: {os.listdir(data_dir)}")
else:
    print("prml-har-project not found in home")