with open(r"c:\Users\luis\Downloads\web-preview-navegable\preview-web\index.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = re.findall(r"line-height:[^;}]*", content)
for m in set(matches):
    print(m)
