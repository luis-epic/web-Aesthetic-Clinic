with open(r"c:\Users\luis\Downloads\web-preview-navegable\preview-web\index.html.bak", "r", encoding="utf-8") as f:
    content = f.read()

# Look for styles
import re
styles = re.findall(r"<style>(.*?)</style>", content, re.DOTALL)
if styles:
    print(f"Found {len(styles)} style blocks.")
    print("First 500 chars of style block 1:")
    print(styles[0][:500])
else:
    print("No style blocks found in index.html.bak")
