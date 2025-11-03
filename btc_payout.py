import os
import requests
import json
from datetime import datetime

class BitcoinPayoutForge:
    def __init__(self):
        self.api_key = os.getenv("NOWPAYMENTS_API_KEY")
        self.btc_wallet = os.getenv("YOUR_BTC_WALLET")
        self.base_url = "https://api.nowpayments.io/v1"
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
    def create_btc_payment_link(self, amount_usd: float = 97) -> str:
        """Create simple Bitcoin payment link for X posts"""
        # If no API key, return fallback
        if not self.api_key:
            return "BITCOIN_OPTION_AVAILABLE - Set NOWPAYMENTS_API_KEY"
            
        payload = {
            "price_amount": amount_usd,
            "price_currency": "usd",
            "pay_currency": "btc", 
            "ipn_callback_url": "https://trenchaikits.com/webhook",
            "order_description": "Trench AI Kit - Rebel Edition"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/payment",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            payment_data = response.json()
            return payment_data['invoice_url']
            
        except Exception as e:
            print(f"❌ BTC PAYMENT LINK FAILED: {str(e)}")
            # Fallback to static BTC address
            return f"bitcoin:{self.btc_wallet}?amount=0.0015&label=Trench_AI_Kit_$97"

# Battle execution
if __name__ == "__main__":
    forge = BitcoinPayoutForge()
    
    # Create Bitcoin payment link for Rebel kit
    btc_link = forge.create_btc_payment_link(97)
    
    print(f"\n🎯 BITCOIN PAYMENT SYSTEM")
    print(f"🔗 PAYMENT LINK: {btc_link}")
    if forge.btc_wallet:
        print(f"🏦 WALLET: {forge.btc_wallet}")
    else:
        print("❌ Set YOUR_BTC_WALLET environment variable")
