with open("c:\\Users\\luis\\Downloads\\web-preview-navegable\\preview-web\\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Let's search for script tags
import re
scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
print(f"Found {len(scripts)} script blocks.")

for i, script in enumerate(scripts):
    if "hero" in script.lower() or "slide" in script.lower():
        print(f"\n--- Script Block {i} (contains 'hero' or 'slide') ---")
        # Print first 2000 chars of the script block
        print(script[:2000])
