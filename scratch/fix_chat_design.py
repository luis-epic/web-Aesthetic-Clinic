import os
import re
import pathlib

"""
Fix chat design issues across all HTML files:
1. Remove dark/black border — make the chat window cleaner and whiter
2. Fix suggestions distortion when messages pile up by adding flex-shrink: 0
"""

# CSS replacements to apply
REPLACEMENTS = [
    # 1. Chat window: lighter, cleaner, whiter background, softer shadow
    (
        """/* Chat Window Panel */
.ai-chat-window {
  position: fixed !important;
  bottom: 96px !important;
  right: 26px !important;
  width: 360px !important;
  height: 480px !important;
  border-radius: 18px !important;
  background: rgba(255, 254, 251, 0.88) !important;
  backdrop-filter: blur(25px) saturate(120%) !important;
  -webkit-backdrop-filter: blur(25px) saturate(120%) !important;
  border: 1px solid rgba(176, 141, 79, 0.16) !important;
  box-shadow: 0 20px 50px -15px rgba(43, 39, 35, 0.22) !important;
  display: flex !important;
  flex-direction: column !important;
  z-index: 100000 !important;
  overflow: hidden !important;
  transform: translateY(20px) scale(0.95) !important;
  opacity: 0 !important;
  pointer-events: none !important;
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
}""",
        """/* Chat Window Panel */
.ai-chat-window {
  position: fixed !important;
  bottom: 96px !important;
  right: 26px !important;
  width: 360px !important;
  height: 480px !important;
  border-radius: 18px !important;
  background: #ffffff !important;
  backdrop-filter: blur(25px) saturate(120%) !important;
  -webkit-backdrop-filter: blur(25px) saturate(120%) !important;
  border: 1px solid rgba(220, 215, 205, 0.5) !important;
  box-shadow: 0 12px 40px -10px rgba(0, 0, 0, 0.12), 0 4px 12px rgba(0, 0, 0, 0.06) !important;
  display: flex !important;
  flex-direction: column !important;
  z-index: 100000 !important;
  overflow: hidden !important;
  transform: translateY(20px) scale(0.95) !important;
  opacity: 0 !important;
  pointer-events: none !important;
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
}"""
    ),

    # 2. Header: softer, warmer dark instead of pure black
    (
        """/* Header */
.ai-chat-header {
  background: linear-gradient(135deg, #2b2723, #1c1916) !important;
  padding: 16px 20px !important;
  display: flex !important;
  align-items: center !important;
  gap: 12px !important;
  border-bottom: 1px solid rgba(176, 141, 79, 0.1) !important;
}""",
        """/* Header */
.ai-chat-header {
  background: linear-gradient(135deg, #3d3530, #2e2822) !important;
  padding: 16px 20px !important;
  display: flex !important;
  align-items: center !important;
  gap: 12px !important;
  flex-shrink: 0 !important;
  border-bottom: none !important;
}"""
    ),

    # 3. Suggestions area: prevent shrink distortion
    (
        """/* Suggested chips area */
.ai-chat-suggestions {
  display: flex !important;
  gap: 8px !important;
  padding: 8px 16px !important;
  overflow-x: auto !important;
  background: #fbf9f6 !important;
  border-top: 1px solid rgba(176, 141, 79, 0.06) !important;
  scrollbar-width: none !important;
}""",
        """/* Suggested chips area */
.ai-chat-suggestions {
  display: flex !important;
  gap: 8px !important;
  padding: 8px 16px !important;
  overflow-x: auto !important;
  background: #ffffff !important;
  border-top: 1px solid rgba(220, 215, 205, 0.3) !important;
  scrollbar-width: none !important;
  flex-shrink: 0 !important;
  min-height: 42px !important;
}"""
    ),

    # 4. Input area: prevent shrink distortion
    (
        """/* Input Area */
.ai-chat-input-area {
  display: flex !important;
  align-items: center !important;
  padding: 12px 18px !important;
  background: #fff !important;
  border-top: 1px solid rgba(176, 141, 79, 0.1) !important;
  gap: 10px !important;
}""",
        """/* Input Area */
.ai-chat-input-area {
  display: flex !important;
  align-items: center !important;
  padding: 12px 18px !important;
  background: #fff !important;
  border-top: 1px solid rgba(220, 215, 205, 0.3) !important;
  gap: 10px !important;
  flex-shrink: 0 !important;
}"""
    ),

    # 5. Messages area: white background, ensure it shrinks properly
    (
        """/* Messages Area */
.ai-chat-messages {
  flex-grow: 1 !important;
  padding: 20px !important;
  overflow-y: auto !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 14px !important;
  background: #fbf9f6 !important;
}""",
        """/* Messages Area */
.ai-chat-messages {
  flex: 1 1 0 !important;
  min-height: 0 !important;
  padding: 20px !important;
  overflow-y: auto !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 14px !important;
  background: #fafafa !important;
}"""
    ),

    # 6. Bot bubble: cleaner border
    (
        """.bot .ai-chat-bubble {
  background: #fff !important;
  color: var(--ink) !important;
  border: 1px solid rgba(176, 141, 79, 0.12) !important;
  border-top-left-radius: 2px !important;
}""",
        """.bot .ai-chat-bubble {
  background: #fff !important;
  color: var(--ink) !important;
  border: 1px solid rgba(220, 215, 205, 0.4) !important;
  border-top-left-radius: 2px !important;
}"""
    ),
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
            # Try normalizing line endings
            old_norm = old.replace('\n', '\r\n')
            if old_norm in content:
                content = content.replace(old_norm, new.replace('\n', '\r\n'), 1)
                patched += 1
            else:
                print(f"  Warning: Could not find block starting with: {old[:60]}...")

    if patched > 0:
        p.write_text(content, encoding='utf-8')
        print(f"  Patched {patched}/{len(REPLACEMENTS)} CSS blocks.")
        return True
    else:
        print("  No changes needed or applied.")
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
