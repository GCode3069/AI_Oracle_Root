#!/usr/bin/env python3
"""
NeuroSkins × Frequency Fusion
Main entry point
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.system import create_system
from src.core.config import ProductTier


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="NeuroSkins × Frequency Fusion: Adaptive Neural Interface"
    )
    
    parser.add_argument(
        '--tier',
        type=str,
        choices=['lite', 'pro', 'ascend'],
        default='lite',
        help='Product tier (default: lite)'
    )
    
    parser.add_argument(
        '--user-id',
        type=str,
        default='default',
        help='User identifier (default: default)'
    )
    
    parser.add_argument(
        '--duration',
        type=int,
        default=20,
        help='Session duration in minutes (default: 20)'
    )
    
    parser.add_argument(
        '--age',
        type=int,
        default=25,
        help='User age for verification (default: 25)'
    )
    

    
    parser.add_argument(
        '--status',
        action='store_true',
        help='Show system status and exit'
    )
    
    args = parser.parse_args()
    
    # Create system
    print("=" * 60)
    print("NeuroSkins × Frequency Fusion")
    print("Adaptive Neural Interface System")
    print("=" * 60)
    print()
    
    system = create_system(tier=args.tier, user_id=args.user_id)
    
    # Verify age
    if not system.verify_user_age(args.age):
        print(f"[ERROR] Age verification failed. Minimum age: 18")
        return 1
    
    print(f"[OK] User verified: age {args.age}")
    print()
    
    # Initialize hardware
    if not system.initialize_hardware():
        print("[ERROR] Hardware initialization failed")
        return 1
    
    print()
    
    # Show status
    if args.status:
        import json
        status = system.get_status()
        print(json.dumps(status, indent=2))
        return 0
    
    # Start session
    print(f"[INFO] Starting {args.tier.upper()} tier session...")
    print(f"[INFO] Duration: {args.duration} minutes")
    print(f"[INFO] Using real hardware sensors")
    print()
    
    try:
        # Start session
        session_id = system.start_session()
        
        # Run closed-loop
        system.run_closed_loop(duration_minutes=args.duration)
        
        # Stop session
        system.stop_session()
        
        print()
        print("=" * 60)
        print("Session Complete")
        print("=" * 60)
        
        # Show final status
        status = system.get_status()
        print(f"Safety Score: {status['safety']['safety_score']:.2f}")
        print(f"Warnings: {status['safety']['warning_count']}")
        print(f"Critical Events: {status['safety']['critical_count']}")
        
        return 0
        
    except KeyboardInterrupt:
        print()
        print("[INFO] Session interrupted by user")
        system.stop_session()
        return 0
    
    except Exception as e:
        print()
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        system.stop_session()
        return 1


if __name__ == '__main__':
    sys.exit(main())
