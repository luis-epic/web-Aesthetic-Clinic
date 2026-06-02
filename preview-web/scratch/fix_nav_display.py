import os

root_dir = r"c:\Users\luis\Downloads\web-preview-navegable\preview-web"

target_css = "nav[data-astro-cid-3ef6ksr2] ul[data-astro-cid-3ef6ksr2] a[data-astro-cid-3ef6ksr2]{font-size:.9rem;padding:15px 0;width:100%;border-bottom:1px solid var(--line)}"
replacement_css = "nav[data-astro-cid-3ef6ksr2] ul[data-astro-cid-3ef6ksr2] a[data-astro-cid-3ef6ksr2]{display:block;text-align:center;font-size:.9rem;padding:15px 0;width:100%;border-bottom:1px solid var(--line)}"

modified_count = 0
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if target_css in content:
                content = content.replace(target_css, replacement_css)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Patched display:block in: {os.path.relpath(filepath, root_dir)}")
                modified_count += 1
            else:
                # Check for alternative spacing or already patched
                if replacement_css in content:
                    print(f"Already patched display:block in: {os.path.relpath(filepath, root_dir)}")
                else:
                    print(f"Warning: Target CSS not found in: {os.path.relpath(filepath, root_dir)}")

print(f"Successfully fixed navigation link borders in {modified_count} files.")
