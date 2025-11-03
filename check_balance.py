#!/usr/bin/env python3
"""
Auto-check Bitcoin balance and USD value
"""

import requests
import json

BITCOIN_ADDRESS = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"
TARGET_USD = 10000

def check_bitcoin(address):
    try:
        print(f"Checking: {address[:20]}...")
        
        url = f"https://blockstream.info/api/address/{address}"
        r = requests.get(url, timeout=10)
        data = r.json()
        
        satoshis = data.get('chain_stats', {}).get('funded_txo_sum', 0)
        btc = satoshis / 100000000
        
        print(f"Current Balance: {btc:.8f} BTC")
        
        if btc > 0:
            # Get USD rate
            rate_url = "https://api.coindesk.com/v1/bpi/currentprice.json"
            rate_data = requests.get(rate_url, timeout=10).json()
            usd_rate = float(rate_data['bpi']['USD']['rate'].replace(',', ''))
            usd_value = btc * usd_rate
            
            print(f"USD Value: ${usd_value:,.2f}")
            print(f"Target: ${TARGET_USD:,}")
            print(f"Progress: {(usd_value/TARGET_USD)*100:.1f}%")
            
            if usd_value >= TARGET_USD:
                print(">>> TARGET HIT!")
            elif usd_value >= TARGET_USD * 0.5:
                print(">>> 50% TO GO!")
            elif usd_value >= TARGET_USD * 0.25:
                print(">>> Getting there...")
            else:
                print(">>> Keep pushing...")
            
            return usd_value
        else:
            print("Balance: 0 BTC (no donations yet)")
            print(">>> Keep generating and uploading videos!")
            return 0
            
    except Exception as e:
        print(f"Error: {e}")
        return 0

if __name__ == "__main__":
    print("="*60)
    print("BITCOIN BALANCE CHECK")
    print("="*60)
    print()
    check_bitcoin(BITCOIN_ADDRESS)
    print()
    print("="*60)

