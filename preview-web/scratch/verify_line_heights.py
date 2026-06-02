import os
import re

root_dir = r"c:\Users\luis\Downloads\web-preview-navegable\preview-web"

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find any remaining line-heights under 1.2
            for m in re.finditer(r"line-height:\s*1\.[0-1][0-9]*[^;}]*", content):
                val = m.group(0)
                # Ignore button close or single characters or elements that are not headings/text blocks
                if "1.12" in val or "1.1" in val or "1.05" in val:
                    print(f"Remaining in {os.path.relpath(filepath, root_dir)}: {val}")
