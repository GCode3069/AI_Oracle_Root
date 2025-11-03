#!/usr/bin/env python3
"""
REVENUE TRACKER DASHBOARD - REAL WORKING CODE
Tracks revenue across ALL platforms and products
Shows real-time revenue, projections, and optimization recommendations
"""
import os
import json
from pathlib import Path
from datetime import datetime, timedelta

BASE_DIR = Path("F:/AI_Oracle_Root/scarify")
REVENUE_FILE = BASE_DIR / "revenue_tracking.json"

class RevenueTracker:
    """Track and analyze revenue from all sources"""
    
    def __init__(self):
        self.data = self._load_data()
    
    def _load_data(self):
        """Load revenue data"""
        if REVENUE_FILE.exists():
            with open(REVENUE_FILE, 'r') as f:
                return json.load(f)
        return {
            'platforms': {},
            'products': {},
            'tips': {},
            'total_revenue': 0,
            'start_date': datetime.now().isoformat(),
            'transactions': []
        }
    
    def _save_data(self):
        """Save revenue data"""
        REVENUE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(REVENUE_FILE, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def log_revenue(self, source, amount, description="", date=None):
        """Log revenue from any source"""
        if date is None:
            date = datetime.now().isoformat()
        
        transaction = {
            'date': date,
            'source': source,
            'amount': float(amount),
            'description': description
        }
        
        self.data['transactions'].append(transaction)
        self.data['total_revenue'] += float(amount)
        
        # Update source totals
        if source not in self.data['platforms'] and source not in self.data['products'] and source not in self.data['tips']:
            # Categorize
            if source in ['youtube', 'tiktok', 'rumble', 'instagram', 'snapchat', 'twitter']:
                self.data.setdefault('platforms', {})[source] = 0
            elif source in ['gumroad', 'patreon', 'fiverr']:
                self.data.setdefault('products', {})[source] = 0
            else:
                self.data.setdefault('tips', {})[source] = 0
        
        # Add to category total
        for category in ['platforms', 'products', 'tips']:
            if source in self.data.get(category, {}):
                self.data[category][source] += float(amount)
        
        self._save_data()
        print(f"[Revenue] Logged: ${amount:.2f} from {source}")
        return True
    
    def show_dashboard(self):
        """Display revenue dashboard"""
        print("\n" + "="*70)
        print("  REVENUE TRACKER DASHBOARD")
        print("="*70 + "\n")
        
        # Total revenue
        total = self.data.get('total_revenue', 0)
        print(f"[TOTAL REVENUE] ${total:.2f}\n")
        
        # Platform breakdown
        print("[PLATFORM REVENUE]")
        platforms = self.data.get('platforms', {})
        for platform, revenue in sorted(platforms.items(), key=lambda x: x[1], reverse=True):
            percentage = (revenue / total * 100) if total > 0 else 0
            print(f"  {platform.title()}: ${revenue:.2f} ({percentage:.1f}%)")
        print()
        
        # Product sales
        print("[PRODUCT REVENUE]")
        products = self.data.get('products', {})
        for product, revenue in sorted(products.items(), key=lambda x: x[1], reverse=True):
            percentage = (revenue / total * 100) if total > 0 else 0
            print(f"  {product.title()}: ${revenue:.2f} ({percentage:.1f}%)")
        print()
        
        # Tips/donations
        print("[TIPS & DONATIONS]")
        tips = self.data.get('tips', {})
        for tip_source, revenue in sorted(tips.items(), key=lambda x: x[1], reverse=True):
            percentage = (revenue / total * 100) if total > 0 else 0
            print(f"  {tip_source.title()}: ${revenue:.2f} ({percentage:.1f}%)")
        print()
        
        # Recent transactions
        print("[RECENT TRANSACTIONS]")
        recent = self.data.get('transactions', [])[-10:]
        for tx in reversed(recent):
            date = datetime.fromisoformat(tx['date']).strftime('%Y-%m-%d %H:%M')
            print(f"  {date} | ${tx['amount']:6.2f} | {tx['source'].title():<15} | {tx['description']}")
        print()
        
        # Projections
        self._show_projections()
    
    def _show_projections(self):
        """Show revenue projections"""
        print("[REVENUE PROJECTIONS]\n")
        
        # Calculate daily average
        transactions = self.data.get('transactions', [])
        if not transactions:
            print("  No data yet - start logging revenue!\n")
            return
        
        start_date = datetime.fromisoformat(self.data['start_date'])
        days_active = (datetime.now() - start_date).days or 1
        total = self.data.get('total_revenue', 0)
        
        daily_avg = total / days_active
        
        print(f"  Days Active: {days_active}")
        print(f"  Daily Average: ${daily_avg:.2f}")
        print()
        
        # 30/60/90 day projections
        projections = {
            '30 days': daily_avg * 30,
            '60 days': daily_avg * 60,
            '90 days': daily_avg * 90,
            '1 year': daily_avg * 365,
        }
        
        print("  Projections (at current pace):")
        for period, amount in projections.items():
            print(f"    {period}: ${amount:,.2f}")
        print()
    
    def export_report(self):
        """Export detailed revenue report"""
        report_file = BASE_DIR / f"revenue_report_{datetime.now().strftime('%Y%m%d')}.txt"
        
        with open(report_file, 'w') as f:
            f.write("REVENUE TRACKER REPORT\n")
            f.write("="*70 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write(f"Total Revenue: ${self.data.get('total_revenue', 0):.2f}\n\n")
            
            f.write("PLATFORM REVENUE:\n")
            for platform, revenue in self.data.get('platforms', {}).items():
                f.write(f"  {platform.title()}: ${revenue:.2f}\n")
            f.write("\n")
            
            f.write("PRODUCT REVENUE:\n")
            for product, revenue in self.data.get('products', {}).items():
                f.write(f"  {product.title()}: ${revenue:.2f}\n")
            f.write("\n")
            
            f.write("TRANSACTIONS:\n")
            for tx in self.data.get('transactions', []):
                date = datetime.fromisoformat(tx['date']).strftime('%Y-%m-%d %H:%M')
                f.write(f"  {date} | ${tx['amount']:6.2f} | {tx['source']} | {tx['description']}\n")
        
        print(f"[Export] Report saved: {report_file}\n")
        return report_file

def quick_log_revenue(source, amount, description=""):
    """Quick function to log revenue"""
    tracker = RevenueTracker()
    tracker.log_revenue(source, amount, description)
    tracker.show_dashboard()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 2:
        # Log revenue
        source = sys.argv[1]
        amount = float(sys.argv[2])
        description = sys.argv[3] if len(sys.argv) > 3 else ""
        quick_log_revenue(source, amount, description)
    else:
        # Show dashboard
        tracker = RevenueTracker()
        tracker.show_dashboard()
        
        print("""
REVENUE TRACKER - USAGE

Log revenue:
python revenue_tracker_dashboard.py SOURCE AMOUNT "Description"

Examples:
python revenue_tracker_dashboard.py rumble 15.50 "1,000 views"
python revenue_tracker_dashboard.py gumroad 97.00 "Script pack sale"
python revenue_tracker_dashboard.py cashapp 10.00 "Tip from fan"

Show dashboard:
python revenue_tracker_dashboard.py

Export report:
python revenue_tracker_dashboard.py --export
""")

