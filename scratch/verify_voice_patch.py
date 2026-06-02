import os
import pathlib

def verify_file(filepath):
    p = pathlib.Path(filepath)
    content = p.read_text(encoding="utf-8")
    
    issues = []
    
    # Check volume button
    vol_count = content.count('id="aiChatVolume"')
    if vol_count != 1:
        issues.append(f"Expected exactly 1 volume button, found {vol_count}")
        
    # Check mic button
    mic_count = content.count('id="aiChatMic"')
    if mic_count != 1:
        issues.append(f"Expected exactly 1 mic button, found {mic_count}")
        
    # Check JS support
    js_count = content.count('initVoiceChatSupport')
    if js_count != 1:
        issues.append(f"Expected exactly 1 JS voice support instance, found {js_count}")
        
    # Check CSS styles
    css_count = content.count('/* ── Estilos de Voz Asistente AI ── */')
    if css_count != 1:
        issues.append(f"Expected exactly 1 CSS voice styling block, found {css_count}")
        
    # Check typing timeout hook
    hook_count = content.count('window.speakAiResponse(botResponse)')
    if hook_count == 0:
        issues.append("Could not find window.speakAiResponse call in typing timeout callbacks")
    elif hook_count < 2:
        issues.append(f"Expected at least 2 hook calls, found {hook_count}")
        
    if issues:
        print(f"File: {filepath} -> FAILED")
        for iss in issues:
            print(f"  - {iss}")
        return False
    else:
        print(f"File: {filepath} -> PASSED")
        return True

def main():
    base_dir = r"c:\Users\luis\Downloads\web-preview-navegable\preview-web"
    html_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    failed = 0
    for f in html_files:
        if not verify_file(f):
            failed += 1
            
    if failed == 0:
        print("All files passed verification successfully!")
    else:
        print(f"{failed} files failed verification.")

if __name__ == '__main__':
    main()
