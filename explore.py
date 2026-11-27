import os

# Search for train.csv
search_paths = [
    '/Users/thisisgulshanshah/Downloads',
    '/Users/thisisgulshanshah/prml-har-project',
    '/Users/thisisgulshanshah/Documents/prml-har-project',
    '/Users/thisisgulshanshah/Documents/programming/prml-har-project',
    '/Users/thisisgulshanshah/Documents/programming/Vibe Codedd/free-claude-code/AIML-PROJECT',
]

for base in search_paths:
    for root, dirs, files in os.walk(base):
        for f in files:
            if 'train' in f.lower() and f.endswith('.csv'):
                print(f'FOUND: {os.path.join(root, f)}')
            if 'test' in f.lower() and f.endswith('.csv'):
                print(f'FOUND: {os.path.join(root, f)}')

print('Search complete')