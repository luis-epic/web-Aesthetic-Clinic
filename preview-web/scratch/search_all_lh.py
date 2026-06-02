with open(r"c:\Users\luis\Downloads\web-preview-navegable\preview-web\index.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
styles = re.findall(r"<style[^>]*>(.*?)</style>", content, re.DOTALL)
print("Line-heights in styles:")
for i, style in enumerate(styles):
    for m in re.finditer(r"([^{}]+line-height[^}]+)", style):
        print(f"Block {i}: {m.group(0).strip()}")
