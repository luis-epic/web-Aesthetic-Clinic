with open(r"c:\Users\luis\Downloads\web-preview-navegable\preview-web\index.html", "r", encoding="utf-8") as f:
    content = f.read()

print(f"File size: {len(content)}")
print(f"Count of 'slider': {content.lower().count('slider')}")
print(f"Count of 'handle': {content.lower().count('handle')}")
