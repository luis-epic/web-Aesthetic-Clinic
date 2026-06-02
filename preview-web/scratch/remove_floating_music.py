import os
import pathlib
import re

root_dir = r"c:\Users\luis\Downloads\web-preview-navegable\preview-web"

# The elements to remove
MUSIC_HTML = """
<!-- Widget Música de Espera Flotante -->
<div class="ambient-player-container" id="ambientPlayer">
  <button class="ambient-play-btn" id="ambientPlayBtn" aria-label="Reproducir música de espera">
    <svg class="play-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <polygon points="5 3 19 12 5 21 5 3"></polygon>
    </svg>
    <svg class="pause-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:none;">
      <rect x="6" y="4" width="4" height="16"></rect>
      <rect x="14" y="4" width="4" height="16"></rect>
    </svg>
  </button>
  
  <div class="ambient-controls">
    <span class="ambient-title">Música de Espera</span>
    <div class="equalizer-waves">
      <span class="wave-bar bar-1"></span>
      <span class="wave-bar bar-2"></span>
      <span class="wave-bar bar-3"></span>
      <span class="wave-bar bar-4"></span>
    </div>
    
    <div class="ambient-volume-wrapper">
      <svg class="vol-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M11 5L6 9H2v6h4l5 4V5zM15.54 8.46a5 5 0 0 1 0 7.07"></path>
      </svg>
      <input type="range" class="ambient-volume-slider" id="ambientVolume" min="0" max="1" step="0.1" value="0.4" aria-label="Volumen música">
    </div>
  </div>
  
  <div class="ambient-tooltip" id="ambientTooltip">
    ¿Te gustaría ambientar tu visita con música de espera relajante?
    <button class="tooltip-close" id="closeTooltipBtn" aria-label="Cerrar sugerencia">&times;</button>
  </div>
</div>

<audio id="ambientAudio" loop preload="auto">
  <source src="https://incompetech.com/music/royalty-free/mp3-royaltyfree/Gymnopedie%20No%201.mp3" type="audio/mp3">
</audio>
"""

# Let's clean line breaks in comparison
def clean_str(s):
    return s.strip().replace('\r\n', '\n')

removed_count = 0
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Normalize
            content = content.replace('\r\n', '\n')
            
            updated = False
            
            # 1. Remove HTML
            html_cleaned = clean_str(MUSIC_HTML)
            if html_cleaned in content:
                content = content.replace(html_cleaned, "")
                updated = True
            else:
                # Try partial match by id
                content, count = re.subn(r'<!-- Widget Música de Espera Flotante -->.*?<audio id="ambientAudio".*?</audio>', '', content, flags=re.DOTALL)
                if count > 0:
                    updated = True
            
            # 2. Remove CSS
            content, count_css = re.subn(r'/\* ── Estilos de Música de Espera Flotante \(Idea 1\) ── \*/.*?\n\}\n(?=\n|$)|\/\* ── Estilos de Música de Espera Flotante \(Idea 1\) ── \*\/.*?\}', '', content, flags=re.DOTALL)
            if count_css > 0:
                updated = True
                
            # 3. Remove JS
            content, count_js = re.subn(r'// ── Música de Espera Flotante \(Spa Lounge Ambient\) ──.*?\n\s*\}\)\(\);', '', content, flags=re.DOTALL)
            if count_js > 0:
                updated = True
                
            if updated:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Removed floating music widget from: {os.path.relpath(filepath, root_dir)}")
                removed_count += 1

print(f"Successfully cleaned floating player from {removed_count} files.")
