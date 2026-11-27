import os

dirs = [
    'data',
    'notebooks',
    'src',
    'models',
    'presentation'
]

base = '/Users/thisisgulshanshah/Documents/programming/Vibe Codedd/free-claude-code/AIML-PROJECT'

for d in dirs:
    path = os.path.join(base, d)
    os.makedirs(path, exist_ok=True)
    print(f'Created: {path}')

print('Done!')