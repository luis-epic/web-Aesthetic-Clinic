with open(r"c:\Users\luis\Downloads\web-preview-navegable\preview-web\index.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
styles = re.findall(r"<style[^>]*>(.*?)</style>", content, re.DOTALL)
print("Navigation styles:")
for style in styles:
    for rule in style.split("}"):
        if "data-astro-cid-3ef6ksr2" in rule and ("ul" in rule or "li" in rule or "nav" in rule or "burger" in rule):
            print(rule.strip() + "}")
