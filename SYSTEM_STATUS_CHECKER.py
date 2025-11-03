#!/usr/bin/env python3
"""
SYSTEM STATUS CHECKER
Verifies what's operational and functional in the SCARIFY system
"""
import os, sys, json
from pathlib import Path
from datetime import datetime

BASE = Path("F:/AI_Oracle_Root/scarify")
HORROR_BASE = BASE / "abraham_horror"

class SystemStatusChecker:
    """Check system operational status"""
    
    def __init__(self):
        self.status = {
            'generators': {},
            'apis': {},
            'platforms': {},
            'files': {},
            'directories': {}
        }
    
    def check_generators(self):
        """Check generator scripts"""
        generators = [
            ('VIRAL_OPTIMIZED_GENERATOR.py', BASE),
            ('ABRAHAM_ULTIMATE_FINAL.py', BASE),
            ('BLITZKRIEG_15_CHANNELS.py', BASE),
            ('working_abraham.py', BASE),
            ('abe_maxheadroom.py', BASE / 'abraham_horror')
        ]
        
        print("\n[GENERATOR SCRIPTS]")
        print("-" * 70)
        
        for name, path in generators:
            file_path = path / name
            exists = file_path.exists()
            size = file_path.stat().st_size / 1024 if exists else 0
            
            status = "[OK]" if exists else "[MISSING]"
            print(f"  {status} {name}")
            if exists:
                print(f"      Location: {file_path}")
                print(f"      Size: {size:.1f} KB")
            
            self.status['generators'][name] = {
                'exists': exists,
                'path': str(file_path),
                'size_kb': size
            }
    
    def check_apis(self):
        """Check API keys and configurations"""
        print("\n[API KEYS]")
        print("-" * 70)
        
        apis = {
            'ElevenLabs': os.getenv('ELEVENLABS_API_KEY'),
            'Pexels': os.getenv('PEXELS_API_KEY'),
            'YouTube OAuth': (BASE / 'client_secret_679199614743-1fq6sini3p9kjs237ek4seg4ojp4a4qe.apps.googleusercontent.com.json').exists()
        }
        
        for api, key in apis.items():
            if isinstance(key, bool):
                status = "[OK]" if key else "[MISSING]"
                print(f"  {status} {api}")
            else:
                status = "[OK]" if key else "[MISSING]"
                print(f"  {status} {api}: {'Configured' if key else 'Not configured'}")
            
            self.status['apis'][api] = bool(key) if not isinstance(key, bool) else key
    
    def check_platforms(self):
        """Check platform readiness"""
        print("\n[PLATFORM READINESS]")
        print("-" * 70)
        
        platforms = {
            'YouTube': {
                'generator': (BASE / 'VIRAL_OPTIMIZED_GENERATOR.py').exists(),
                'uploader': (BASE / 'youtube_uploader.py').exists(),
                'creds': (BASE / 'client_secret_679199614743-1fq6sini3p9kjs237ek4seg4ojp4a4qe.apps.googleusercontent.com.json').exists(),
                'output': (HORROR_BASE / 'youtube_ready').exists()
            },
            'TikTok': {
                'output': (HORROR_BASE / 'tiktok_ready').exists()
            },
            'Instagram': {
                'output': (HORROR_BASE / 'instagram_ready').exists()
            }
        }
        
        for platform, checks in platforms.items():
            all_ok = all(checks.values())
            status = "[OK]" if all_ok else "[PARTIAL]"
            print(f"  {status} {platform}")
            
            for check_name, check_result in checks.items():
                check_status = "[OK]" if check_result else "[MISSING]"
                print(f"      {check_status} {check_name}")
            
            self.status['platforms'][platform] = checks
    
    def check_files(self):
        """Check important files"""
        print("\n[IMPORTANT FILES]")
        print("-" * 70)
        
        important_files = [
            ('Chapman 2025 Config', BASE / 'configs' / 'chapman_2025.yaml'),
            ('YouTube Token', HORROR_BASE / 'youtube_token.pickle'),
            ('Launch Script', BASE / 'LAUNCH_VIRAL_GENERATOR.ps1')
        ]
        
        for name, file_path in important_files:
            exists = file_path.exists()
            status = "[OK]" if exists else "[MISSING]"
            print(f"  {status} {name}: {file_path}")
            
            self.status['files'][name] = {
                'exists': exists,
                'path': str(file_path)
            }
    
    def check_directories(self):
        """Check output directories"""
        print("\n[OUTPUT DIRECTORIES]")
        print("-" * 70)
        
        dirs = {
            'audio': HORROR_BASE / 'audio',
            'videos': HORROR_BASE / 'videos',
            'youtube_ready': HORROR_BASE / 'youtube_ready',
            'tiktok_ready': HORROR_BASE / 'tiktok_ready',
            'instagram_ready': HORROR_BASE / 'instagram_ready',
            'uploaded': HORROR_BASE / 'uploaded',
            'analytics': HORROR_BASE / 'analytics'
        }
        
        for name, dir_path in dirs.items():
            exists = dir_path.exists()
            if exists:
                file_count = len(list(dir_path.glob("*")))
                status = f"[OK] ({file_count} files)"
            else:
                status = "[MISSING]"
                file_count = 0
            
            print(f"  {status} {name}: {dir_path}")
            
            self.status['directories'][name] = {
                'exists': exists,
                'path': str(dir_path),
                'file_count': file_count
            }
    
    def generate_report(self):
        """Generate status report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'status': self.status,
            'summary': {
                'operational_generators': sum(1 for g in self.status['generators'].values() if g['exists']),
                'total_generators': len(self.status['generators']),
                'apis_configured': sum(1 for a in self.status['apis'].values() if a),
                'total_apis': len(self.status['apis']),
                'platforms_ready': sum(1 for p in self.status['platforms'].values() if all(p.values())),
                'total_platforms': len(self.status['platforms'])
            }
        }
        
        report_file = BASE / 'system_status.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n[REPORT] Saved: {report_file}")
        return report
    
    def run_full_check(self):
        """Run all checks"""
        print("\n" + "=" * 70)
        print("SCARIFY SYSTEM STATUS CHECK")
        print("=" * 70)
        
        self.check_generators()
        self.check_apis()
        self.check_platforms()
        self.check_files()
        self.check_directories()
        
        report = self.generate_report()
        
        print("\n" + "=" * 70)
        print("[SUMMARY]")
        print("=" * 70)
        print(f"Generators: {report['summary']['operational_generators']}/{report['summary']['total_generators']}")
        print(f"APIs: {report['summary']['apis_configured']}/{report['summary']['total_apis']}")
        print(f"Platforms Ready: {report['summary']['platforms_ready']}/{report['summary']['total_platforms']}")
        print("=" * 70 + "\n")

if __name__ == "__main__":
    checker = SystemStatusChecker()
    checker.run_full_check()

