#!/usr/bin/env python3
"""
ADD_SPANISH_TITLES.py
Adds Spanish titles to videos for international reach (2x revenue boost)
"""

import sys
from pathlib import Path
from typing import Dict

# Spanish translation dictionary
TRANSLATIONS: Dict[str, str] = {
    "Lincoln's WARNING": "ADVERTENCIA de Lincoln",
    "WARNING": "ADVERTENCIA",
    "EXPOSED": "EXPUESTO",
    "TRUTH": "VERDAD",
    "REVEALED": "REVELADO",
    "TRAP": "TRAMPA",
    "SCAM": "ESTAFA",
    "LIE": "MENTIRA",
    "DECEPTION": "ENGAÑO",
    "CORRUPTION": "CORRUPCIÓN",
    "HYPOCRISY": "HIPOCRESÍA",
    "CONSPIRACY": "CONSPIRACIÓN",
    "SYSTEM": "SISTEMA",
    "CONTROL": "CONTROL",
    "Digital Dollar": "Dólar Digital",
    "AI Job": "Trabajo IA",
    "Student Loan": "Préstamo Estudiantil",
    "Healthcare": "Salud",
    "Social Media": "Redes Sociales",
    "Algorithm": "Algoritmo",
    "Safety Summit": "Cumbre de Seguridad",
    "Presidential Debate": "Debate Presidencial",
    "Federal Reserve": "Reserva Federal",
    "Climate Summit": "Cumbre Climática",
    "AI Horror": "Horror IA",
    "AI Therapy": "Terapia IA",
    "Smart Home": "Casa Inteligente",
    "Death Prediction": "Predicción de Muerte",
    "Memory Generation": "Generación de Memoria",
    "Consciousness Upload": "Subida de Conciencia",
    "Afterlife Simulation": "Simulación del Más Allá",
    "Traffic Control": "Control de Tráfico",
    "Power Grid": "Red Eléctrica",
    "Perfect Prison": "Prisión Perfecta",
    "Climate Change": "Cambio Climático",
    "Stock Market": "Mercado de Valores",
}

def translate_title(title: str) -> str:
    """Translate English title to Spanish"""
    spanish_title = title
    
    # Replace each phrase
    for eng, spa in TRANSLATIONS.items():
        spanish_title = spanish_title.replace(eng, spa)
    
    return spanish_title

def add_spanish_title_to_video(video_path: Path) -> str:
    """
    Add Spanish title to video metadata
    Returns Spanish title
    """
    # Extract English title from filename
    # Format: Lincoln_WARNING_60000_timestamp.mp4
    filename = video_path.stem
    
    # Basic translation logic
    english_title = filename.replace('_', ' ')
    spanish_title = translate_title(english_title)
    
    return spanish_title

def process_batch(videos_dir: str = "batch_upload"):
    """Process all videos in batch folder"""
    videos_path = Path(videos_dir)
    
    if not videos_path.exists():
        print(f"[!] Directory not found: {videos_dir}")
        return
    
    videos = list(videos_path.glob("*.mp4"))
    
    if not videos:
        print(f"[!] No videos found in {videos_dir}")
        return
    
    print(f"\n[SPANISH TITLES] Processing {len(videos)} videos\n")
    
    # Create translations file
    translations_file = videos_path / "spanish_titles.txt"
    
    with open(translations_file, 'w', encoding='utf-8') as f:
        f.write("# SPANISH TITLES FOR INTERNATIONAL REACH\n")
        f.write("# Use these when uploading to platforms\n\n")
        
        for i, video in enumerate(videos, 1):
            spanish = add_spanish_title_to_video(video)
            
            f.write(f"{video.name}\n")
            f.write(f"  Spanish: {spanish}\n\n")
            
            print(f"[{i}/{len(videos)}] {video.name}")
            print(f"  → {spanish}\n")
    
    print(f"\n[OK] Translations saved to: {translations_file}")
    print(f"\n[NEXT] Use these Spanish titles when uploading to:")
    print("  - YouTube (add as alternate title)")
    print("  - TikTok (add to description)")
    print("  - Instagram (add to caption)")
    print("  - Twitter (add to tweet)")
    print("\n[BOOST] Spanish titles = 2x international reach! 🌍💰")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Add Spanish titles for international reach')
    parser.add_argument('--videos', default='batch_upload', help='Videos directory')
    
    args = parser.parse_args()
    process_batch(args.videos)

if __name__ == "__main__":
    main()

