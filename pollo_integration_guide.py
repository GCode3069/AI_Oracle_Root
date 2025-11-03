#!/usr/bin/env python3
"""
POLLO.AI INTEGRATION GUIDE
You have 326 credits - let's use them!

Based on your screenshot:
- Plan: Lite-Monthly
- Credits: 326 available (0 used this month)
- Cost per image: 3 credits
- Web interface: pollo.ai/app

USE CASES FOR YOUR PROJECT:
1. Generate Abraham Lincoln images (better than Stability AI?)
2. Generate video backgrounds (better than Pexels?)
3. Generate full videos with Abe (AI Video feature)

Let's test each to see if $328/month is justified!
"""
import os
import sys
import requests
import json
from pathlib import Path
from datetime import datetime

# Your Pollo API key from screenshot
POLLO_API_KEY = "pollo_5EW9VjxB2eAUknmhd9vb9F2OJFDjPVVZttOQJRaaQ248"

BASE_DIR = Path("F:/AI_Oracle_Root/scarify")
TEST_DIR = BASE_DIR / "pollo_tests"
TEST_DIR.mkdir(parents=True, exist_ok=True)

def test_pollo_with_correct_endpoints():
    """
    Test Pollo with web-based endpoints
    The API might be at different URLs than I tried before
    """
    print("\n" + "="*70)
    print("POLLO.AI - TESTING WITH YOUR 326 CREDITS")
    print("="*70)
    print(f"Credits available: 326")
    print(f"Cost per image: 3 credits")
    print(f"Cost per video: Unknown (need to test)")
    print(f"Monthly cost: $328")
    print(f"\nGoal: Determine if Pollo improves your videos enough to justify cost")
    print("="*70)
    
    # Possible API endpoints to try
    possible_endpoints = [
        "https://api.pollo.ai",
        "https://pollo.ai/api",
        "https://api.pollo.ai/v1",
        "https://api.pollo.ai/api/v1"
    ]
    
    headers = {
        "Authorization": f"Bearer {POLLO_API_KEY}",
        "Content-Type": "application/json"
    }
    
    print("\n[1/3] Testing API connectivity...")
    for base_url in possible_endpoints:
        try:
            # Try to get account info
            test_endpoints = ["/account", "/user", "/credits", "/status"]
            for endpoint in test_endpoints:
                try:
                    response = requests.get(
                        f"{base_url}{endpoint}",
                        headers=headers,
                        timeout=10
                    )
                    if response.status_code in [200, 201]:
                        print(f"  [OK] Found working endpoint: {base_url}{endpoint}")
                        print(f"  Response: {response.json()}")
                        return base_url
                except:
                    continue
        except:
            continue
    
    print("  [INFO] Standard API endpoints not found")
    print("  [NOTE] Pollo may require web-based interaction or different auth")
    return None

def generate_lincoln_test_image():
    """
    TEST 1: Generate Abraham Lincoln image using Pollo
    Compare to current Stability AI fallback
    
    This costs 3 credits (you have 326)
    """
    print("\n" + "="*70)
    print("TEST 1: GENERATE LINCOLN IMAGE WITH POLLO")
    print("="*70)
    print("Cost: 3 credits (326 available)")
    print("Goal: Compare quality to current system\n")
    
    print("[Manual Test Required]")
    print("\nSteps:")
    print("1. Go to: https://pollo.ai/app")
    print("2. Click 'Txt2Img' in left sidebar")
    print("3. Enter prompt:")
    print("   'Abraham Lincoln portrait, 1865, black and white,")
    print("    serious expression, historical photo, high detail'")
    print("4. Click 'Create'")
    print("5. Download result to: F:\\AI_Oracle_Root\\scarify\\pollo_tests\\lincoln_test.jpg")
    print("\n6. Then compare:")
    print("   - Pollo result: pollo_tests/lincoln_test.jpg")
    print("   - Current: lincoln_faces/lincoln_optimized.jpg")
    print("\n7. Is Pollo version better? If NO → Cancel subscription!")
    print("="*70)

def generate_video_background_test():
    """
    TEST 2: Generate video background using Pollo
    Compare to Pexels (FREE)
    """
    print("\n" + "="*70)
    print("TEST 2: GENERATE VIDEO BACKGROUND WITH POLLO")
    print("="*70)
    print("Cost: Unknown credits")
    print("Goal: Compare to Pexels (FREE)\n")
    
    print("[Manual Test Required]")
    print("\nSteps:")
    print("1. Go to: https://pollo.ai/app")
    print("2. Check if 'AI Video' is available in sidebar")
    print("3. If yes:")
    print("   - Generate: 'American flag waving, dramatic, cinematic'")
    print("   - Download result")
    print("   - Compare to Pexels equivalent")
    print("4. If Pollo NOT better than FREE Pexels → Cancel!")
    print("="*70)

def generate_full_abe_video_test():
    """
    TEST 3: Generate full Abraham Lincoln video
    Compare to current FFmpeg + VHS effects
    
    This is the BIG test - does Pollo replace your entire system?
    """
    print("\n" + "="*70)
    print("TEST 3: GENERATE FULL ABE VIDEO WITH POLLO")
    print("="*70)
    print("Cost: Unknown credits")
    print("Goal: Can Pollo replace FFmpeg entirely?\n")
    
    print("[Manual Test Required]")
    print("\nSteps:")
    print("1. Go to: https://pollo.ai/app")
    print("2. Try 'AI Video' feature")
    print("3. Prompt:")
    print("   'Abraham Lincoln speaking on old VHS TV broadcast,")
    print("    1980s Max Headroom style, glitchy, scan lines, static,")
    print("    vertical format 1080x1920, 15 seconds'")
    print("4. Generate and download")
    print("5. Compare to your current videos:")
    print("   - abraham_horror/uploaded/*.mp4")
    print("\n6. Does Pollo match your VHS aesthetic? If NO → Cancel!")
    print("="*70)

