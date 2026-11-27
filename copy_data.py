import os
import shutil
import glob

# Check what's in Downloads
downloads = '/Users/thisisgulshanshah/Downloads'
print(f"Downloads contents: {os.listdir(downloads)}")

# Check for archive
archive = os.path.join(downloads, 'archive')
if os.path.exists(archive):
    print(f"Archive contents: {os.listdir(archive)}")

    # Copy files
    target = '/Users/thisisgulshanshah/Documents/programming/Vibe Codedd/free-claude-code/AIML-PROJECT/data'
    os.makedirs(target, exist_ok=True)

    for f in ['train.csv', 'test.csv']:
        src = os.path.join(archive, f)
        dst = os.path.join(target, f)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied {src} -> {dst}")
        else:
            print(f"Not found: {src}")
else:
    print("Archive folder not found")

# Also check prml-har-project
prml = '/Users/thisisgulshanshah/prml-har-project'
if os.path.exists(prml):
    print(f"prml-har-project contents: {os.listdir(prml)}")
    data_dir = os.path.join(prml, 'data')
    if os.path.exists(data_dir):
        print(f"data contents: {os.listdir(data_dir)}")
        target = '/Users/thisisgulshanshah/Documents/programming/Vibe Codedd/free-claude-code/AIML-PROJECT/data'
        for f in ['train.csv', 'test.csv']:
            src = os.path.join(data_dir, f)
            dst = os.path.join(target, f)
            if os.path.exists(src):
                shutil.copy2(src, dst)
                print(f"Copied {src} -> {dst}")