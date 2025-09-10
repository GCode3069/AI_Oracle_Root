#!/usr/bin/env python
# SCARIFY TTS Enhanced Script
# GCode3069 | UTC: 2025-09-02 05:56:03

import os
import sys
import json
import argparse
import re
from pathlib import Path

# Import ElevenLabs configuration
try:
    from elevenlabs_config import generate_elevenlabs_tts
    HAVE_ELEVENLABS = True
except ImportError:
    HAVE_ELEVENLABS = False
    print("WARNING: ElevenLabs integration not available. Using system TTS instead.")

def extract_text_from_json(json_path):
    """Extract text content from a script JSON file"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for field in ['script', 'text', 'content']:
            if field in data and data[field]:
                return re.sub(r'<[^>]+>', '', str(data[field]))
        print(f"Warning: Couldn't find text content in fields 'script', 'text', or 'content' in {json_path}")
        return None
    except Exception as e:
        print(f"Error reading script JSON: {e}")
        return None

def system_tts(text, output_path):
    """Fallback to system TTS if ElevenLabs is not available"""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.save_to_file(text, output_path)
        engine.runAndWait()
        print(f"Generated system TTS: {output_path}")
        return True
    except Exception as e:
        print(f"System TTS error: {e}")
        return False

def generate_tts(text, output_path, voice="jiminex"):
    """Generate TTS using available methods"""
    if not text:
        print("Error: No text provided for TTS generation")
        return False
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    if HAVE_ELEVENLABS:
        success = generate_elevenlabs_tts(text, output_path, voice)
        if success:
            return True
        print("ElevenLabs TTS failed, falling back to system TTS")
    return system_tts(text, output_path)

def main():
    parser = argparse.ArgumentParser(description="Generate TTS audio from script JSON")
    parser.add_argument("-i", "--input", required=False, help="Input script JSON file")
    parser.add_argument("-o", "--output", required=True, help="Output audio file path (.wav or .mp3)")
    parser.add_argument("-v", "--voice", default="jiminex", help="Voice style (default: jiminex)")
    parser.add_argument("-t", "--text", help="Direct text input instead of JSON file")
    parser.add_argument("--test", action="store_true", help="Run a test with a sample phrase")

    args = parser.parse_args()

    if args.test:
        test_text = "Every street leads deeper into the maze. Every turn takes you further from home."
        print(f"Running test with voice: {args.voice}")
        success = generate_tts(test_text, args.output, args.voice)
        if success:
            print("Test successful!")
        else:
            print("Test failed!")
        return

    if args.text:
        text = args.text
    else:
        if not args.input:
            print("Error: either --input or --text must be provided")
            sys.exit(1)
        text = extract_text_from_json(args.input)

    if text:
        success = generate_tts(text, args.output, args.voice)
        if success:
            print("TTS generation successful!")
            print(f"Output: {os.path.abspath(args.output)}")
        else:
            print("TTS generation failed!")
            sys.exit(1)
    else:
        print("Error: Failed to get text content")
        sys.exit(1)

if __name__ == "__main__":
    main()
