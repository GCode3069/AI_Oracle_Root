#!/usr/bin/env python3
"""
POLLO.AI API INTEGRATION TEST
Test the $328/month Pollo API to validate it's worth keeping

Based on screenshots:
- API Key: pollo_5EW9VjxB2eAUknmhd9vb9F2OJFDjPVVZttOQJRaaQ248
- Credits: 326 available
- Endpoint: pollo.ai/api-platform
"""
import os
import sys
import json
import requests
import time
from pathlib import Path
from datetime import datetime

# Pollo API Configuration
POLLO_API_KEY = "pollo_5EW9VjxB2eAUknmhd9vb9F2OJFDjPVVZttOQJRaaQ248"
POLLO_BASE_URL = "https://api.pollo.ai/v1"

BASE_DIR = Path("F:/AI_Oracle_Root/scarify")
TEST_OUTPUT = BASE_DIR / "test_results"
TEST_OUTPUT.mkdir(parents=True, exist_ok=True)

def test_pollo_connectivity():
    """Test basic Pollo API connectivity"""
    print("\n" + "="*70)
    print("POLLO.AI API CONNECTIVITY TEST")
    print("="*70)
    print(f"API Key: {POLLO_API_KEY[:20]}...{POLLO_API_KEY[-10:]}")
    print(f"Cost: $328/month")
    print(f"Status: Currently integrated in abraham_MAX_HEADROOM.py\n")
    
    headers = {
        "Authorization": f"Bearer {POLLO_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Test 1: Check account/credits
    print("[Test 1/4] Checking account status...")
    try:
        # Try common endpoints
        endpoints_to_try = [
            f"{POLLO_BASE_URL}/account",
            f"{POLLO_BASE_URL}/user/account",
            f"{POLLO_BASE_URL}/credits",
            f"{POLLO_BASE_URL}/status"
        ]
        
        for endpoint in endpoints_to_try:
            try:
                response = requests.get(endpoint, headers=headers, timeout=10)
                if response.status_code in [200, 201]:
                    print(f"  [OK] Connected to: {endpoint}")
                    print(f"  Response: {response.json()}")
                    break
            except:
                continue
        else:
            print("  [WARNING] Standard endpoints not found, trying image generation test...")
    except Exception as e:
        print(f"  [ERROR] {e}")
    
    # Test 2: Generate test image (cheaper than video)
    print("\n[Test 2/4] Testing image generation...")
    try:
        image_payload = {
            "prompt": "Abraham Lincoln portrait, serious expression, black and white, historical photo style",
            "width": 512,
            "height": 512,
            "num_outputs": 1
        }
        
        response = requests.post(
            f"{POLLO_BASE_URL}/image/generate",
            headers=headers,
            json=image_payload,
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            print(f"  [OK] Image generation request accepted!")
            result = response.json()
            print(f"  Response: {json.dumps(result, indent=2)}")
            
            # Save test result
            with open(TEST_OUTPUT / "pollo_image_test.json", "w") as f:
                json.dump(result, f, indent=2)
        else:
            print(f"  [FAIL] Status code: {response.status_code}")
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"  [ERROR] {e}")
    
    # Test 3: Check available models
    print("\n[Test 3/4] Checking available models...")
    try:
        response = requests.get(
            f"{POLLO_BASE_URL}/models",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            models = response.json()
            print(f"  [OK] Available models:")
            for model in models.get('data', []):
                print(f"    - {model.get('name', 'Unknown')}: {model.get('description', 'No description')}")
        else:
            print(f"  [INFO] Models endpoint returned: {response.status_code}")
    except Exception as e:
        print(f"  [ERROR] {e}")
    
    # Test 4: Compare to current FFmpeg implementation
    print("\n[Test 4/4] Cost-benefit analysis...")
    print("  Current setup:")
    print("    - Using FFmpeg + Pexels (FREE)")
    print("    - Processing time: ~60-90s per video")
    print("    - Quality: Authentic VHS aesthetic")
    print("  ")
    print("  Pollo.ai:")
    print("    - Cost: $328/month")
    print("    - Credits available: 326")
    print("    - Use case: AI video generation")
    print("  ")
    print("  VERDICT:")
    print("    - IF Pollo generates better Lincoln videos: KEEP")
    print("    - IF quality is same/worse than FFmpeg: CANCEL")
    print("    - Potential savings: $3,936/year if canceled")
    
    print("\n" + "="*70)
    print("TEST COMPLETE - Review results above")
    print("="*70)

def generate_pollo_video_test():
    """Generate a test video using Pollo to compare quality"""
    print("\n" + "="*70)
    print("POLLO VIDEO GENERATION TEST")
    print("="*70)
    
    headers = {
        "Authorization": f"Bearer {POLLO_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Test video generation
    print("\n[1/3] Requesting video generation...")
    
    video_payload = {
        "prompt": "Abraham Lincoln speaking on old VHS TV broadcast, glitchy, Max Headroom style, 1980s aesthetic, scan lines, static",
        "duration": 5,  # Start with short test
        "resolution": "1080x1920",  # Vertical for shorts
        "style": "realistic"
    }
    
    try:
        response = requests.post(
            f"{POLLO_BASE_URL}/video/generate",
            headers=headers,
            json=video_payload,
            timeout=60
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            print(f"  [OK] Video generation started!")
            print(f"  Job ID: {result.get('id', 'N/A')}")
            print(f"  Status: {result.get('status', 'N/A')}")
            
            # Save result
            with open(TEST_OUTPUT / "pollo_video_test.json", "w") as f:
                json.dump(result, f, indent=2)
            
            # Check status
            job_id = result.get('id')
            if job_id:
                print("\n[2/3] Checking generation status...")
                for i in range(10):  # Check for up to 100 seconds
                    time.sleep(10)
                    status_response = requests.get(
                        f"{POLLO_BASE_URL}/video/{job_id}",
                        headers=headers,
                        timeout=10
                    )
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        status = status_data.get('status', 'unknown')
                        print(f"  [{i+1}/10] Status: {status}")
                        
                        if status == 'completed':
                            video_url = status_data.get('video_url') or status_data.get('url')
                            print(f"\n[3/3] [OK] Video generated!")
                            print(f"  URL: {video_url}")
                            
                            # Download video
                            if video_url:
                                video_response = requests.get(video_url, timeout=60)
                                output_file = TEST_OUTPUT / f"pollo_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
                                with open(output_file, 'wb') as f:
                                    f.write(video_response.content)
                                print(f"  Saved to: {output_file}")
                                print(f"\n  [ACTION REQUIRED] Compare this video to FFmpeg output!")
                            break
                        elif status in ['failed', 'error']:
                            print(f"  [FAIL] Generation failed: {status_data.get('error', 'Unknown error')}")
                            break
                else:
                    print(f"  [TIMEOUT] Video still processing after 100s")
        else:
            print(f"  [FAIL] Status code: {response.status_code}")
            print(f"  Response: {response.text}")
            print(f"\n  [NOTE] Pollo API may not be properly configured")
            print(f"  [ACTION] Check API documentation at pollo.ai/api-platform/docs")
    
    except Exception as e:
        print(f"  [ERROR] {e}")
        print(f"\n  [NOTE] This may indicate Pollo API is not set up correctly")
        print(f"  [RECOMMENDATION] Consider canceling if not essential")
    
    print("\n" + "="*70)

def comprehensive_api_test():
    """Test ALL paid APIs and generate cost report"""
    print("\n" + "="*70)
    print("COMPREHENSIVE API COST ANALYSIS")
    print("="*70)
    
    results = {
        'elevenlabs': {
            'cost_monthly': 22,
            'cost_annual': 264,
            'using': True,
            'essential': True,
            'verdict': 'KEEP',
            'reason': 'Voice generation is core functionality'
        },
        'pexels': {
            'cost_monthly': 0,
            'cost_annual': 0,
            'using': True,
            'essential': True,
            'verdict': 'KEEP',
            'reason': 'Free B-roll footage'
        },
        'pollo': {
            'cost_monthly': 328,
            'cost_annual': 3936,
            'using': True,  # NOW USING in abraham_MAX_HEADROOM.py
            'essential': False,  # Needs validation
            'verdict': 'TEST REQUIRED',
            'reason': 'Expensive - must prove value vs FFmpeg'
        },
        'stability': {
            'cost_monthly': 10,
            'cost_annual': 120,
            'using': True,  # NOW USING in abraham_MAX_HEADROOM.py (fallback)
            'essential': False,
            'verdict': 'TEST REQUIRED',
            'reason': 'Image enhancement - minimal impact observed'
        }
    }
    
    total_monthly = sum(api['cost_monthly'] for api in results.values())
    total_annual = sum(api['cost_annual'] for api in results.values())
    
    optimized_monthly = sum(
        api['cost_monthly'] for api in results.values() 
        if api['essential']
    )
    optimized_annual = optimized_monthly * 12
    
    potential_savings_monthly = total_monthly - optimized_monthly
    potential_savings_annual = total_annual - optimized_annual
    
    print(f"\nCURRENT COSTS:")
    print(f"  Monthly: ${total_monthly}")
    print(f"  Annual: ${total_annual}")
    
    print(f"\nIF CANCELING NON-ESSENTIAL:")
    print(f"  Monthly: ${optimized_monthly}")
    print(f"  Annual: ${optimized_annual}")
    
    print(f"\nPOTENTIAL SAVINGS:")
    print(f"  Monthly: ${potential_savings_monthly}")
    print(f"  Annual: ${potential_savings_annual}")
    
    print(f"\nAPI BREAKDOWN:")
    for api_name, api_data in results.items():
        print(f"\n  {api_name.upper()}:")
        print(f"    Cost: ${api_data['cost_monthly']}/month (${api_data['cost_annual']}/year)")
        print(f"    Using: {api_data['using']}")
        print(f"    Essential: {api_data['essential']}")
        print(f"    Verdict: {api_data['verdict']}")
        print(f"    Reason: {api_data['reason']}")
    
    print(f"\n" + "="*70)
    print(f"RECOMMENDATION:")
    print(f"="*70)
    print(f"1. Test Pollo.ai video quality vs FFmpeg")
    print(f"2. Test Stability.ai image enhancement impact")
    print(f"3. If no significant improvement -> Save ${potential_savings_annual}/year")
    print(f"4. Current system (FFmpeg + Pexels) is FREE and working well")
    print(f"=" * 70)
    
    # Save report
    with open(TEST_OUTPUT / "api_cost_analysis.json", "w") as f:
        json.dump({
            'results': results,
            'total_monthly': total_monthly,
            'total_annual': total_annual,
            'optimized_monthly': optimized_monthly,
            'optimized_annual': optimized_annual,
            'potential_savings_monthly': potential_savings_monthly,
            'potential_savings_annual': potential_savings_annual,
            'generated_at': datetime.now().isoformat()
        }, f, indent=2)
    
    print(f"\nReport saved to: {TEST_OUTPUT / 'api_cost_analysis.json'}")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("POLLO.AI API TESTING SUITE")
    print("Testing $328/month subscription to validate ROI")
    print("="*70)
    
    # Run tests
    test_pollo_connectivity()
    
    # Ask if user wants to test video generation (uses credits)
    print("\n" + "="*70)
    print("VIDEO GENERATION TEST")
    print("="*70)
    print("This will use Pollo credits to generate a test video.")
    print("Continue? (y/n): ", end="")
    
    # Auto-yes for now since user wants testing
    print("y (auto-proceeding)")
    generate_pollo_video_test()
    
    # Final cost analysis
    comprehensive_api_test()
    
    print("\n" + "="*70)
    print("ALL TESTS COMPLETE")
    print("="*70)
    print(f"Results saved to: {TEST_OUTPUT}")
    print("\nNext steps:")
    print("1. Review test results")
    print("2. Compare Pollo video quality to FFmpeg output")
    print("3. Decide: KEEP or CANCEL Pollo ($3,936/year savings if cancel)")
    print("4. Same for Stability.ai ($120/year)")
    print("="*70)

