import os
import pathlib

root_dir = r"c:\Users\luis\Downloads\web-preview-navegable\preview-web"

MUSIC_BTN_HTML = """      <button class="ai-chat-music-btn" id="aiChatMusic" aria-label="Activar música de espera" style="background:none; border:none; color:rgba(255,255,255,0.6); cursor:pointer; display:grid; place-items:center; transition:all 0.3s; padding: 4px; outline:none; margin-right: 6px;">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:19px; height:19px;" class="music-icon">
          <path d="M9 18V5l12-2v13"></path>
          <circle cx="6" cy="18" r="3"></circle>
          <circle cx="18" cy="16" r="3"></circle>
        </svg>
      </button>
      <button class="ai-chat-volume-btn" id="aiChatVolume\""""

AUDIO_TAG_HTML = """<audio id="waitingMusicAudio" loop preload="auto">
  <source src="/waiting_music.mp3" type="audio/mp3">
</audio>
</body>"""

CSS_INJECT = """/* ── Estilos de Voz Asistente AI ── */
.ai-chat-music-btn:hover {
  color: #fff !important;
  transform: scale(1.08) !important;
}
.ai-chat-music-btn.active {
  color: var(--gold-soft) !important;
}"""

JS_INJECT = """    // 3. Configuración de Música de Espera Local
    const musicBtn = document.getElementById('aiChatMusic');
    const musicAudio = document.getElementById('waitingMusicAudio');
    
    if (musicBtn && musicAudio) {
      let musicPlaying = localStorage.getItem('waitingMusicPlaying') === 'true';
      const musicVolume = localStorage.getItem('waitingMusicVolume') || '0.4';
      
      musicAudio.volume = parseFloat(musicVolume);
      musicBtn.classList.toggle('active', musicPlaying);
      
      if (musicPlaying) {
        musicAudio.play().then(() => {
          musicBtn.setAttribute('aria-label', 'Desactivar música de espera');
        }).catch(err => {
          console.log("Música de espera - Autoplay bloqueado.");
          musicPlaying = false;
          musicBtn.classList.remove('active');
          localStorage.setItem('waitingMusicPlaying', 'false');
        });
      }
      
      musicBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        musicPlaying = !musicPlaying;
        musicBtn.classList.toggle('active', musicPlaying);
        localStorage.setItem('waitingMusicPlaying', musicPlaying ? 'true' : 'false');
        
        if (musicPlaying) {
          musicBtn.setAttribute('aria-label', 'Desactivar música de espera');
          musicAudio.play().catch(err => {
            console.error("Error al reproducir la música de espera local:", err);
          });
        } else {
          musicBtn.setAttribute('aria-label', 'Activar música de espera');
          musicAudio.pause();
        }
      });
    }

    if (window.speechSynthesis && window.speechSynthesis.onvoiceschanged !== undefined) {"""

def patch_file(filepath):
    print(f"Processing: {filepath}")
    p = pathlib.Path(filepath)
    content = p.read_text(encoding="utf-8")
    
    # Normalize line endings
    content = content.replace('\r\n', '\n')
    
    if "aiChatMusic" in content:
        print("  Already contains music button. Skipping.")
        return False
        
    # 1. Prepend music button to volume button
    vol_target = '      <button class="ai-chat-volume-btn" id="aiChatVolume"'
    if vol_target in content:
        content = content.replace(vol_target, MUSIC_BTN_HTML, 1)
        print("  Music button injected in header.")
    else:
        print("  Error: Volume button target not found.")
        return False

    # 2. Inject CSS
    css_target = '/* ── Estilos de Voz Asistente AI ── */'
    if css_target in content:
        content = content.replace(css_target, CSS_INJECT, 1)
        print("  CSS styles injected.")
    else:
        print("  Error: CSS target not found.")
        return False

    # 3. Inject Audio Tag before </body>
    body_target = '</body>'
    if body_target in content:
        content = content.replace(body_target, AUDIO_TAG_HTML, 1)
        print("  Audio tag injected.")
    else:
        print("  Error: Body tag not found.")
        return False

    # 4. Inject JS logic
    js_target = '    if (window.speechSynthesis && window.speechSynthesis.onvoiceschanged !== undefined) {'
    if js_target in content:
        # Find the last occurrence in case there are multiple
        parts = content.rsplit(js_target, 1)
        if len(parts) == 2:
            content = parts[0] + JS_INJECT + parts[1]
            print("  JS logic injected.")
        else:
            print("  Error: Failed to split JS target.")
            return False
    else:
        print("  Error: JS target not found.")
        return False

    # Write changes back
    p.write_text(content, encoding="utf-8")
    print("  Successfully patched.")
    return True

def main():
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    print(f"Found {len(html_files)} HTML files to process.")
    success = 0
    for f in html_files:
        if patch_file(f):
            success += 1
    print(f"Patched {success}/{len(html_files)} files successfully.")

if __name__ == '__main__':
    main()
