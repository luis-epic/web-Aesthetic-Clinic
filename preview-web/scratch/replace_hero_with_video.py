import re

filepath = r"c:\Users\luis\Downloads\web-preview-navegable\preview-web\index.html"

with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# Locate the hero section
hero_pattern = r'<section class="hero" id="inicio" data-astro-cid-bbe6dxrz>.*?</section>'

NEW_HERO_HTML = """<section class="hero" id="inicio" data-astro-cid-bbe6dxrz>
  <div class="slides" id="slides" data-astro-cid-bbe6dxrz>
    <div class="slide active" data-astro-cid-bbe6dxrz>
      <div class="sbg" data-astro-cid-bbe6dxrz>
        <video autoplay loop muted playsinline style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; z-index: 0;">
          <source src="/video_clinica.mp4" type="video/mp4">
        </video>
        <svg viewBox="0 0 1440 760" preserveAspectRatio="xMidYMid slice" data-astro-cid-bbe6dxrz style="position: absolute; inset: 0; width: 100%; height: 100%; z-index: 1; pointer-events: none;">
          <rect width="1440" height="760" fill="url(#gDark)" data-astro-cid-bbe6dxrz opacity="0.45"></rect>
          <circle cx="1180" cy="200" r="320" fill="url(#gGold)" opacity=".14"/>
          <circle cx="280" cy="640" r="220" fill="#b08d4f" opacity=".08"/>
        </svg>
      </div>
      <div class="slide-veil" data-astro-cid-bbe6dxrz style="z-index: 2;"></div>
      <div class="slide-inner" data-astro-cid-bbe6dxrz style="z-index: 3;">
        <div class="slide-anim" data-astro-cid-bbe6dxrz>
          <span class="eyebrow" data-astro-cid-bbe6dxrz>Clínicas en Bilbao &amp; Vitoria</span>
          <h1 data-astro-cid-bbe6dxrz>Medicina estética es <em>nuestro compromiso</em></h1>
          <p data-astro-cid-bbe6dxrz>Cuidar de ti. Más de 18 años ofreciendo resultados naturales, en armonía y duraderos.</p>
          <div class="slide-cta" data-astro-cid-bbe6dxrz>
            <a class="btn btn-primary" data-astro-cid-bbe6dxrz href="https://wa.me/34722349947" target="_blank" rel="noopener">Pide tu cita</a>
            <a href="./tratamientos.html" class="btn btn-line" data-astro-cid-bbe6dxrz>Tratamientos</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>"""

# Replace the hero section using regex
modified_html, count = re.subn(hero_pattern, NEW_HERO_HTML, html, flags=re.DOTALL)

if count > 0:
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(modified_html)
    print("SUCCESS: Hero section successfully replaced with background video in index.html.")
else:
    print("ERROR: Hero section pattern not found in index.html.")
