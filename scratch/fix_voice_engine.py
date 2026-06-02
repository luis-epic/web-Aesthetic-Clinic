import os
import re
import pathlib

"""
Fix voice engine across all HTML files.

Root causes of silence:
1. Google Translate TTS URL (translate.google.com/translate_tts) is blocked by CORS
   when called from localhost or any non-Google origin. The Audio() fails silently.
2. The SpeechSynthesis fallback calls getVoices() which returns [] in Chrome on first
   call. Voices load asynchronously, but speakTextFallback already ran with empty list.
3. The voice IIFE is outside DOMContentLoaded, and voices may not be ready yet.

Fix: Replace the entire voice engine with a robust native SpeechSynthesis implementation
that properly waits for voices to load before speaking.
"""

OLD_VOICE_BLOCK_START = '  // ── Soporte de Voz del Asistente AI (Speech-to-Text & Text-to-Speech con Google TTS y Fallback Femenino) ──'
OLD_VOICE_BLOCK_END = '  })();'

NEW_VOICE_JS = """
  // ── Soporte de Voz del Asistente AI (Voz Femenina Nativa) ──
  (function initVoiceChatSupport() {
    const micBtn = document.getElementById('aiChatMic');
    const volBtn = document.getElementById('aiChatVolume');
    const chatInput = document.getElementById('aiChatInput');

    if (!micBtn || !volBtn || !chatInput) {
      console.warn('Asistente AI - Elementos de voz no encontrados en el DOM.');
      return;
    }

    let voiceEnabled = false;
    let recognition = null;
    let isListening = false;
    let cachedVoices = [];
    let selectedVoice = null;

    // ── Precarga de voces ──
    // Chrome carga las voces de forma asíncrona. Debemos esperarlas.
    function loadVoices() {
      cachedVoices = window.speechSynthesis ? window.speechSynthesis.getVoices() : [];
      if (cachedVoices.length > 0) {
        selectedVoice = pickFemaleSpanishVoice(cachedVoices);
        if (selectedVoice) {
          console.log('Asistente AI - Voz preseleccionada:', selectedVoice.name, selectedVoice.lang);
        } else {
          console.warn('Asistente AI - No se encontró voz femenina en español. Se usará la voz por defecto.');
        }
      }
      return cachedVoices.length > 0;
    }

    // Intentar cargar ahora
    loadVoices();

    // Chrome dispara este evento cuando las voces están listas
    if (window.speechSynthesis && window.speechSynthesis.onvoiceschanged !== undefined) {
      window.speechSynthesis.onvoiceschanged = function() {
        loadVoices();
      };
    }

    function pickFemaleSpanishVoice(voices) {
      const spanishVoices = voices.filter(function(v) {
        return v.lang && v.lang.replace('_', '-').toLowerCase().startsWith('es');
      });

      if (spanishVoices.length === 0) return null;

      var maleNames = ['pablo', 'raul', 'raúl', 'david', 'sabino', 'mateo', 'jorge',
                       'andrés', 'andres', 'diego', 'carlos', 'miguel', 'hombre',
                       'male', 'guy', 'boy', 'hector', 'héctor', 'enrique'];
      var femaleNames = ['helena', 'laura', 'lucia', 'lucía', 'elena', 'monica',
                         'mónica', 'paulina', 'marisol', 'angela', 'ángela',
                         'zira', 'sara', 'juana', 'silvia', 'teresa', 'ana',
                         'sabina', 'hilda', 'elvira', 'conchita', 'lupe',
                         'penelope', 'penélope', 'miren', 'ines', 'inés',
                         'female', 'mujer', 'google'];

      // Filtrar voces masculinas
      var nonMaleVoices = spanishVoices.filter(function(v) {
        var n = v.name.toLowerCase();
        return !maleNames.some(function(m) { return n.indexOf(m) !== -1; });
      });

      // 1. Buscar voz femenina es-ES
      var voice = nonMaleVoices.find(function(v) {
        var n = v.name.toLowerCase();
        var isEsES = v.lang.replace('_', '-').toLowerCase().startsWith('es-es');
        return isEsES && femaleNames.some(function(f) { return n.indexOf(f) !== -1; });
      });
      if (voice) return voice;

      // 2. Buscar voz femenina en cualquier español
      voice = nonMaleVoices.find(function(v) {
        var n = v.name.toLowerCase();
        return femaleNames.some(function(f) { return n.indexOf(f) !== -1; });
      });
      if (voice) return voice;

      // 3. Buscar cualquier voz no-masculina es-ES
      voice = nonMaleVoices.find(function(v) {
        return v.lang.replace('_', '-').toLowerCase().startsWith('es-es');
      });
      if (voice) return voice;

      // 4. Cualquier voz no-masculina española
      if (nonMaleVoices.length > 0) return nonMaleVoices[0];

      // 5. Cualquier voz española
      return spanishVoices[0];
    }

    // ── Text-to-Speech con reintentos de carga de voces ──
    function speakText(text) {
      if (!window.speechSynthesis) {
        console.warn('Asistente AI - SpeechSynthesis no soportado.');
        return;
      }

      // Cancelar cualquier locución previa
      window.speechSynthesis.cancel();

      // Limpiar HTML
      var cleanText = text.replace(/<[^>]*>/g, '');
      cleanText = cleanText.replace(/&nbsp;/g, ' ');
      cleanText = cleanText.replace(/&lt;/g, '<').replace(/&gt;/g, '>');
      cleanText = cleanText.replace(/&amp;/g, '&');
      cleanText = cleanText.replace(/\\*\\*/g, '');
      cleanText = cleanText.trim();

      if (!cleanText) {
        console.log('Asistente AI - Texto vacío.');
        return;
      }

      console.log('Asistente AI - Preparando lectura:', cleanText.substring(0, 80) + '...');

      // Si las voces aún no han cargado, esperamos un poco
      if (cachedVoices.length === 0) {
        loadVoices();
      }

      // Dividir en chunks para evitar cortes en textos largos (Chrome corta a ~300 chars)
      var chunks = splitIntoChunks(cleanText, 200);
      var chunkIndex = 0;

      function speakNextChunk() {
        if (chunkIndex >= chunks.length || !voiceEnabled) return;

        var utterance = new SpeechSynthesisUtterance(chunks[chunkIndex]);
        utterance.lang = 'es-ES';
        utterance.rate = 1.0;
        utterance.pitch = 1.05;

        // Re-check voice availability
        if (!selectedVoice) {
          loadVoices();
        }
        if (selectedVoice) {
          utterance.voice = selectedVoice;
          console.log('Asistente AI - Usando voz:', selectedVoice.name);
        } else {
          console.log('Asistente AI - Usando voz por defecto del sistema.');
        }

        utterance.onend = function() {
          chunkIndex++;
          if (chunkIndex < chunks.length && voiceEnabled) {
            // Pequeño delay entre chunks para estabilidad en Chrome
            setTimeout(speakNextChunk, 80);
          }
        };

        utterance.onerror = function(e) {
          console.error('Asistente AI - Error de locución:', e.error);
          // Intentar siguiente chunk
          chunkIndex++;
          if (chunkIndex < chunks.length && voiceEnabled) {
            setTimeout(speakNextChunk, 100);
          }
        };

        // Chrome bug: speechSynthesis puede quedarse en pausa
        window.speechSynthesis.resume();
        window.speechSynthesis.speak(utterance);

        // Chrome bug: locuciones largas se paran. Keepalive timer.
        var keepAlive = setInterval(function() {
          if (!window.speechSynthesis.speaking) {
            clearInterval(keepAlive);
          } else {
            window.speechSynthesis.pause();
            window.speechSynthesis.resume();
          }
        }, 10000);

        utterance.onend = function() {
          clearInterval(keepAlive);
          chunkIndex++;
          if (chunkIndex < chunks.length && voiceEnabled) {
            setTimeout(speakNextChunk, 80);
          }
        };
      }

      // Delay de 200ms para dar tiempo a Chrome a cargar voces si es la primera vez
      setTimeout(function() {
        if (cachedVoices.length === 0) {
          loadVoices();
        }
        speakNextChunk();
      }, 200);
    }

    function splitIntoChunks(text, maxLen) {
      var chunks = [];
      var sentences = text.match(/[^.!?]+[.!?]*/g) || [text];
      var current = '';

      for (var i = 0; i < sentences.length; i++) {
        var s = sentences[i];
        if ((current + s).length > maxLen) {
          if (current.trim()) chunks.push(current.trim());
          current = s;
        } else {
          current += ' ' + s;
        }
      }
      if (current.trim()) chunks.push(current.trim());
      return chunks;
    }

    // ── Volumen toggle ──
    volBtn.addEventListener('click', function() {
      voiceEnabled = !voiceEnabled;
      volBtn.classList.toggle('active', voiceEnabled);
      if (voiceEnabled) {
        volBtn.setAttribute('aria-label', 'Desactivar lectura de voz');
        // Forzar carga de voces con interacción del usuario (requerido por Chrome)
        if (cachedVoices.length === 0) {
          loadVoices();
        }
        speakText('Lectura de voz activada');
      } else {
        volBtn.setAttribute('aria-label', 'Activar lectura de voz');
        window.speechSynthesis.cancel();
      }
    });

    window.speakAiResponse = function(text) {
      if (voiceEnabled) {
        speakText(text);
      }
    };

    // ── Speech-to-Text (Micrófono) ──
    var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.lang = 'es-ES';
      recognition.interimResults = false;

      recognition.onstart = function() {
        isListening = true;
        micBtn.classList.add('listening');
        chatInput.placeholder = 'Escuchando...';
      };

      recognition.onresult = function(e) {
        var transcript = e.results[0][0].transcript;
        chatInput.value = transcript;
        chatInput.focus();
      };

      recognition.onerror = function(e) {
        console.error('Speech recognition error:', e.error);
        stopRecognition();
      };

      recognition.onend = function() {
        stopRecognition();
      };

      function stopRecognition() {
        isListening = false;
        micBtn.classList.remove('listening');
        chatInput.placeholder = 'Escribe un mensaje...';
        try { recognition.stop(); } catch(err) {}
      }

      micBtn.addEventListener('click', function(e) {
        e.preventDefault();
        if (isListening) {
          stopRecognition();
        } else {
          try {
            recognition.start();
          } catch(err) {
            console.error('Failed to start speech recognition:', err);
          }
        }
      });
    } else {
      micBtn.style.display = 'none';
    }

    console.log('Asistente AI - Sistema de voz inicializado correctamente.');
  })();
"""


