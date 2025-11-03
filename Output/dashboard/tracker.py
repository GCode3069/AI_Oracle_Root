import requests, time, os
from datetime import datetime
GUMROAD_KEY = ''
LINK = 'https://gumroad.com/l/buy-rebel-97'
def track_sales():
    url = f'https://api.gumroad.com/v2/sales?access_token={GUMROAD_KEY}&product_id=rebel-97'
    while True:
        try:
            r = requests.get(url)
            sales = r.json()['sales']
            total = len(sales) * 97
            print(f'🤑 {datetime.now()} | SALES: {len(sales)} | TOTAL: ${total}')
            with open('dashboard/gumroad_live.txt', 'w') as f:
                f.write(f'Sales: {len(sales)} | Revenue: ${total}')
        except: pass
        time.sleep(30)
track_sales()
