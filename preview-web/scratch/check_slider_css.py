with open(r"c:\Users\luis\Downloads\web-preview-navegable\preview-web\index.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = re.finditer(r"(\.[a-zA-Z0-9_-]+slider[^{}]*|\.[a-zA-Z0-9_-]+handle[^{}]*)\s*\{[^{}]*\}", content)
for m in matches:
    print(m.group(0))

# Print all classes inside style with slider or handle
print("\nMore details:")
style_content = re.search(r"<style>(.*?)</style>", content, re.DOTALL)
if style_content:
    style_text = style_content.group(1)
    for m in re.finditer(r"\.[a-zA-Z0-9_-]*(?:slider|handle|divider|bar)[a-zA-Z0-9_-]*\s*\{[^{}]*\}", style_text):
        print(m.group(0))