def patch_file(filepath):
    print(f"Processing: {filepath}")
    p = pathlib.Path(filepath)
    content = p.read_text(encoding='utf-8')

    # Find and replace the old voice block
    start_marker = '// ── Soporte de Voz del Asistente AI'
    end_marker_iife = '  })();'

    start_idx = content.find(start_marker)
    if start_idx == -1:
        print("  ERROR: Voice block not found.")
        return False

    # Find the matching end of the IIFE after start
    # We need the LAST })(); that closes the IIFE
    end_search_start = start_idx
    end_idx = -1
    # Find all })(); after start and take the last one before </script>
    script_close = content.find('</script>', start_idx)
    if script_close == -1:
        print("  ERROR: </script> not found after voice block.")
        return False

    # Search for the closing })(); of the IIFE
    search_area = content[start_idx:script_close]
    # Find the last occurrence of })(); in this area
    last_iife_close = search_area.rfind('})();')
    if last_iife_close == -1:
        print("  ERROR: IIFE closing })(); not found.")
        return False

    end_idx = start_idx + last_iife_close + len('})();')

    old_block = content[start_idx:end_idx]
    print(f"  Found voice block: {len(old_block)} chars (lines ~{content[:start_idx].count(chr(10))+1} to ~{content[:end_idx].count(chr(10))+1})")

    content = content[:start_idx] + NEW_VOICE_JS.strip() + content[end_idx:]

    p.write_text(content, encoding='utf-8')
    print("  Successfully patched.")
    return True


def main():
    base_dir = r"c:\Users\luis\Downloads\web-preview-navegable\preview-web"
    html_files = []
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if f.endswith('.html'):
                html_files.append(os.path.join(root, f))

    print(f"Found {len(html_files)} HTML files.")
    success = 0
    for f in html_files:
        if patch_file(f):
            success += 1
    print(f"\nPatched {success}/{len(html_files)} files.")


if __name__ == '__main__':
    main()
