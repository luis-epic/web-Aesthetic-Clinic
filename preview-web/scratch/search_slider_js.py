with open(r"c:\Users\luis\Downloads\web-preview-navegable\preview-web\index.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
scripts = re.findall(r"<script[^>]*>(.*?)</script>", content, re.DOTALL)
print(f"Found {len(scripts)} inline script blocks.")

for i, script in enumerate(scripts):
    if "slider" in script or "caso" in script:
        print(f"Block {i} (contains 'slider' or 'caso'):")
        print(script[:1500])
        print("-" * 50)
