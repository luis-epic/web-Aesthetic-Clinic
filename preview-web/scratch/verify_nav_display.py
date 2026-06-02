import os

root_dir = r"c:\Users\luis\Downloads\web-preview-navegable\preview-web"
target_css = "nav[data-astro-cid-3ef6ksr2] ul[data-astro-cid-3ef6ksr2] a[data-astro-cid-3ef6ksr2]{display:block;text-align:center;"

errors = 0
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if target_css not in content:
                print(f"Error: display:block missing in {os.path.relpath(filepath, root_dir)}")
                errors += 1

if errors == 0:
    print("Verification SUCCESSFUL. All 16 files correctly updated.")
else:
    print(f"Verification FAILED with {errors} error(s).")
    exit(1)
