import os
import re

root_dir = r"c:\Users\luis\Downloads\web-preview-navegable\preview-web"

CSS_COMMENT = "/* ── Estilos de Voz Asistente AI ── */"
CSS_INJECT = """/* ── Estilos de Música de Espera Asistente ── */
.ai-chat-music-btn {
  background: none;
  border: none;
  color: rgba(0,0,0,0.35) !important;
  cursor: pointer;
  display: grid;
  place-items: center;
  transition: all 0.3s ease;
  padding: 4px;
  outline: none;
  margin-right: 6px;
}
.ai-chat-music-btn:hover {
  color: #977634 !important;
  transform: scale(1.08) !important;
}
.ai-chat-music-btn.active {
  color: #b08d4f !important;
}
"""

HTML_TARGET = '<button class="ai-chat-volume-btn" id="aiChatVolume"'
HTML_INJECT = """<button class="ai-chat-music-btn" id="aiChatMusic" aria-label="Activar música de espera" style="background:none; border:none; color:rgba(0,0,0,0.35); cursor:pointer; display:grid; place-items:center; transition:all 0.3s; padding: 4px; outline:none; margin-right: 6px;">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:19px; height:19px;" class="music-icon">
            <path d="M9 18V5l12-2v13"></path>
            <circle cx="6" cy="18" r="3"></circle>
            <circle cx="18" cy="16" r="3"></circle>
          </svg>
        </button>
        <button class="ai-chat-volume-btn" id="aiChatVolume\""""

AUDIO_INJECT = """<audio id="waitingMusicAudio" loop preload="auto">
  <source src="/waiting_music.mp3" type="audio/mp3">
</audio>
</body>"""

JS_TARGET = """    const micBtn = document.getElementById('aiChatMic');
    const volBtn = document.getElementById('aiChatVolume');
    const chatInput = document.getElementById('aiChatInput');"""

JS_INJECT = """    const micBtn = document.getElementById('aiChatMic');
    const volBtn = document.getElementById('aiChatVolume');
    const chatInput = document.getElementById('aiChatInput');

    // ── Configuración de Música de Espera Asistente ──
    const musicBtn = document.getElementById('aiChatMusic');
    const musicAudio = document.getElementById('waitingMusicAudio');
    
    if (musicBtn && musicAudio) {
      let musicPlaying = localStorage.getItem('waitingMusicPlaying') === 'true';
      musicAudio.volume = 0.25; // Muy suave de fondo
      musicBtn.classList.toggle('active', musicPlaying);
      
      if (musicPlaying) {
        musicAudio.play().then(() => {
          musicBtn.setAttribute('aria-label', 'Desactivar música de espera');
        }).catch(err => {
          console.log("Música de espera - Autoplay bloqueado por el navegador.");
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
            console.error("Error al reproducir música de espera:", err);
          });
        } else {
          musicBtn.setAttribute('aria-label', 'Activar música de espera');
          musicAudio.pause();
        }
      });
    }"""

def patch_file(filepath):
    print(f"Processing: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Normalize line endings
    content = content.replace('\r\n', '\n')
    
    if "aiChatMusic" in content:
        print("  Already contains music logic. Skipping.")
        return False
        
    # 1. Inject CSS
    if CSS_COMMENT in content:
        content = content.replace(CSS_COMMENT, CSS_INJECT + "\n" + CSS_COMMENT, 1)
        print("  CSS injected.")
    else:
        print("  Error: CSS comment target not found.")
        return False
        
    # 2. Inject HTML button
    if HTML_TARGET in content:
        content = content.replace(HTML_TARGET, HTML_INJECT, 1)
        print("  HTML button injected.")
    else:
        print("  Error: HTML button target not found.")
        return False
        
    # 3. Inject Audio Tag
    if "</body>" in content:
        content = content.replace("</body>", AUDIO_INJECT, 1)
        print("  Audio tag injected.")
    else:
        print("  Error: Closing body tag not found.")
        return False
        
    # 4. Inject JS logic
    if JS_TARGET in content:
        content = content.replace(JS_TARGET, JS_INJECT, 1)
        print("  JS logic injected.")
    else:
        print("  Error: JS targets not found.")
        return False
        
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
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
