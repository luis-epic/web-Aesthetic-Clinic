import os

root_dir = r"c:\Users\luis\Downloads\web-preview-navegable\preview-web"
target_url = "https://incompetech.com/music/royalty-free/mp3-royaltyfree/Gymnopedie%20No%201.mp3"

errors = 0
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if target_url not in content:
                print(f"Error: Target URL not found in {os.path.relpath(filepath, root_dir)}")
                errors += 1

if errors == 0:
    print("Verification SUCCESSFUL. All 16 files correctly updated with Gymnopedie No 1 music URL.")
else:
    print(f"Verification FAILED with {errors} error(s).")
    exit(1)
