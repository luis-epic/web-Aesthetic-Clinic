import os
import re
import pathlib

# Define the CSS to inject
VOICE_CSS = """
/* ── Estilos de Voz Asistente AI ── */
.ai-chat-volume-btn:hover {
  color: #fff !important;
  transform: scale(1.08) !important;
}
.ai-chat-volume-btn.active {
  color: var(--gold-soft) !important;
}
.ai-chat-volume-btn.active .vol-slash {
  opacity: 0 !important;
}
.ai-chat-mic:hover {
  color: var(--gold-deep) !important;
  transform: scale(1.1) !important;
}
.ai-chat-mic.listening {
  color: #ff4d4d !important;
  animation: micPulse 1.5s infinite !important;
}
@keyframes micPulse {
  0% { transform: scale(1); filter: drop-shadow(0 0 2px rgba(255, 77, 77, 0.4)); }
  50% { transform: scale(1.15); filter: drop-shadow(0 0 8px rgba(255, 77, 77, 0.8)); }
  100% { transform: scale(1); filter: drop-shadow(0 0 2px rgba(255, 77, 77, 0.4)); }
}
"""

VOICE_JS = """
  // ── Soporte de Voz del Asistente AI (Speech-to-Text & Text-to-Speech con Google TTS y Fallback Femenino) ──
  (function initVoiceChatSupport() {
    const micBtn = document.getElementById('aiChatMic');
    const volBtn = document.getElementById('aiChatVolume');
    const chatInput = document.getElementById('aiChatInput');

    if (!micBtn || !volBtn || !chatInput) return;

    let voiceEnabled = false;
    let recognition = null;
    let isListening = false;
    let speakTimeout = null;
    let currentAudio = null;

    // 1. Configuración de Text-to-Speech (Lectura en voz alta)
    volBtn.addEventListener('click', () => {
      voiceEnabled = !voiceEnabled;
      volBtn.classList.toggle('active', voiceEnabled);
      if (voiceEnabled) {
        volBtn.setAttribute('aria-label', 'Desactivar lectura de voz');
        speakText("Lectura de voz activada");
      } else {
        volBtn.setAttribute('aria-label', 'Activar lectura de voz');
        if (currentAudio) {
          console.log("Asistente AI - Deteniendo audio previo.");
          currentAudio.pause();
          currentAudio = null;
        }
        if (window.speechSynthesis) {
          window.speechSynthesis.cancel();
        }
        if (speakTimeout) {
          clearTimeout(speakTimeout);
        }
      }
    });

    function speakText(text) {
      console.log("Asistente AI - Preparando locución de voz...");
      
      // Detener cualquier audio previo
      if (currentAudio) {
        console.log("Asistente AI - Deteniendo audio previo.");
        currentAudio.pause();
        currentAudio = null;
      }
      if (window.speechSynthesis) {
        window.speechSynthesis.cancel();
      }
      if (speakTimeout) {
        clearTimeout(speakTimeout);
      }

      // Limpiar etiquetas HTML y entidades
      let cleanText = text.replace(/<[^>]*>/g, '');
      cleanText = cleanText.replace(/&nbsp;/g, ' ');
      cleanText = cleanText.replace(/&lt;/g, '<').replace(/&gt;/g, '>');
      cleanText = cleanText.trim();

      if (!cleanText) {
        console.log("Asistente AI - Texto vacío. No hay nada que hablar.");
        return;
      }

      // Dividir el texto en fragmentos de máximo 180 caracteres para la API de Google TTS
      const chunks = [];
      const sentences = cleanText.match(/[^.!?]+[.!?]*/g) || [cleanText];
      
      let currentChunk = "";
      for (let sentence of sentences) {
        if ((currentChunk + sentence).length > 180) {
          if (currentChunk) chunks.push(currentChunk.trim());
          currentChunk = sentence;
        } else {
          currentChunk += " " + sentence;
        }
      }
      if (currentChunk) chunks.push(currentChunk.trim());

      let chunkIndex = 0;

      function playNextChunk() {
        if (!voiceEnabled) {
          currentAudio = null;
          return;
        }
        if (chunkIndex >= chunks.length) {
          console.log("Asistente AI - Finalizó la lectura de todos los fragmentos.");
          currentAudio = null;
          return;
        }

        const chunkText = chunks[chunkIndex];
        console.log("Asistente AI - Reproduciendo fragmento " + (chunkIndex + 1) + " de " + chunks.length + ":", chunkText);
        
        const url = `https://translate.google.com/translate_tts?ie=UTF-8&tl=es-ES&client=tw-ob&q=${encodeURIComponent(chunkText)}`;
        
        currentAudio = new Audio(url);
        
        currentAudio.addEventListener('ended', () => {
          chunkIndex++;
          playNextChunk();
        });

        currentAudio.addEventListener('error', (e) => {
          console.error("Asistente AI - Error al reproducir audio de Google TTS. Usando fallback nativo.", e);
          speakTextFallback(cleanText);
        });

        currentAudio.play().catch(err => {
          console.warn("Asistente AI - Reproducción bloqueada por navegador o error. Usando fallback nativo.", err);
          speakTextFallback(cleanText);
        });
      }

      // Iniciar la reproducción del primer fragmento
      playNextChunk();
    }

    function speakTextFallback(cleanText) {
      if (!window.speechSynthesis) {
        console.warn("Asistente AI - Fallback no soportado.");
        return;
      }
      
      console.log("Asistente AI - Iniciando fallback de voz nativo con:", cleanText);
      speakTimeout = setTimeout(() => {
        const utterance = new SpeechSynthesisUtterance(cleanText);
        utterance.lang = 'es-ES';

        const voices = window.speechSynthesis.getVoices();
        const spanishVoices = voices.filter(v => v.lang.startsWith('es'));
        
        const maleKeywords = ['male', 'pablo', 'raul', 'raúl', 'david', 'sabino', 'mateo', 'jorge', 'hombre', 'guy', 'boy'];
        const femaleKeywords = ['female', 'helena', 'laura', 'lucia', 'elena', 'monica', 'mónica', 'paulina', 'marisol', 'angela', 'ángela', 'google', 'zira', 'sara', 'juana', 'silvia', 'teresa', 'ana', 'local', 'sabina', 'hilda'];

        const potentialFemaleVoices = spanishVoices.filter(v => {
          const nameLower = v.name.toLowerCase();
          return !maleKeywords.some(keyword => nameLower.includes(keyword));
        });

        let spanishVoice = potentialFemaleVoices.find(v => {
          const nameLower = v.name.toLowerCase();
          return femaleKeywords.some(keyword => nameLower.includes(keyword)) && v.lang.toLowerCase().replace('_', '-').startsWith('es-es');
        });
        if (!spanishVoice) {
          spanishVoice = potentialFemaleVoices.find(v => {
            const nameLower = v.name.toLowerCase();
            return femaleKeywords.some(keyword => nameLower.includes(keyword));
          });
        }
        if (!spanishVoice) {
          spanishVoice = potentialFemaleVoices.find(v => v.lang.toLowerCase().replace('_', '-').startsWith('es-es'));
        }
        if (!spanishVoice) {
          spanishVoice = potentialFemaleVoices[0];
        }
        if (!spanishVoice) {
          spanishVoice = spanishVoices[0];
        }
        
        if (spanishVoice) {
          console.log("Asistente AI (Fallback) - Voz seleccionada:", spanishVoice.name);
          utterance.voice = spanishVoice;
        }

        utterance.rate = 1.05;
        utterance.pitch = 1.0;

        window.speechSynthesis.resume();
        window.speechSynthesis.speak(utterance);
      }, 150);
    }

    window.speakAiResponse = function(text) {
      if (voiceEnabled) {
        speakText(text);
      }
    };

    // 2. Configuración de Speech-to-Text (Dictado por micrófono)
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.lang = 'es-ES';
      recognition.interimResults = false;

      recognition.onstart = () => {
        isListening = true;
        micBtn.classList.add('listening');
        chatInput.placeholder = "Escuchando...";
      };

      recognition.onresult = (e) => {
        const transcript = e.results[0][0].transcript;
        chatInput.value = transcript;
        chatInput.focus();
      };

      recognition.onerror = (e) => {
        console.error("Speech recognition error:", e.error);
        stopRecognition();
      };

      recognition.onend = () => {
        stopRecognition();
      };

      function stopRecognition() {
        isListening = false;
        micBtn.classList.remove('listening');
        chatInput.placeholder = "Escribe un mensaje...";
        if (recognition) {
          try { recognition.stop(); } catch(err) {}
        }
      }

      micBtn.addEventListener('click', (e) => {
        e.preventDefault();
        if (isListening) {
          stopRecognition();
        } else {
          try {
            recognition.start();
          } catch(err) {
            console.error("Failed to start speech recognition:", err);
          }
        }
      });
    } else {
      micBtn.style.display = 'none';
    }

    if (window.speechSynthesis && window.speechSynthesis.onvoiceschanged !== undefined) {
      window.speechSynthesis.onvoiceschanged = () => {
        window.speechSynthesis.getVoices();
      };
    }
  })();
"""

