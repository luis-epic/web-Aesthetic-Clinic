with open(r"c:\Users\luis\Downloads\web-preview-navegable\preview-web\index.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
styles = re.findall(r"<style[^>]*>(.*?)</style>", content, re.DOTALL)
print("Before and after decorations:")
for style in styles:
    for m in re.finditer(r"([^{}]+:(?:before|after)[^{}]*\{[^{}]*\})", style):
        print(m.group(0))
