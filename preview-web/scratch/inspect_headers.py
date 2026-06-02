import os
import re

root_dir = r"c:\Users\luis\Downloads\web-preview-navegable\preview-web"

def inspect_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract <header class="nav" ...> ... </header>
    match = re.search(r'<header[^>]*>.*?</header>', content, re.DOTALL)
    if match:
        print(f"File: {os.path.relpath(filepath, root_dir)}")
        print(match.group(0))
        print("-" * 50)
    else:
        print(f"File: {os.path.relpath(filepath, root_dir)} - NO HEADER FOUND")

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.html'):
            inspect_file(os.path.join(root, file))