VOLUME_BTN_HTML = """      <button class="ai-chat-volume-btn" id="aiChatVolume" aria-label="Activar lectura de voz" style="background:none; border:none; color:rgba(255,255,255,0.6); cursor:pointer; display:grid; place-items:center; transition:all 0.3s; padding: 4px; outline:none; margin-right: 6px;">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:19px; height:19px;" class="vol-icon">
          <line x1="1" y1="1" x2="23" y2="23" class="vol-slash" style="transition: opacity 0.25s ease; stroke: currentColor;"></line>
          <path d="M9 9v6a3 3 0 0 0 3 3h1.586l4.707 4.707A1 1 0 0 0 20 22V4a1 1 0 0 0-1.707-.707L13.586 8H12a3 3 0 0 0-3 3z"></path>
        </svg>
      </button>
      <button class="ai-chat-close" id="aiChatClose" aria-label="Cerrar Asistente AI">&times;</button>"""

MIC_BTN_HTML = """      <button id="aiChatMic" aria-label="Hablar por voz" class="ai-chat-mic" style="background: none; border: none; color: var(--gold); cursor: pointer; display: grid; place-items: center; transition: color 0.3s, transform 0.2s; outline: none; margin-right: 6px; padding: 4px;">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width: 20px; height: 20px; stroke: currentColor;">
          <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
          <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
          <line x1="12" y1="19" x2="12" y2="23"></line>
          <line x1="8" y1="23" x2="16" y2="23"></line>
        </svg>
      </button>
      <button id="aiChatSend" aria-label="Enviar mensaje">"""

