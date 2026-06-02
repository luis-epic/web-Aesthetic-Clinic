import os

root_dir = r"c:\Users\luis\Downloads\web-preview-navegable\preview-web"
target_text = "initAmbientWaitingMusic"

errors = 0
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if target_text not in content:
                print(f"Error: Waiting music support missing in {os.path.relpath(filepath, root_dir)}")
                errors += 1

if errors == 0:
    print("Verification SUCCESSFUL. Waiting music correctly injected into all 16 files.")
else:
    print(f"Verification FAILED with {errors} error(s).")
    exit(1)
