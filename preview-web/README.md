# 🏥 Clínica Médica Estética — Dra. Iratxe Díaz

Sitio web estático de alta fidelidad, interactivo y premium de la clínica de medicina estética de la Dra. Iratxe Díaz (centros en Bilbao y Vitoria-Gasteiz).

Este proyecto ha sido optimizado con características interactivas avanzadas, consistencia de marca oficial, y una arquitectura limpia para despliegues rápidos de producción.

---

## 🌟 Características Principales

### 1. 🤖 Asistente Virtual AI Integrado (Conversacional)
*   **Widget Glassmorphic:** Interfaz elegante con efecto cristal esmerilado (`backdrop-filter: blur(25px)`), halo dorado expansivo e indicador de estado "En línea" pulsante en verde.
*   **Contexto Médico Completo:** Responde de forma inmediata y profesional a consultas sobre tratamientos (Ácido Hialurónico, Bótox, CoolSculpting, etc.), ubicaciones de clínicas, teléfonos, correos y horarios.
*   **Sugerencias con 1-Clic:** Chips deslizables horizontales con preguntas predefinidas para agilizar el flujo de atención del paciente.
*   **Simulación de Escritura:** Indicador de escritura animado (`.ai-typing-indicator`) que recrea una conversación humana realista.

### 📸 2. Comparador Interactivo "Antes y Después" (Drag Engine)
*   **Arrastre Suave (Desktop & Touch):** Deslizador vertical de barra de oro y tirador circular minimalista que funciona al hacer clic o arrastrar el dedo en cualquier punto de la imagen.
*   **Visuales en Alta Resolución:** Tres casos reales con alineación milimétrica al píxel:
    *   👄 **Aumento de Labios**
    *   ✨ **Armonización Facial**
    *   👁️ **Tratamiento de Ojeras**
*   **Transiciones Fluida de Pestañas:** Cambio rápido de caso con desvanecimiento de opacidad suave (350ms) y auto-reseteo al centro.

### ❄️ 3. Módulo CoolSculpting® Dedicado
*   **Visualización Proporcional (1:1):** Slider de comparación exclusivo para la reducción abdominal sin distorsiones ni estiramientos.
*   **Insignia de Temperatura:** Badge flotante esmerilado de `-9° Criolipólisis` integrado en la esquina superior derecha del comparador para mantener la identidad científica del tratamiento.

### ✍️ 4. Blog de Salud Estética Enriquecido
*   **5 Artículos Únicos:** Información médica especializada y redactada en español sobre neuromoduladores, melasma, ácido hialurónico, criolipólisis y rutinas de otoño.
*   **Imágenes Exclusivas:** Eliminación completa de duplicados; cada artículo cuenta con su respectiva fotografía hero única que coincide en el listado (`blog.html`) y el interior del post.

### 🎨 5. Identidad Corporativa & CTAs
*   **Branding SVG Oficial:** Reemplazo de logotipos genéricos por el logotipo vectorial oficial de la clínica en cabeceras y pie de página.
*   **Favicon Personalizado:** Isotipo geométrico `"id"` en color dorado corporativo (`#b08d4f`) para una apariencia refinada en las pestañas del navegador.
*   **Llamadas a la Acción (WhatsApp):** Botones de "Pide tu cita" redirigen de inmediato al canal oficial de WhatsApp (`wa.me/34722349947`) para optimizar la conversión de leads.
*   **Footer Minimalista:** Pie de página crema elegante con enlaces legales en mayúsculas espaciadas.

---

## 🛠️ Tecnologías Utilizadas

*   **Estructura:** HTML5 Semántico
*   **Estilos:** Vanilla CSS (con scoping dinámico de Astro)
*   **Lógica:** JavaScript Nativo (ES6) sin dependencias externas
*   **Configuración:** Vercel Routing Configuration (`vercel.json`)

---

## 💻 Desarrollo Local

Para visualizar y probar la página web en tu entorno local:

1.  Asegúrate de estar en la carpeta raíz del proyecto (`preview-web`).
2.  Levanta un servidor local estático. Por ejemplo, utilizando `http-server` de Node.js:
    ```bash
    npx.cmd http-server -p 8080
    ```
3.  Abre en tu navegador la dirección:
    👉 `http://localhost:8080`

---

## 🚀 Despliegue en Vercel

El proyecto ya incluye el archivo de configuración `vercel.json` con la directiva `"cleanUrls": true` para eliminar las extensiones `.html` de la barra de direcciones y mejorar el SEO del sitio.

Tienes **dos opciones** rápidas para desplegarlo:

### Opción A: Despliegue Directo (Vercel CLI)
Si tienes Vercel CLI instalado o mediante `npx`:
1.  Abre la terminal en la carpeta raíz `preview-web`.
2.  Ejecuta el comando:
    ```bash
    npx.cmd vercel
    ```
3.  Inicia sesión si la terminal lo requiere y confirma los pasos sugeridos (tarda menos de 30 segundos).
4.  Una vez verificado el enlace de prueba, despliega a producción con:
    ```bash
    npx.cmd vercel --prod
    ```

### Opción B: Conexión GitHub (Automática y Recomendada)
1.  Inicializa Git y sube tus archivos a un repositorio de GitHub:
    ```bash
    git init
    git add .
    git commit -m "Mejoras de interactividad, Antes/Después y Blog"
    git branch -M main
    git remote add origin <URL-DE-TU-REPOSITORIO-GITHUB>
    git push -u origin main
    ```
2.  Ve a tu panel de control de Vercel (`vercel.com`).
3.  Haz clic en **"Add New"** > **"Project"** y selecciona tu repositorio.
4.  Vercel detectará el proyecto estático y lo desplegará de forma automática con cada `push` que hagas.
