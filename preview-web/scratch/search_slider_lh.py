with open(r"c:\Users\luis\Downloads\web-preview-navegable\preview-web\index.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
style_content = re.search(r"<style>(.*?)</style>", content, re.DOTALL)
if style_content:
    style_text = style_content.group(1)
    for line in style_text.split("}"):
        if "slider-handle" in line:
            print(line + "}")
else:
    print("No style block")
