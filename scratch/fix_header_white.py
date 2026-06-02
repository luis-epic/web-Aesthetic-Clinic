import os
import pathlib

"""
Change chat header from dark/black to white with gold text.
Also update the close button, volume button and online status
colors to work on a white background.
"""

OLD_HEADER_CSS = """/* Header */
.ai-chat-header {
  background: linear-gradient(135deg, #3d3530, #2e2822) !important;
  padding: 16px 20px !important;
  display: flex !important;
  align-items: center !important;
  gap: 12px !important;
  flex-shrink: 0 !important;
  border-bottom: none !important;
}"""

NEW_HEADER_CSS = """/* Header */
.ai-chat-header {
  background: #ffffff !important;
  padding: 16px 20px !important;
  display: flex !important;
  align-items: center !important;
  gap: 12px !important;
  flex-shrink: 0 !important;
  border-bottom: 1px solid rgba(176, 141, 79, 0.12) !important;
}"""

# Header text: was white on dark, now needs to be dark/gold on white
OLD_HEADER_H4 = """.ai-chat-header-info h4 {
  font-family: Jost, sans-serif !important;
  font-size: 0.92rem !important;
  font-weight: 500 !important;
  color: #fff !important;
  margin: 0 !important;
}"""

NEW_HEADER_H4 = """.ai-chat-header-info h4 {
  font-family: Jost, sans-serif !important;
  font-size: 0.92rem !important;
  font-weight: 600 !important;
  color: #977634 !important;
  margin: 0 !important;
}"""

# Subtitle: was gold on dark, now softer tone on white
OLD_HEADER_SPAN = """.ai-chat-header-info span {
  font-family: Jost, sans-serif !important;
  font-size: 0.72rem !important;
  color: var(--gold-soft) !important;
  opacity: 0.85 !important;
}"""

NEW_HEADER_SPAN = """.ai-chat-header-info span {
  font-family: Jost, sans-serif !important;
  font-size: 0.72rem !important;
  color: #a09080 !important;
  opacity: 1 !important;
}"""

# Close button: was white/60% on dark, now needs to be dark on white
OLD_CLOSE = """.ai-chat-close {
  background: none !important;
  border: none !important;
  color: rgba(255, 255, 255, 0.6) !important;
  font-size: 1.6rem !important;
  cursor: pointer !important;
  transition: color 0.3s !important;
  line-height: 1 !important;
}
.ai-chat-close:hover {
  color: #fff !important;
}"""

NEW_CLOSE = """.ai-chat-close {
  background: none !important;
  border: none !important;
  color: rgba(0, 0, 0, 0.3) !important;
  font-size: 1.6rem !important;
  cursor: pointer !important;
  transition: color 0.3s !important;
  line-height: 1 !important;
}
.ai-chat-close:hover {
  color: #977634 !important;
}"""

# Online status ring: was matching dark header, now white
OLD_ONLINE = """.ai-chat-online-status {
  position: absolute !important;
  bottom: 0 !important;
  right: 0 !important;
  width: 10px !important;
  height: 10px !important;
  border-radius: 50% !important;
  background: #25d366 !important;
  border: 1.5px solid #2b2723 !important;
  animation: onlinePulse 2s infinite !important;
}"""

NEW_ONLINE = """.ai-chat-online-status {
  position: absolute !important;
  bottom: 0 !important;
  right: 0 !important;
  width: 10px !important;
  height: 10px !important;
  border-radius: 50% !important;
  background: #25d366 !important;
  border: 1.5px solid #ffffff !important;
  animation: onlinePulse 2s infinite !important;
}"""

# Avatar border: softer gold
OLD_AVATAR = """.ai-chat-avatar {
  width: 100% !important;
  height: 100% !important;
  object-fit: cover !important;
  border-radius: 50% !important;
  border: 1.5px solid var(--gold-soft) !important;
}"""

NEW_AVATAR = """.ai-chat-avatar {
  width: 100% !important;
  height: 100% !important;
  object-fit: cover !important;
  border-radius: 50% !important;
  border: 1.5px solid rgba(176, 141, 79, 0.3) !important;
}"""

REPLACEMENTS = [
    (OLD_HEADER_CSS, NEW_HEADER_CSS),
    (OLD_HEADER_H4, NEW_HEADER_H4),
    (OLD_HEADER_SPAN, NEW_HEADER_SPAN),
    (OLD_CLOSE, NEW_CLOSE),
    (OLD_ONLINE, NEW_ONLINE),
    (OLD_AVATAR, NEW_AVATAR),
]


def patch_file(filepath):
    print(f"Processing: {filepath}")
    p = pathlib.Path(filepath)
    content = p.read_text(encoding='utf-8')
    patched = 0

    for old, new in REPLACEMENTS:
        if old in content:
            content = content.replace(old, new, 1)
            patched += 1
        else:
            old_crlf = old.replace('\n', '\r\n')
            if old_crlf in content:
                content = content.replace(old_crlf, new.replace('\n', '\r\n'), 1)
                patched += 1
            else:
                print(f"  Warning: block not found: {old[:50]}...")

    # Also update the inline style of the volume button (was white on dark)
    old_vol_style = 'color:rgba(255,255,255,0.6)'
    new_vol_style = 'color:rgba(0,0,0,0.35)'
    if old_vol_style in content:
        content = content.replace(old_vol_style, new_vol_style, 1)
        patched += 1

    # Update volume hover CSS to match
    old_vol_hover = """.ai-chat-volume-btn:hover {
  color: #fff !important;
  transform: scale(1.08) !important;
}
.ai-chat-volume-btn.active {
  color: var(--gold-soft) !important;
}"""
    new_vol_hover = """.ai-chat-volume-btn:hover {
  color: #977634 !important;
  transform: scale(1.08) !important;
}
.ai-chat-volume-btn.active {
  color: #b08d4f !important;
}"""
    if old_vol_hover in content:
        content = content.replace(old_vol_hover, new_vol_hover, 1)
        patched += 1
    else:
        old_vol_hover_crlf = old_vol_hover.replace('\n', '\r\n')
        if old_vol_hover_crlf in content:
            content = content.replace(old_vol_hover_crlf, new_vol_hover.replace('\n', '\r\n'), 1)
            patched += 1

    if patched > 0:
        p.write_text(content, encoding='utf-8')
        print(f"  Patched {patched} blocks.")
        return True
    else:
        print("  No changes.")
        return False


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
