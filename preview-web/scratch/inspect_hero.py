with open("c:\\Users\\luis\\Downloads\\web-preview-navegable\\preview-web\\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Search for the class containing "hero" in the HTML code
start_idx = html.find('class="hero"')
if start_idx == -1:
    # Try looking for other markers, like astro class names
    start_idx = html.find('hero')

if start_idx != -1:
    print("Found hero reference at index:", start_idx)
    # Print 3000 characters around it
    start = max(0, start_idx - 100)
    print(html[start:start+3000])
else:
    print("Hero section not found")
