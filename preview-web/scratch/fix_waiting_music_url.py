import os

root_dir = r"c:\Users\luis\Downloads\web-preview-navegable\preview-web"

old_url = "https://assets.mixkit.co/music/preview/mixkit-relaxing-in-the-spa-2194.mp3"
new_url = "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Gymnopedie%20No%201.mp3"

modified_count = 0
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if old_url in content:
                content = content.replace(old_url, new_url)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Patched Gymnopedie No 1 in: {os.path.relpath(filepath, root_dir)}")
                modified_count += 1
            else:
                if new_url in content:
                    print(f"Already patched in: {os.path.relpath(filepath, root_dir)}")
                else:
                    print(f"Warning: Mixkit URL not found in: {os.path.relpath(filepath, root_dir)}")

print(f"Successfully updated music source URL in {modified_count} files.")
