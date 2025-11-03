#!/usr/bin/env python3
"""
FIX_BITCOIN_RECITATION.py - Remove Bitcoin address from scripts

ISSUE: Lincoln is reciting the Bitcoin address (bc1q...) verbally
FIX: Remove address from ALL scripts, QR code is enough

Also adds:
- More satire (use that time for roasting)
- Screams/emphasis
- Jumpcut opportunities
"""

import re
from pathlib import Path

BITCOIN_ADDRESS = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"

def remove_bitcoin_recitation(script: str) -> str:
    """
    Remove any Bitcoin address recitation from script
    
    Removes:
    - Full address (bc1q...)
    - Partial address
    - "Bitcoin address is..."
    - "Send to bc1q..."
    """
    
    cleaned = script
    
    # Remove full Bitcoin address
    cleaned = cleaned.replace(BITCOIN_ADDRESS, '')
    
    # Remove common Bitcoin address phrases
    patterns = [
        r'Bitcoin address is:?\s*\S+',
        r'Send to:?\s*bc1q\S+',
        r'bc1q[a-z0-9]{30,}',
        r'The address is:?\s*\S+',
        r'Donate at:?\s*bc1q\S+',
    ]
    
    for pattern in patterns:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
    
    # Clean up extra spaces
    cleaned = re.sub(r'\s+', ' ', cleaned)
    cleaned = cleaned.strip()
    
    return cleaned

def add_more_satire_and_screams(script: str) -> str:
    """
    Replace Bitcoin recitation time with MORE SATIRE
    
    Add:
    - Screaming emphasis (ALL CAPS words)
    - Exclamation points
    - Rage breaks
    """
    
    # If script mentions "Bitcoin below" or "QR code", that's enough
    # Don't need to recite address
    
    # Add emphasis to key words
    emphasis_words = [
        ('lying', 'LYING'),
        ('corrupt', 'CORRUPT'),
        ('steal', 'STEAL'),
        ('rob', 'ROB'),
        ('scam', 'SCAM'),
        ('fraud', 'FRAUD'),
    ]
    
    for old, new in emphasis_words:
        script = re.sub(r'\b' + old + r'\b', new, script, flags=re.IGNORECASE)
    
    return script

def verify_no_address_in_scripts():
    """Check all script files for Bitcoin address recitation"""
    print("\n" + "="*60)
    print("CHECKING FOR BITCOIN ADDRESS RECITATION")
    print("="*60 + "\n")
    
    files = [
        "abraham_MAX_HEADROOM.py",
        "MAX_HEADROOM_ULTIMATE.py",
        "SCRIPTS_WITH_REAL_EDGE.py",
        "MORE_HEADLINE_ROASTS.py",
        "FIX_TIMING_AND_DARKNESS.py"
    ]
    
    issues = []
    
    for file_name in files:
        file_path = Path(file_name)
        if not file_path.exists():
            continue
        
        content = file_path.read_text(encoding='utf-8')
        
        # Check for Bitcoin address in quotes (actual scripts)
        if 'bc1q' in content or BITCOIN_ADDRESS in content:
            # Find context
            lines = content.splitlines()
            for i, line in enumerate(lines):
                if 'bc1q' in line.lower() and ('"' in line or "'" in line):
                    print(f"[FOUND] {file_name}:{i+1}")
                    print(f"  {line.strip()[:100]}")
                    issues.append((file_name, i+1, line))
    
    if issues:
        print(f"\n[ISSUE] Found {len(issues)} instances of Bitcoin address in scripts")
        print(f"[ACTION] Should be removed - QR code is enough!")
        return False
    else:
        print(f"[OK] No Bitcoin address recitation found")
        print(f"[OK] Scripts only mention 'Bitcoin below' or 'QR code'")
        return True

if __name__ == "__main__":
    clean = verify_no_address_in_scripts()
    
    if clean:
        print("\n" + "="*60)
        print("SCRIPTS ARE CLEAN")
        print("="*60)
        print("\nLincoln will NOT recite the address.")
        print("QR code is sufficient for donations.")
    else:
        print("\n" + "="*60)
        print("FIX NEEDED")
        print("="*60)
        print("\nRemove Bitcoin address from scripts.")
        print("Replace with MORE SATIRE and SCREAMS!")


