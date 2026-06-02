with open(r"c:\Users\luis\Downloads\web-preview-navegable\preview-web\index.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
style_content = re.search(r"<style>(.*?)</style>", content, re.DOTALL)
if style_content:
    style_text = style_content.group(1)
    
    # Search for styles of slider-handle pseudos
    for m in re.finditer(r"\.slider-handle[^}]*\{[^}]*\}", style_text):
        print(m.group(0))
else:
    print("No style block")
