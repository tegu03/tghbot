# price_fetcher.py
import requests

def get_price_by_token_name(token_name):
    try:
        url = f"https://api.pump.fun/api/coins/{token_name}"
        response = requests.get(url, timeout=10)
        data = response.json()
        marketcap = data.get('marketCap', 0)
        return marketcap
    except Exception as e:
        print(f"[ERROR] Gagal fetch harga: {e}")
        return None
