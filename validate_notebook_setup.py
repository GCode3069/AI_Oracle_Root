#!/usr/bin/env python3
"""
Validation script for AI Oracle Jupyter Notebooks setup
Run this script to verify your environment is properly configured.
"""

import os
import sys
from pathlib import Path

def check_color(condition, success_msg, failure_msg):
    """Print colored status message"""
    if condition:
        print(f"✅ {success_msg}")
        return True
    else:
        print(f"❌ {failure_msg}")
        return False

def main():
    print("=" * 70)
    print("AI Oracle Notebook Environment Validation")
    print("=" * 70)
    print()
    
    all_checks_passed = True
    
    # Check 1: Python packages
    print("📦 Checking Python Packages...")
    packages = [
        ('gspread', 'Google Sheets API client'),
        ('oauth2client', 'OAuth2 client for Google APIs'),
        ('google.cloud.texttospeech', 'Google Cloud Text-to-Speech'),
        ('pandas', 'Data manipulation library'),
        ('dotenv', 'Environment variable loader'),
        ('IPython', 'Interactive Python (for Jupyter)')
    ]
    
    for package, description in packages:
        try:
            if package == 'google.cloud.texttospeech':
                __import__('google.cloud.texttospeech')
            elif package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package)
            check_color(True, f"{package:30} - {description}", "")
        except ImportError:
            check_color(False, "", f"{package:30} - NOT INSTALLED")
            all_checks_passed = False
    
    print()
    
    # Check 2: Directory structure
    print("📁 Checking Directory Structure...")
    dirs = [
        ('credentials', 'For storing API credentials'),
        ('2_Voiceover_Vault', 'For storing generated audio files'),
        ('1_Script_Engine/Google_Sheets_Integration', 'Google Sheets notebook location')
    ]
    
    for dir_path, description in dirs:
        exists = Path(dir_path).exists()
        if not exists and dir_path == 'credentials':
            # Create credentials directory if it doesn't exist
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            print(f"📝 Created {dir_path:40} - {description}")
        else:
            check_color(exists, f"{dir_path:40} - {description}", 
                       f"{dir_path:40} - NOT FOUND")
    
    print()
    
    # Check 3: Environment file
    print("🔐 Checking Environment Configuration...")
    env_file_exists = Path('.env').exists()
    env_example_exists = Path('.env.example').exists()
    
    check_color(env_example_exists, ".env.example exists (template)", 
               ".env.example NOT FOUND")
    
    if env_file_exists:
        check_color(True, ".env file exists", "")
        
        # Load and check environment variables
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            env_vars = [
                ('GOOGLE_SHEETS_CREDENTIALS_PATH', 'Google Sheets credentials path'),
                ('GOOGLE_SHEET_ID', 'Google Sheet ID'),
                ('GOOGLE_APPLICATION_CREDENTIALS', 'Google Cloud TTS credentials (Option 1)'),
                ('GOOGLE_CLOUD_API_KEY', 'Google Cloud API key (Option 2)')
            ]
            
            for var, description in env_vars:
                value = os.getenv(var)
                if value and value != 'your_sheet_id_here' and value != 'your_api_key_here':
                    check_color(True, f"  {var:40} - Set", "")
                else:
                    print(f"  ⚠️  {var:40} - Not set or using placeholder")
        except Exception as e:
            print(f"  ⚠️  Could not load .env: {e}")
    else:
        check_color(False, "", ".env file NOT FOUND - Copy .env.example to .env and configure")
        all_checks_passed = False
    
    print()
    
    # Check 4: Credential files
    print("🔑 Checking Credential Files...")
    cred_files = [
        'credentials/google_sheets_credentials.json',
        'credentials/google_cloud_tts_credentials.json',
        'credentials/client_secrets.json'
    ]
    
    found_any = False
    for cred_file in cred_files:
        exists = Path(cred_file).exists()
        if exists:
            check_color(True, f"{cred_file}", "")
            found_any = True
        else:
            print(f"  ℹ️  {cred_file} - Not found (optional)")
    
    if not found_any:
        print("  ⚠️  No credential files found. You'll need at least one for the notebooks to work.")
    
    print()
    
    # Check 5: Notebooks
    print("📓 Checking Jupyter Notebooks...")
    notebooks = [
        '1_Script_Engine/Google_Sheets_Integration/01_Sheets_Integration.ipynb',
        '1_Script_Engine/02_SSML_Generator.ipynb'
    ]
    
    for notebook in notebooks:
        exists = Path(notebook).exists()
        if exists:
            # Try to validate JSON structure
            try:
                import json
                with open(notebook, 'r') as f:
                    nb_data = json.load(f)
                cells = len(nb_data.get('cells', []))
                check_color(True, f"{notebook} ({cells} cells)", "")
            except Exception as e:
                check_color(False, "", f"{notebook} - INVALID: {e}")
                all_checks_passed = False
        else:
            check_color(False, "", f"{notebook} - NOT FOUND")
            all_checks_passed = False
    
    print()
    print("=" * 70)
    
    if all_checks_passed:
        print("✅ All critical checks passed! You're ready to use the notebooks.")
        print()
        print("Next steps:")
        print("  1. If you haven't already, configure your .env file")
        print("  2. Add your Google Cloud credentials to the credentials/ directory")
        print("  3. Launch Jupyter: jupyter notebook or jupyter lab")
        print("  4. Open and run the notebooks in 1_Script_Engine/")
    else:
        print("⚠️  Some checks failed. Please review the issues above.")
        print()
        print("Common fixes:")
        print("  • Install missing packages: pip install -r requirements.txt")
        print("  • Copy .env.example to .env: cp .env.example .env")
        print("  • Add your credentials to the credentials/ directory")
        print("  • See 1_Script_Engine/README.md for detailed setup instructions")
    
    print("=" * 70)
    
    return 0 if all_checks_passed else 1

if __name__ == '__main__':
    sys.exit(main())
