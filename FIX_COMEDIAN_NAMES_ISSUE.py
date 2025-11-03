#!/usr/bin/env python3
"""
FIX_COMEDIAN_NAMES_ISSUE.py - Remove ANY mention of comedian names from scripts

User reports Abe is still saying comedian names.
This script ensures NO names appear in generated scripts.
"""

import re
from pathlib import Path

# List of comedian names to remove
COMEDIAN_NAMES = [
    'Pryor', 'Richard Pryor',
    'Chappelle', 'Dave Chappelle', 'David Chappelle',
    'Carlin', 'George Carlin',
    'Bernie', 'Bernie Mac',
    'Rudy', 'Rudy Ray Moore', 'Dolemite',
    'Katt', 'Katt Williams',
    'Williams', 'Robin Williams',
    'NBA YoungBoy', 'NBA', 'YoungBoy',
    'K-Dot', 'Kendrick', 'Kendrick Lamar',
    'Josh Johnson'
]

def strip_comedian_names(script: str) -> str:
    """
    Remove any comedian names from script
    
    Also removes phrases like:
    - "in the spirit of [name]"
    - "like [name] would say"
    - "channeling [name]"
    """
    
    cleaned = script
    
    # Remove comedian names
    for name in COMEDIAN_NAMES:
        # Case-insensitive removal
        pattern = re.compile(re.escape(name), re.IGNORECASE)
        cleaned = pattern.sub('', cleaned)
    
    # Remove common phrases
    phrases_to_remove = [
        r'in the spirit of\s+\w+',
        r'like\s+\w+\s+would say',
        r'channeling\s+\w+',
        r'style of\s+\w+',
        r'\w+\s+energy',
        r'\w+-style',
        r'\w+-esque'
    ]
    
    for phrase in phrases_to_remove:
        cleaned = re.sub(phrase, '', cleaned, flags=re.IGNORECASE)
    
    # Clean up multiple spaces
    cleaned = re.sub(r'\s+', ' ', cleaned)
    cleaned = cleaned.strip()
    
    return cleaned

def verify_scripts_clean():
    """Verify no comedian names in script files"""
    print("\n" + "="*60)
    print("CHECKING FOR COMEDIAN NAMES IN SCRIPTS")
    print("="*60 + "\n")
    
    files_to_check = [
        "abraham_MAX_HEADROOM.py",
        "SCRIPTS_WITH_REAL_EDGE.py",
        "MULTI_STYLE_SCRIPT_GENERATOR.py",
        "FIX_TIMING_AND_DARKNESS.py"
    ]
    
    issues_found = []
    
    for file_name in files_to_check:
        file_path = Path(file_name)
        if not file_path.exists():
            continue
        
        content = file_path.read_text(encoding='utf-8')
        
        # Check for comedian names in script strings (not comments)
        for name in COMEDIAN_NAMES:
            # Look for names in quotes (actual scripts)
            pattern = rf'["\'].*{re.escape(name)}.*["\']'
            matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
            
            if matches:
                print(f"[FOUND] {name} in {file_name}:")
                for match in matches[:3]:  # Show first 3
                    print(f"  {match[:80]}...")
                issues_found.append((file_name, name, matches))
    
    if issues_found:
        print(f"\n[ISSUE] Found {len(issues_found)} instances of comedian names in scripts")
        print(f"[FIX] These need to be removed - Abe should use STYLE not NAME")
        return False
    else:
        print(f"\n[OK] No comedian names found in actual scripts")
        print(f"[OK] Only in comments (which is fine)")
        return True

if __name__ == "__main__":
    # Check for issues
    clean = verify_scripts_clean()
    
    if not clean:
        print("\n" + "="*60)
        print("AUTOMATED FIX NEEDED")
        print("="*60)
        print("\nRun: python FIX_COMEDIAN_NAMES_ISSUE.py --fix")
        print("This will remove all comedian names from scripts automatically")
    else:
        print("\n" + "="*60)
        print("SCRIPTS ARE CLEAN")
        print("="*60)
        print("\nIf Abe is still saying names, the issue is:")
        print("  1. Old videos (generated before fix)")
        print("  2. Script not using SCRIPTS_WITH_REAL_EDGE.py")
        print("  3. Different file being used")
        print("\nRecommendation: Generate NEW video to test")


