import os

root_dir = r"c:\Users\luis\Downloads\web-preview-navegable\preview-web"

# Replacements to improve line-height of headings and avoid overlapping text lines
REPLACEMENTS = [
    ("line-height:1.12", "line-height:1.3"),
    ("line-height: 1.12", "line-height: 1.3"),
    ("line-height:1.1", "line-height:1.3"),
    ("line-height: 1.1", "line-height: 1.3"),
    ("line-height:1.05", "line-height:1.25"),
    ("line-height: 1.05", "line-height: 1.25")
]

modified_count = 0
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            updated = False
            for old, new in REPLACEMENTS:
                if old in content:
                    content = content.replace(old, new)
                    updated = True
            
            if updated:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Patched line-heights in: {os.path.relpath(filepath, root_dir)}")
                modified_count += 1

print(f"Successfully improved line-heights in {modified_count} files.")
