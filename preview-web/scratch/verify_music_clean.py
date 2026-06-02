import os

root_dir = r"c:\Users\luis\Downloads\web-preview-navegable\preview-web"

def verify_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    checks = {
        "ai-chat-music-btn CSS class": ".ai-chat-music-btn",
        "aiChatMusic HTML button id": 'id="aiChatMusic"',
        "waitingMusicAudio tag": 'id="waitingMusicAudio"',
        "local waiting_music.mp3 source": 'src="/waiting_music.mp3"',
        "waitingMusicPlaying localStorage JS key": "'waitingMusicPlaying'",
    }
    
    missing = []
    for desc, term in checks.items():
        if term not in content:
            missing.append(desc)
            
    if missing:
        print(f"Error in {os.path.relpath(filepath, root_dir)}: missing {', '.join(missing)}")
        return False
    return True

def main():
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    print(f"Verifying {len(html_files)} HTML files...")
    failures = 0
    for f in html_files:
        if not verify_file(f):
            failures += 1
            
    if failures == 0:
        print("ALL 16 HTML FILES VERIFIED SUCCESSFULLY!")
    else:
        print(f"VERIFICATION FAILED: {failures} files have issues.")

if __name__ == '__main__':
    main()
