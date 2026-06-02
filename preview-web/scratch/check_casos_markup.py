with open(r"c:\Users\luis\Downloads\web-preview-navegable\preview-web\index.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = re.findall(r'<div[^>]*class="[^"]*comparison-slider[^"]*"[^>]*>.*?</div>', content, re.DOTALL)
if matches:
    print(matches[0][:4000])
