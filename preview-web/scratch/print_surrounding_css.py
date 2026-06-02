with open(r"c:\Users\luis\Downloads\web-preview-navegable\preview-web\index.html", "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find("nav[data-astro-cid-3ef6ksr2] ul[data-astro-cid-3ef6ksr2]{position:fixed;")
if idx != -1:
    print(content[idx:idx+600])
else:
    print("Not found")
