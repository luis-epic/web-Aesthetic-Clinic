with open(r"c:\Users\luis\Downloads\web-preview-navegable\preview-web\index.html", "r", encoding="utf-8") as f:
    content = f.read()

import re

print("Negative margins in CSS:")
neg_margins = re.findall(r"[a-zA-Z0-9_-]+\s*\{[^}]*margin-[a-z]+:\s*-[0-9][^}]*\}", content)
for m in neg_margins:
    print(m)

print("\nLine heights less than 1.2 in CSS:")
line_heights = re.findall(r"[a-zA-Z0-9_-]+\s*\{[^}]*line-height:\s*1\.[0-1][^}]*\}", content)
for m in line_heights:
    print(m)
