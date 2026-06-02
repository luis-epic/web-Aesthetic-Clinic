import os
import pathlib

root_dir = r"c:\Users\luis\Downloads\web-preview-navegable\preview-web"

# Define CSS, HTML and JS to inject
MUSIC_CSS = """
/* ── Estilos de Música de Espera Flotante (Idea 1) ── */
.ambient-player-container {
  position: fixed !important;
  bottom: 26px !important;
  left: 26px !important;
  display: flex !important;
  align-items: center !important;
  gap: 12px !important;
  background: rgba(255, 254, 251, 0.72) !important;
  backdrop-filter: blur(20px) saturate(110%) !important;
  -webkit-backdrop-filter: blur(20px) saturate(110%) !important;
  border: 1px solid rgba(176, 141, 79, 0.18) !important;
  box-shadow: 0 10px 30px -10px rgba(43, 39, 35, 0.15), 0 1px 3px rgba(0,0,0,0.05) !important;
  border-radius: 40px !important;
  padding: 8px 16px 8px 8px !important;
  z-index: 99999 !important;
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
  font-family: Jost, sans-serif !important;
  color: var(--ink) !important;
  max-width: 52px !important;
  overflow: hidden !important;
  white-space: nowrap !important;
}
.ambient-player-container:hover, .ambient-player-container.playing {
  max-width: 280px !important;
}
.ambient-play-btn {
  width: 36px !important;
  height: 36px !important;
  border-radius: 50% !important;
  background: linear-gradient(135deg, #b08d4f, #977634) !important;
  color: #fff !important;
  border: none !important;
  display: grid !important;
  place-items: center !important;
  cursor: pointer !important;
  box-shadow: 0 4px 10px rgba(151, 118, 52, 0.2) !important;
  transition: transform 0.25s, background 0.3s !important;
  flex-shrink: 0 !important;
  outline: none !important;
}
.ambient-play-btn:hover {
  transform: scale(1.08) !important;
}
.ambient-play-btn svg {
  width: 14px !important;
  height: 14px !important;
  stroke: currentColor !important;
  fill: currentColor !important;
}
.ambient-controls {
  display: flex !important;
  align-items: center !important;
  gap: 14px !important;
  opacity: 0 !important;
  transition: opacity 0.3s ease !important;
}
.ambient-player-container:hover .ambient-controls, .ambient-player-container.playing .ambient-controls {
  opacity: 1 !important;
}
.ambient-title {
  font-size: 0.76rem !important;
  font-weight: 500 !important;
  letter-spacing: 0.08em !important;
  text-transform: uppercase !important;
  color: var(--gold-deep) !important;
}
/* Equalizer */
.equalizer-waves {
  display: flex !important;
  align-items: flex-end !important;
  gap: 2.5px !important;
  height: 14px !important;
  width: 22px !important;
}
.wave-bar {
  width: 2.5px !important;
  background: var(--gold) !important;
  border-radius: 2px !important;
  height: 2px !important;
  transition: height 0.15s ease !important;
}
.ambient-player-container.playing .wave-bar {
  animation: equalize 1.2s ease-in-out infinite alternate !important;
}
.bar-1 { animation-delay: 0.1s !important; }
.bar-2 { animation-delay: 0.4s !important; }
.bar-3 { animation-delay: 0.25s !important; }
.bar-4 { animation-delay: 0.55s !important; }
@keyframes equalize {
  0% { height: 3px; }
  100% { height: 14px; }
}
/* Volume */
.ambient-volume-wrapper {
  display: flex !important;
  align-items: center !important;
  gap: 6px !important;
  border-left: 1px solid rgba(176, 141, 79, 0.15) !important;
  padding-left: 10px !important;
}
.ambient-volume-wrapper svg {
  width: 14px !important;
  height: 14px !important;
  color: var(--ink-soft) !important;
}
.ambient-volume-slider {
  -webkit-appearance: none !important;
  appearance: none !important;
  width: 50px !important;
  height: 3px !important;
  background: rgba(176, 141, 79, 0.15) !important;
  border-radius: 2px !important;
  outline: none !important;
}
.ambient-volume-slider::-webkit-slider-thumb {
  -webkit-appearance: none !important;
  appearance: none !important;
  width: 8px !important;
  height: 8px !important;
  border-radius: 50% !important;
  background: var(--gold) !important;
  cursor: pointer !important;
  transition: transform 0.15s !important;
}
.ambient-volume-slider::-webkit-slider-thumb:hover {
  transform: scale(1.3) !important;
}
/* Tooltip */
.ambient-tooltip {
  position: absolute !important;
  bottom: 58px !important;
  left: 0 !important;
  background: rgba(27, 26, 24, 0.92) !important;
  color: #f7f3ec !important;
  padding: 10px 32px 10px 14px !important;
  border-radius: 12px !important;
  font-size: 0.74rem !important;
  line-height: 1.4 !important;
  box-shadow: var(--shadow) !important;
  border: 1px solid rgba(176, 141, 79, 0.2) !important;
  width: 240px !important;
  z-index: 100000 !important;
  pointer-events: auto !important;
  transition: opacity 0.3s, transform 0.3s !important;
  transform: translateY(10px) !important;
  opacity: 0 !important;
  visibility: hidden !important;
}
.ambient-tooltip.show {
  opacity: 1 !important;
  visibility: visible !important;
  transform: translateY(0) !important;
}
.tooltip-close {
  position: absolute !important;
  top: 5px !important;
  right: 8px !important;
  background: none !important;
  border: none !important;
  color: rgba(255,255,255,0.4) !important;
  font-size: 1.1rem !important;
  cursor: pointer !important;
  outline: none !important;
}
.tooltip-close:hover {
  color: var(--gold-soft) !important;
}
@media (max-width: 480px) {
  .ambient-player-container {
    bottom: 96px !important;
    left: 16px !important;
  }
}
"""

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
  <source src="https://assets.mixkit.co/music/preview/mixkit-relaxing-in-the-spa-2194.mp3" type="audio/mp3">