def cost_benefit_analysis():
    """
    Final decision matrix
    """
    print("\n" + "="*70)
    print("POLLO.AI COST-BENEFIT DECISION MATRIX")
    print("="*70)
    
    print("\nCURRENT SYSTEM (WITHOUT POLLO):")
    print("  Cost: $22/month (ElevenLabs only)")
    print("  Quality: ✅ Authentic VHS aesthetic")
    print("  Speed: 60-90s per video")
    print("  Features: ✅ All working (glitch, VHS, QR, comedy)")
    
    print("\nPOLLO.AI:")
    print("  Cost: $328/month")
    print("  Credits: 326 available")
    print("  Quality: ??? (TEST REQUIRED)")
    print("  Speed: ??? (TEST REQUIRED)")
    
    print("\nDECISION CRITERIA:")
    print("  Keep Pollo IF:")
    print("    ✓ Generates BETTER Lincoln images than Stability")
    print("    ✓ Generates BETTER backgrounds than Pexels (FREE)")
    print("    ✓ Can replicate VHS aesthetic (saves FFmpeg time)")
    print("    ✓ Significantly faster than current 60-90s")
    
    print("\n  Cancel Pollo IF:")
    print("    ✗ Quality is same/worse than current")
    print("    ✗ Cannot match VHS aesthetic")
    print("    ✗ Pexels (FREE) is just as good")
    print("    ✗ Doesn't save significant time")
    
    print("\nPOTENTIAL SAVINGS IF CANCELED:")
    print("  Monthly: $328")
    print("  Annual: $3,936")
    
    print("\n" + "="*70)
    print("RECOMMENDATION:")
    print("="*70)
    print("1. Run all 3 manual tests above")
    print("2. Compare quality honestly")
    print("3. If Pollo doesn't significantly improve your videos:")
    print("   → CANCEL and save $3,936/year")
    print("4. Your current system ($22/month) is already excellent")
    print("="*70)

def create_comparison_checklist():
    """
    Create a checklist for comparing Pollo vs Current system
    """
    checklist = """
# POLLO.AI VS CURRENT SYSTEM - COMPARISON CHECKLIST

## TEST 1: LINCOLN IMAGE QUALITY

### Current System (Stability AI fallback):
- [ ] Quality: _____/10
- [ ] Detail: _____/10
- [ ] Authenticity: _____/10

### Pollo.ai (3 credits):
- [ ] Quality: _____/10
- [ ] Detail: _____/10
- [ ] Authenticity: _____/10

**Winner:** ____________
**Justifies $328/month?** YES / NO

---

## TEST 2: VIDEO BACKGROUNDS

### Current System (Pexels - FREE):
- [ ] Quality: _____/10
- [ ] Variety: _____/10
- [ ] Relevance: _____/10

### Pollo.ai (? credits):
- [ ] Quality: _____/10
- [ ] Variety: _____/10
- [ ] Relevance: _____/10

**Winner:** ____________
**Justifies $328/month?** YES / NO

---

## TEST 3: FULL VIDEO GENERATION

### Current System (FFmpeg + VHS effects):
- [ ] VHS Aesthetic: _____/10
- [ ] Max Headroom Glitch: _____/10
- [ ] Processing Time: _____ seconds
- [ ] Total Cost: $22/month

### Pollo.ai (? credits):
- [ ] VHS Aesthetic: _____/10
- [ ] Max Headroom Glitch: _____/10
- [ ] Processing Time: _____ seconds
- [ ] Total Cost: $328/month

**Winner:** ____________
**Justifies $328/month?** YES / NO

---

## FINAL DECISION

### Total Score:
- Current System: _____/30
- Pollo.ai: _____/30

### Cost Comparison:
- Current: $22/month ($264/year)
- Pollo: $328/month ($3,936/year)
- Difference: $306/month ($3,672/year)

### VERDICT:
- [ ] **KEEP POLLO** - Significantly better quality/speed
- [ ] **CANCEL POLLO** - Not worth $3,936/year extra

### Notes:
_____________________________________________
_____________________________________________
_____________________________________________

**Decision Date:** __________
**Action Taken:** __________
"""
    
    checklist_path = TEST_DIR / "POLLO_COMPARISON_CHECKLIST.md"
    with open(checklist_path, "w", encoding="utf-8") as f:
        f.write(checklist)
    
    print(f"\n[Checklist Created]")
    print(f"Location: {checklist_path}")
    print(f"Use this to compare Pollo vs your current system!\n")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("POLLO.AI - YOU HAVE 326 CREDITS!")
    print("Let's determine if $328/month is justified")
    print("="*70)
    
    # Test connectivity
    base_url = test_pollo_with_correct_endpoints()
    
    # Manual test guides
    generate_lincoln_test_image()
    generate_video_background_test()
    generate_full_abe_video_test()
    
    # Cost analysis
    cost_benefit_analysis()
    
    # Create comparison tool
    create_comparison_checklist()
    
    print("\n" + "="*70)
    print("NEXT STEPS:")
    print("="*70)
    print("1. Run the 3 manual tests above at pollo.ai/app")
    print("2. Fill out: pollo_tests/POLLO_COMPARISON_CHECKLIST.md")
    print("3. Make honest comparison")
    print("4. If Pollo not significantly better → Cancel & save $3,936/year")
    print("5. Your current system is already EXCELLENT at $22/month")
    print("="*70)

