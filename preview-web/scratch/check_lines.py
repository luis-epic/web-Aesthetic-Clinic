with open(r"c:\Users\luis\Downloads\web-preview-navegable\preview-web\index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Search for any element or text with lines, borders or underlines
import re
print("Search for potential text overlapping elements:")
# Look for custom line decorations
matches = re.findall(r"\.[a-zA-Z0-9_-]+\s*\{[^}]*border[^}]*\}", content)
for m in matches[:10]:
    print(m)
