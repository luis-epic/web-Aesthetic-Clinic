import os

root_dir = r"c:\Users\luis\Downloads\web-preview-navegable\preview-web"

target_css_1 = "nav[data-astro-cid-3ef6ksr2] ul[data-astro-cid-3ef6ksr2]{position:fixed;inset:124px 0 auto;"
target_css_2 = "nav[data-astro-cid-3ef6ksr2] ul[data-astro-cid-3ef6ksr2].show{transform:translateY(0)}"

replacement_css_1 = "nav[data-astro-cid-3ef6ksr2] ul[data-astro-cid-3ef6ksr2]{position:absolute;top:100%;"
replacement_css_2 = "nav[data-astro-cid-3ef6ksr2] ul[data-astro-cid-3ef6ksr2].show{transform:translateY(0);opacity:1;visibility:visible;pointer-events:auto}"

errors = 0
html_files = []

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

for filepath in html_files:
    rel_path = os.path.relpath(filepath, root_dir)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if target_css_1 in content:
        print(f"Error: Old CSS rule 1 still present in {rel_path}")
        errors += 1
    
    if target_css_2 in content:
        # Check if it was replaced or if it matches target_css_2 exactly (which was old)
        # Note: the old was exactly `nav[data-astro-cid-3ef6ksr2] ul[data-astro-cid-3ef6ksr2].show{transform:translateY(0)}`
        # and the new contains `opacity:1;visibility:visible;pointer-events:auto`
        if f"{target_css_2}nav" in content or f"{target_css_2}<" in content or content.endswith(target_css_2):
            print(f"Error: Old CSS rule 2 still present in {rel_path}")
            errors += 1
            
    if replacement_css_1 not in content:
        print(f"Error: New CSS rule 1 NOT found in {rel_path}")
        errors += 1
        
    if replacement_css_2 not in content:
        print(f"Error: New CSS rule 2 NOT found in {rel_path}")
        errors += 1

if errors == 0:
    print(f"Verification SUCCESSFUL. Checked {len(html_files)} files. No errors found.")
else:
    print(f"Verification FAILED with {errors} error(s).")
    exit(1)
