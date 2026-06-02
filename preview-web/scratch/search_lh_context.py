import os
import re

root_dir = r"c:\Users\luis\Downloads\web-preview-navegable\preview-web"

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find line-height and print surrounding 150 chars
            for m in re.finditer(r"line-height:\s*1[^;}]*", content):
                start = max(0, m.start() - 100)
                end = min(len(content), m.end() + 100)
                print(f"File: {os.path.relpath(filepath, root_dir)}")
                print(f"Context: {content[start:end]}")
                print("="*40)
