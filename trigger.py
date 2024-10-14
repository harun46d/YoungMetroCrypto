import requests
from datetime import datetime

def get_usd_pairs():
    url = 'https://api.binance.com/api/v3/ticker/price'
    response = requests.get(url)
    
    if response.status_code == 200:
        all_pairs = response.json()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        usd_pairs = [
                (pair['symbol'], float(pair['price']), current_time)
                for pair in all_pairs if pair['symbol'].endswith('USDT') or pair['symbol'].endswith('BUSD') or pair['symbol'].endswith('TUSD')
            ]
        return usd_pairs
    else:
        print(f"Status Code: {response.status_code}")
        return []
    
    