def patch_file(filepath):
    print(f"Processing: {filepath}")
    p = pathlib.Path(filepath)
    content = p.read_text(encoding="utf-8")
    
    # Normalize line endings
    content = content.replace('\r\n', '\n')
    
    if "initVoiceChatSupport" in content:
        print("  Already patched. Skipping.")
        return False
        
    # 1. Volume button
    close_btn = '<button class="ai-chat-close" id="aiChatClose" aria-label="Cerrar Asistente AI">&times;</button>'
    if close_btn in content:
        content = content.replace(close_btn, VOLUME_BTN_HTML, 1)
        print("  Volume button injected.")
    else:
        print("  Warning: Close button not found. Trying regex.")
        # Try finding button by id
        content, count = re.subn(r'<button[^>]*id="aiChatClose"[^>]*>.*?</button>', VOLUME_BTN_HTML, content, count=1)
        if count > 0:
            print("  Volume button injected via regex.")
        else:
            print("  Error: Could not inject volume button.")
            return False

    # 2. Mic button
    send_btn = '<button id="aiChatSend" aria-label="Enviar mensaje">'
    if send_btn in content:
        content = content.replace(send_btn, MIC_BTN_HTML, 1)
        print("  Mic button injected.")
    else:
        print("  Warning: Send button not found. Trying regex.")
        content, count = re.subn(r'<button[^>]*id="aiChatSend"[^>]*>', MIC_BTN_HTML, content, count=1)
        if count > 0:
            print("  Mic button injected via regex.")
        else:
            print("  Error: Could not inject mic button.")
            return False

    # 3. CSS styles
    first_style_close = content.find('</style>')
    if first_style_close != -1:
        content = content[:first_style_close] + VOICE_CSS + content[first_style_close:]
        print("  CSS injected.")
    else:
        print("  Error: Closing style tag not found.")
        return False

    # 4. Typing timeouts
    pattern_850 = r'(typing\.remove\(\);\s*const\s+botResponse\s*=\s*generateResponse\(text\);\s*addMessage\(botResponse,\s*[\'"]bot[\'"]\);)(\s*\}, \s*850\);)'
    pattern_800 = r'(typing\.remove\(\);\s*const\s+botResponse\s*=\s*generateResponse\(text\);\s*addMessage\(botResponse,\s*[\'"]bot[\'"]\);)(\s*\}, \s*800\);)'
    
    content, count_850 = re.subn(pattern_850, r'\1\n      if (window.speakAiResponse) { window.speakAiResponse(botResponse); }\2', content)
    content, count_800 = re.subn(pattern_800, r'\1\n      if (window.speakAiResponse) { window.speakAiResponse(botResponse); }\2', content)
    print(f"  Typing timeouts patched (850ms: {count_850}, 800ms: {count_800}).")
    
    if count_850 == 0 or count_800 == 0:
        print("  Warning: Could not patch typing timeouts using standard regex.")
        # Fallback regex search for addMessage(botResponse, 'bot')
        fallback_pattern = r'(typing\.remove\(\);\s*const\s+botResponse\s*=\s*generateResponse\(text\);\s*addMessage\(botResponse,\s*[\'"]bot[\'"]\);)'
        content, fallback_count = re.subn(fallback_pattern, r'\1\n      if (window.speakAiResponse) { window.speakAiResponse(botResponse); }', content)
        print(f"  Fallback timeout injection count: {fallback_count}")

    # 5. JS code block
    last_script_close = content.rfind('</script>')
    if last_script_close != -1:
        content = content[:last_script_close] + VOICE_JS + '\n' + content[last_script_close:]
        print("  JS engine injected.")
    else:
        print("  Error: Closing script tag not found.")
        return False

    p.write_text(content, encoding="utf-8")
    print("  Successfully written changes.")
    return True

def main():
    base_dir = r"c:\Users\luis\Downloads\web-preview-navegable\preview-web"
    html_files = []
    for root, dirs, files in os.walk(base_dir):
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
