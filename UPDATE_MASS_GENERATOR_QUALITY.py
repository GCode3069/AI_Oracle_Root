#!/usr/bin/env python3
"""Add quality checks to MASS_GENERATE_100_VIDEOS.py"""
from pathlib import Path

# Read current mass generator
mass_gen = Path('MASS_GENERATE_100_VIDEOS.py')
code = mass_gen.read_text()

# Add uniqueness tracking at the top
additions = '''
# QUALITY ADDITIONS
import hashlib
USED_SCRIPTS = Path('used_scripts_mass.txt')

def is_unique_script(script):
    h = hashlib.md5(script.encode()).hexdigest()
    if USED_SCRIPTS.exists():
        used = set(USED_SCRIPTS.read_text().split())
        if h in used:
            return False
    with open(USED_SCRIPTS, 'a') as f:
        f.write(h + '\\n')
    return True
'''

# Insert after imports
if 'USED_SCRIPTS' not in code:
    code = code.replace('from MULTI_STYLE_SCRIPT_GENERATOR import ScriptStyleGenerator', 
                       'from MULTI_STYLE_SCRIPT_GENERATOR import ScriptStyleGenerator' + additions)

# Add retry logic for unique scripts
retry_logic = '''
            # Generate UNIQUE script (with retry)
            for attempt in range(5):
                if style == 'chatgpt':
                    script = style_gen.chatgpt_style(headline)
                elif style == 'grok':
                    script = style_gen.grok_style(headline)
                elif style == 'opus':
                    script = style_gen.opus_style(headline)
                else:
                    script = style_gen.cursor_style(headline)
                
                if is_unique_script(script):
                    break
                print(f"  [Retry {attempt+1}] Duplicate script")
'''

# Replace simple script generation
if 'Generate UNIQUE script' not in code:
    code = code.replace('''            # Generate script
            if style == 'chatgpt':
                script = style_gen.chatgpt_style(headline)
            elif style == 'grok':
                script = style_gen.grok_style(headline)
            elif style == 'opus':
                script = style_gen.opus_style(headline)
            else:  # cursor
                script = style_gen.cursor_style(headline)''', retry_logic)

# Save updated version
mass_gen.write_text(code)
print("✅ MASS_GENERATE_100_VIDEOS.py updated with quality checks!")
print("  - Uniqueness tracking added")
print("  - Retry logic for duplicates")
print("  - Script hash storage")


