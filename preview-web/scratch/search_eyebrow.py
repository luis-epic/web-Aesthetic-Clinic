with open(r"c:\Users\luis\Downloads\web-preview-navegable\preview-web\index.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = re.finditer(r"eyebrow", content)
count = 0
for m in matches:
    count += 1
    start = max(0, m.start() - 50)
    end = min(len(content), m.end() + 50)
    print(f"Match {count}: {content[start:end]}")
