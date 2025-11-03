#!/usr/bin/env python3
"""
STABILITY AI API INTEGRATION TEST
Test the $10/month Stability AI subscription

From your screenshot:
- Platform: platform.stability.ai
- API Keys: 2 available
- Cost: $10/month ($120/year)
- Current usage: Fallback for Lincoln image generation

GOAL: Determine if Stability improves Lincoln images enough to justify $10/month
"""
import os
import sys
import requests
import json
import base64
from pathlib import Path
from datetime import datetime

# Your Stability API key (from earlier in project)
STABILITY_API_KEY = "sk-sP93JLezaVNYpifbSDf9sn0rUaxhir377fJJV9Vit0nOEPQ1"
STABILITY_API_HOST = "https://api.stability.ai"

BASE_DIR = Path("F:/AI_Oracle_Root/scarify")
TEST_DIR = BASE_DIR / "stability_tests"
TEST_DIR.mkdir(parents=True, exist_ok=True)

def test_stability_connectivity():
    """Test Stability AI API connectivity"""
    print("\n" + "="*70)
    print("STABILITY AI - API CONNECTIVITY TEST")
    print("="*70)
    print(f"Cost: $10/month ($120/year)")
    print(f"Current usage: Fallback for Lincoln images")
    print(f"Goal: Determine if image quality justifies cost\n")
    
    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "application/json"
    }
    
    # Test 1: Check account
    print("[1/3] Testing account access...")
    try:
        response = requests.get(
            f"{STABILITY_API_HOST}/v1/user/account",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            account = response.json()
            print(f"  [OK] Account connected!")
            print(f"  Email: {account.get('email', 'N/A')}")
            print(f"  ID: {account.get('id', 'N/A')}")
        else:
            print(f"  [WARNING] Status: {response.status_code}")
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"  [ERROR] {e}")
    
    # Test 2: Check balance/credits
    print("\n[2/3] Checking balance...")
    try:
        response = requests.get(
            f"{STABILITY_API_HOST}/v1/user/balance",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            balance = response.json()
            print(f"  [OK] Credits available: {balance.get('credits', 'N/A')}")
        else:
            print(f"  [INFO] Balance check: {response.status_code}")
    except Exception as e:
        print(f"  [ERROR] {e}")
    
    # Test 3: List available engines
    print("\n[3/3] Checking available engines...")
    try:
        response = requests.get(
            f"{STABILITY_API_HOST}/v1/engines/list",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            engines = response.json()
            print(f"  [OK] Available engines:")
            for engine in engines:
                print(f"    - {engine.get('id', 'Unknown')}: {engine.get('name', 'N/A')}")
        else:
            print(f"  [INFO] Engines: {response.status_code}")
    except Exception as e:
        print(f"  [ERROR] {e}")
    
    print("\n" + "="*70)

def generate_lincoln_with_stability():
    """
    Generate Abraham Lincoln portrait using Stability AI
    This is the MAIN TEST - does it improve quality?
    """
    print("\n" + "="*70)
    print("STABILITY AI - GENERATE LINCOLN IMAGE")
    print("="*70)
    print("Cost: ~$0.02-0.10 per image")
    print("Goal: Better quality than current fallback\n")
    
    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Use SDXL 1.0 (best quality)
    engine_id = "stable-diffusion-xl-1024-v1-0"
    
    prompt = """
    Abraham Lincoln portrait, 1865 vintage photograph,
    black and white, daguerreotype style, serious expression,
    detailed facial features, historical accuracy, studio lighting,
    high resolution, fine detail, presidential portrait,
    Civil War era, formal attire, authentic period clothing
    """
    
    negative_prompt = """
    cartoon, anime, drawing, painting, color, colorized,
    modern, contemporary, low quality, blurry, distorted,
    unrealistic, fantasy, fictional
    """
    
    payload = {
        "text_prompts": [
            {
                "text": prompt,
                "weight": 1
            },
            {
                "text": negative_prompt,
                "weight": -1
            }
        ],
        "cfg_scale": 7,
        "height": 1024,
        "width": 1024,
        "samples": 1,
        "steps": 30,
    }
    
    print("[1/2] Generating image...")
    print(f"  Engine: {engine_id}")
    print(f"  Resolution: 1024x1024")
    print(f"  Steps: 30 (high quality)")
    
    try:
        response = requests.post(
            f"{STABILITY_API_HOST}/v1/generation/{engine_id}/text-to-image",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Save images
            for i, image in enumerate(data.get("artifacts", [])):
                image_data = base64.b64decode(image["base64"])
                
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_path = TEST_DIR / f"lincoln_stability_{timestamp}.png"
                
                with open(output_path, "wb") as f:
                    f.write(image_data)
                
                file_size = len(image_data) / 1024
                print(f"\n[2/2] [OK] Image generated!")
                print(f"  File: {output_path.name}")
                print(f"  Size: {file_size:.1f} KB")
                print(f"\n  [ACTION REQUIRED] Compare this to:")
                print(f"    - Current: lincoln_faces/lincoln_optimized.jpg")
                print(f"    - This test: {output_path}")
                
                return str(output_path)
        
        elif response.status_code == 403:
            print(f"  [ERROR] 403 Forbidden - API key may be invalid or expired")
            print(f"  Check: platform.stability.ai/account/keys")
        else:
            print(f"  [ERROR] Status: {response.status_code}")
            print(f"  Response: {response.text}")
            
    except Exception as e:
        print(f"  [ERROR] {e}")
        import traceback
        print(traceback.format_exc())
    
    print("\n" + "="*70)
    return None

def compare_quality():
    """
    Quality comparison guide
    """
    print("\n" + "="*70)
    print("QUALITY COMPARISON GUIDE")
    print("="*70)
    
    print("\nCURRENT SYSTEM (without Stability AI):")
    print("  Source: Downloaded from Wikipedia/Library of Congress")
    print("  Quality: High-resolution historical photo")
    print("  Cost: FREE")
    print("  File: lincoln_faces/lincoln_optimized.jpg")
    
    print("\nSTABILITY AI GENERATION:")
    print("  Source: AI-generated from prompt")
    print("  Quality: ??? (TEST ABOVE)")
    print("  Cost: $0.02-0.10 per generation + $10/month")
    print("  File: stability_tests/lincoln_stability_*.png")
    
    print("\nCOMPARISON CHECKLIST:")
    print("  [ ] Detail quality (face, hair, clothing)")
    print("  [ ] Historical accuracy")
    print("  [ ] Authenticity (does it look real?)")
    print("  [ ] Consistency (same Abe each time?)")
    print("  [ ] VHS aesthetic compatibility")
    
    print("\nDECISION:")
    print("  KEEP Stability AI if:")
    print("    - Significantly better quality than downloaded image")
    print("    - More control over expression/angle")
    print("    - Consistent results for different prompts")
    print("    - Worth $10/month improvement")
    
    print("\n  CANCEL Stability AI if:")
    print("    - Same/worse than free downloaded image")
    print("    - Inconsistent results")
    print("    - Not worth $10/month")
    print("    - Current Wikipedia image is good enough")
    
    print("\n" + "="*70)

def stability_integration_code():
    """
    Show how Stability is currently integrated
    """
    print("\n" + "="*70)
    print("CURRENT STABILITY INTEGRATION")
    print("="*70)
    
    print("\nLocation: abraham_MAX_HEADROOM.py")
    print("Usage: Fallback for generate_lincoln_face_pollo()")
    
    print("\nCurrent flow:")
    print("  1. Try Pollo AI first (if available)")
    print("  2. If Pollo fails -> Use Stability AI")
    print("  3. If Stability fails -> Download from Wikipedia")
    
    print("\nCode snippet:")
    print('''
    def generate_lincoln_face_pollo():
        """Generate Lincoln face using Stability AI"""
        try:
            # Stability AI generation
            response = requests.post(
                f"{STABILITY_API_HOST}/v1/generation/...",
                headers={"Authorization": f"Bearer {STABILITY_API_KEY}"},
                json=payload
            )
            if response.status_code == 200:
                # Save and return image
                return image_path
        except:
            # Fallback to Wikipedia download
            return download_lincoln_from_wikipedia()
    ''')
    
    print("\nRECOMMENDATION:")
    print("  If Stability AI quality is good:")
    print("    - Keep it as fallback ($10/month is reasonable)")
    print("    - Use for variety in Lincoln expressions")
    
    print("\n  If quality is not better:")
    print("    - Cancel subscription")
    print("    - Use only Wikipedia download (FREE)")
    print("    - Save $120/year")
    
    print("\n" + "="*70)

def cost_benefit_final():
    """
    Final cost-benefit analysis for BOTH APIs
    """
    print("\n" + "="*70)
    print("FINAL API COST-BENEFIT ANALYSIS")
    print("="*70)
    
    print("\nCURRENT API COSTS:")
    print("  ElevenLabs: $22/month - ESSENTIAL (voice generation)")
    print("  Pexels: FREE - ESSENTIAL (b-roll footage)")
    print("  Pollo.ai: $328/month - TEST REQUIRED (326 credits)")
    print("  Stability.ai: $10/month - TEST REQUIRED (image generation)")
    print("  TOTAL: $360/month ($4,320/year)")
    
    print("\nOPTIMIZED COSTS:")
    
    print("\n  Scenario 1: Keep both Pollo & Stability")
    print("    Monthly: $360")
    print("    Justification: Both provide significant quality boost")
    
    print("\n  Scenario 2: Keep Stability, cancel Pollo")
    print("    Monthly: $32 (save $328!)")
    print("    Annual savings: $3,936")
    print("    Justification: Stability useful, Pollo redundant")
    
    print("\n  Scenario 3: Cancel both")
    print("    Monthly: $22 (save $338!)")
    print("    Annual savings: $4,056")
    print("    Justification: Current system works perfectly")
    
    print("\nMY RECOMMENDATION:")
    print("  1. Test Stability AI (above)")
    print("  2. Test Pollo AI (separate guide)")
    print("  3. Most likely outcome:")
    print("     - Stability: KEEP ($10/month is reasonable for quality images)")
    print("     - Pollo: CANCEL ($328/month not justified)")
    print("     - Final cost: $32/month (saving $328/month)")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    print("\n" + "="*70)
    print("STABILITY AI INTEGRATION TEST")
    print("$10/month - Let's see if it's worth it!")
    print("="*70)
    
    # Test connectivity
    test_stability_connectivity()
    
    # Generate test image
    result = generate_lincoln_with_stability()
    
    # Comparison guide
    compare_quality()
    
    # Show current integration
    stability_integration_code()
    
    # Final analysis
    cost_benefit_final()
    
    print("\n" + "="*70)
    print("NEXT STEPS:")
    print("="*70)
    print("1. Compare generated image to current lincoln_optimized.jpg")
    print("2. If significantly better -> KEEP ($10/month reasonable)")
    print("3. If same/worse -> CANCEL (use free Wikipedia image)")
    print("4. Test Pollo AI separately (likely CANCEL $328/month)")
    print("5. Final recommendation: Keep Stability, cancel Pollo")
    print("   = $32/month total (vs current $360/month)")
    print("="*70)

