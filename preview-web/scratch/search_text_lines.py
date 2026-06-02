with open(r"c:\Users\luis\Downloads\web-preview-navegable\preview-web\index.html", "r", encoding="utf-8") as f:
    content = f.read()

import re

# Find all matches of text-decoration or lines in CSS
print("Text decorations or line-heights in style:")
# Let's extract style tag content
style_content = re.search(r"<style>(.*?)</style>", content, re.DOTALL)
if style_content:
    style_text = style_content.group(1)
    
    # Search for border-bottom on text elements
    for m in re.finditer(r"([^{}]+)\{[^{}]*border-bottom[^{}]*\}", style_text):
        print(f"Border bottom: {m.group(0)}")
        
    for m in re.finditer(r"([^{}]+)\{[^{}]*text-decoration[^{}]*\}", style_text):
        print(f"Text decoration: {m.group(0)}")
        
    for m in re.finditer(r"([^{}]+)\{[^{}]*line-height[^{}]*\}", style_text):
        print(f"Line height: {m.group(0)}")
else:
    print("No style tag found")
