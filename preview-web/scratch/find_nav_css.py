with open(r"c:\Users\luis\Downloads\web-preview-navegable\preview-web\index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Let's find the media query block
import re
pattern = r"nav\[data-astro-cid-3ef6ksr2\] ul\[data-astro-cid-3ef6ksr2\]\{position:fixed;[^}]*\}"
match = re.search(pattern, content)
if match:
    print("Found match:")
    print(match.group(0))
else:
    print("No match found for mobile menu CSS definition")
