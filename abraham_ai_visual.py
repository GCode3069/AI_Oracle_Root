#!/usr/bin/env python3
"""
ABRAHAM LINCOLN VISUAL GENERATOR
Uses Stability AI to generate Abraham Lincoln horror images
"""
import requests
import random
from pathlib import Path

STABILITY_API_KEY = "sk-sP93JLezaVNYpifbSDf9sn0rUaxhir377fJJV9Vit0nOEPQ1"

def generate_lincoln_image(prompt, output_path):
    """Generate Abraham Lincoln horror image using Stability AI"""
    print(f"Generating Lincoln visual: {prompt[:60]}...")
    
    try:
        response = requests.post(
            "https://api.stability.ai/v2beta/stable-image/generate/sd3",
            headers={
                "Authorization": f"Bearer {STABILITY_API_KEY}",
                "Accept": "image/*"
            },
            files={"none": ""},
            data={
                "prompt": prompt,
                "model": "sd3.5-large-turbo",
                "aspect_ratio": "9:16",
                "output_format": "png",
                "seed": random.randint(0, 999999999)
            },
            timeout=120
        )
        
        if response.status_code == 200:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"Lincoln visual OK: {output_path.stat().st_size/1024:.2f} KB")
            return output_path
        else:
            print(f"Stability API error: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Stability AI error: {e}")
    
    return None

# Lincoln horror prompts
LINCOLN_PROMPTS = [
    "Abraham Lincoln portrait, ghostly, spectral, Ford's Theatre, April 1865, cinematic horror lighting, blood-soaked atmosphere, monochromatic with dark red accents, 19th century photography style",
    "Abraham Lincoln skull, cracked, bone fragments, derringer pistol, Victorian horror aesthetic, blood dripping, shadow play, gothic dark atmosphere",
    "Abraham Lincoln's ghostly face emerging from darkness, hollow eyes, torn presidential suit, Ford's Theatre in background, horror cinematography, desaturated colors",
]

if __name__ == "__main__":
    output_dir = Path("abraham_horror/images")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    prompt = LINCOLN_PROMPTS[0]
    output_file = output_dir / "lincoln_horror.png"
    
    generate_lincoln_image(prompt, output_file)