</audio>
"""

MUSIC_JS = """
  // ── Música de Espera Flotante (Spa Lounge Ambient) ──
  (function initAmbientWaitingMusic() {
    const player = document.getElementById('ambientPlayer');
    const playBtn = document.getElementById('ambientPlayBtn');
    const audio = document.getElementById('ambientAudio');
    const volSlider = document.getElementById('ambientVolume');
    const tooltip = document.getElementById('ambientTooltip');
    const closeTooltip = document.getElementById('closeTooltipBtn');
    
    if (!player || !playBtn || !audio || !volSlider || !tooltip) return;
    
    const playIcon = playBtn.querySelector('.play-icon');
    const pauseIcon = playBtn.querySelector('.pause-icon');
    
    // Recopilar estado de localStorage
    const musicState = localStorage.getItem('waitingMusicPlaying') === 'true';
    const volumeState = localStorage.getItem('waitingMusicVolume') || '0.4';
    
    audio.volume = parseFloat(volumeState);
    volSlider.value = volumeState;
    
    // Mostrar tooltip después de 3.5 segundos si nunca se cerró y no se está reproduciendo
    const tooltipClosed = localStorage.getItem('waitingMusicTooltipClosed') === 'true';
    if (!tooltipClosed && !musicState) {
      setTimeout(() => {
        if (audio.paused) {
          tooltip.classList.add('show');
        }
      }, 3500);
    }
    
    if (closeTooltip) {
      closeTooltip.addEventListener('click', (e) => {
        e.stopPropagation();
        tooltip.classList.remove('show');
        localStorage.setItem('waitingMusicTooltipClosed', 'true');
      });
    }
    
    // Restaurar reproducción si corresponde
    if (musicState) {
      audio.play().then(() => {
        setPlayingState(true);
      }).catch(err => {
        console.log("Música de espera - Autoplay bloqueado o interactividad requerida.");
        setPlayingState(false);
      });
    }
    
    function setPlayingState(playing) {
      if (playing) {
        player.classList.add('playing');
        playIcon.style.display = 'none';
        pauseIcon.style.display = 'block';
        tooltip.classList.remove('show');
      } else {
        player.classList.remove('playing');
        playIcon.style.display = 'block';
        pauseIcon.style.display = 'none';
      }
    }
    
    playBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      if (audio.paused) {
        audio.play().then(() => {
          setPlayingState(true);
          localStorage.setItem('waitingMusicPlaying', 'true');
        }).catch(err => {
          console.error("Música de espera - Error de reproducción:", err);
        });
      } else {
        audio.pause();
        setPlayingState(false);
        localStorage.setItem('waitingMusicPlaying', 'false');
      }
    });
    
    volSlider.addEventListener('input', () => {
      audio.volume = volSlider.value;
      localStorage.setItem('waitingMusicVolume', volSlider.value);
    });
  })();
"""

def patch_file(filepath):
    print(f"Processing: {filepath}")
    p = pathlib.Path(filepath)
    content = p.read_text(encoding="utf-8")
    
    # Normalize line endings
    content = content.replace('\r\n', '\n')
    
    if "initAmbientWaitingMusic" in content:
        print("  Already patched. Skipping.")
        return False
        
    # 1. Inject HTML before </body>
    body_close = '</body>'
    if body_close in content:
        content = content.replace(body_close, MUSIC_HTML + '\n' + body_close, 1)
        print("  HTML injected.")
    else:
        print("  Error: Closing body tag not found.")
        return False

    # 2. Inject CSS before </style>
    first_style_close = content.find('</style>')
    if first_style_close != -1:
        content = content[:first_style_close] + MUSIC_CSS + content[first_style_close:]
        print("  CSS injected.")
    else:
        print("  Error: Closing style tag not found.")
        return False

    # 3. Inject JS before </script>
    last_script_close = content.rfind('</script>')
    if last_script_close != -1:
        content = content[:last_script_close] + MUSIC_JS + '\n' + content[last_script_close:]
        print("  JS injected.")
    else:
        print("  Error: Closing script tag not found.")
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
