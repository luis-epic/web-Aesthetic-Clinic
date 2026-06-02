with open(r"c:\Users\luis\Downloads\web-preview-navegable\preview-web\index.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
styles = re.findall(r"<style[^>]*>(.*?)</style>", content, re.DOTALL)
print(f"Found {len(styles)} style blocks.")

for i, style in enumerate(styles):
    for rule in style.split("}"):
        if "slider" in rule or "handle" in rule:
            print(f"Block {i}: {rule.strip()}}}")
