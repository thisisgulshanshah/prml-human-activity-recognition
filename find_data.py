import os
import shutil

# Check possible locations
possible_paths = [
    '/Users/thisisgulshanshah/Downloads/archive/train.csv',
    '/Users/thisisgulshanshah/Downloads/archive/test.csv',
    '/Users/thisisgulshanshah/prml-har-project/data/train.csv',
    '/Users/thisisgulshanshah/prml-har-project/data/test.csv',
    '/Users/thisisgulshanshah/Documents/prml-har-project/data/train.csv',
    '/Users/thisisgulshanshah/Documents/prml-har-project/data/test.csv',
]

target_dir = '/Users/thisisgulshanshah/Documents/programming/Vibe Codedd/free-claude-code/AIML-PROJECT/data'

for src in possible_paths:
    if os.path.exists(src):
        print(f'Found: {src}')
        dst = os.path.join(target_dir, os.path.basename(src))
        shutil.copy2(src, dst)
        print(f'Copied to: {dst}')
    else:
        print(f'Not found: {src}')

# List target dir
print('\nTarget directory contents:')
print(os.listdir(target_dir))