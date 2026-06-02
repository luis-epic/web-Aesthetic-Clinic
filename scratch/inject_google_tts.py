import os

REPLACEMENT_BLOCK = """    let speakTimeout = null;
    let currentAudio = null;

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
          console.warn("Asistente AI - Reproducción bloqueada por navegador (autoplay) o error. Usando fallback nativo.", err);
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
      }, 100);
    }"""

def find_function_block(content, func_name="speakText"):
    idx = content.find(f"function {func_name}(")
    if idx == -1:
        return None
    
    # Locate preceding 'let speakTimeout' if any
    start_idx = content.rfind('let speakTimeout', 0, idx)
    if start_idx == -1:
        start_idx = idx
        
    # Locate braces block
    brace_start = content.find('{', idx)
    if brace_start == -1:
        return None
        
    brace_count = 1
    current_idx = brace_start + 1
    while brace_count > 0 and current_idx < len(content):
        char = content[current_idx]
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
        current_idx += 1
        
    if brace_count == 0:
        return content[start_idx:current_idx]
    return None

def update_file(file_path):
    print(f"Injecting Google TTS in: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"  Error reading file: {e}")
        return False

    func_block = find_function_block(content, "speakText")
    if func_block:
        content = content.replace(func_block, REPLACEMENT_BLOCK, 1)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("  Successfully injected Google TTS.")
            return True
        except Exception as e:
            print(f"  Error writing file: {e}")
            return False
    else:
        print("  Error: Could not locate speakText function block using brace parser.")
        return False

def main():
    html_files = []
    for root, dirs, files in os.walk('preview-web'):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print(f"Found {len(html_files)} HTML files to update.")
    success_count = 0
    for path in html_files:
        if update_file(path):
            success_count += 1
            
    print(f"Updated {success_count}/{len(html_files)} files successfully.")

if __name__ == '__main__':
    main()
