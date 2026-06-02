import os

root_dir = r"c:\Users\luis\Downloads\web-preview-navegable\preview-web"

target_css_1 = "nav[data-astro-cid-3ef6ksr2] ul[data-astro-cid-3ef6ksr2]{position:fixed;inset:124px 0 auto;flex-direction:column;background:var(--paper);padding:24px 30px;gap:0;transform:translateY(-140%);transition:transform .45s cubic-bezier(.5,0,.1,1);box-shadow:var(--shadow);border-bottom:1px solid var(--line);max-height:80vh;overflow:auto}"
replacement_css_1 = "nav[data-astro-cid-3ef6ksr2] ul[data-astro-cid-3ef6ksr2]{position:absolute;top:100%;left:0;right:0;flex-direction:column;background:var(--paper);padding:24px 30px;gap:0;transform:translateY(-110%);opacity:0;visibility:hidden;pointer-events:none;transition:transform .45s cubic-bezier(.5,0,.1,1),opacity .45s,visibility .45s;box-shadow:var(--shadow);border-bottom:1px solid var(--line);max-height:80vh;overflow:auto;z-index:99}"

target_css_2 = "nav[data-astro-cid-3ef6ksr2] ul[data-astro-cid-3ef6ksr2].show{transform:translateY(0)}"
replacement_css_2 = "nav[data-astro-cid-3ef6ksr2] ul[data-astro-cid-3ef6ksr2].show{transform:translateY(0);opacity:1;visibility:visible;pointer-events:auto}"

modified_count = 0
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            updated = False
            if target_css_1 in content:
                content = content.replace(target_css_1, replacement_css_1)
                updated = True
            
            if target_css_2 in content:
                content = content.replace(target_css_2, replacement_css_2)
                updated = True
            
            if updated:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Patched: {os.path.relpath(filepath, root_dir)}")
                modified_count += 1
            else:
                # Check if it was already updated or not found
                if replacement_css_1 in content:
                    print(f"Already patched: {os.path.relpath(filepath, root_dir)}")
                else:
                    print(f"Warning: Targets not found in: {os.path.relpath(filepath, root_dir)}")

print(f"Successfully patched {modified_count} files.")
