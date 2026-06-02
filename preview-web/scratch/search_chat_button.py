with open(r"c:\Users\luis\Downloads\web-preview-navegable\preview-web\index.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
style_content = re.search(r"<style[^>]*>(.*?)</style>", content, re.DOTALL)
if style_content:
    style_text = style_content.group(1)
    for rule in style_text.split("}"):
        if "ai-chat-btn" in rule or "ai-chat-window" in rule:
            print(rule.strip() + "}")
else:
    print("No style block")
