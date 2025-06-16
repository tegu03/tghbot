# pumpportal.py

import requests

API_BASE_URL = "https://pumpportal.io/api/token"

def get_token_price(token_name: str):
    try:
        response = requests.get(f"{API_BASE_URL}?search={token_name}")
        data = response.json()
        
        if not data or 'tokens' not in data or len(data['tokens']) == 0:
            return None

        token = data['tokens'][0]
        return {
            "price": float(token.get("price", 0)),
            "mc": float(token.get("marketCap", 0)),
            "liquidity": float(token.get("liquidity", 0)),
            "volume": float(token.get("volume", 0)),
            "token_address": token.get("address")
        }

    except Exception as e:
        print(f"[PumpPortal ERROR] Failed to fetch token data: {e}")
        return None
