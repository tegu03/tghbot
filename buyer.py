# buyer.py

import json
import time
import os

PORTFOLIO_FILE = "portfolio.json"

def load_portfolio():
    if not os.path.exists(PORTFOLIO_FILE):
        return []
    with open(PORTFOLIO_FILE, "r") as f:
        return json.load(f)

def save_portfolio(portfolio):
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(portfolio, f, indent=2)

def token_already_bought(address):
    portfolio = load_portfolio()
    return any(entry["address"] == address for entry in portfolio)

def buy_token(token):
    """
    Simulasi beli token dan simpan ke portfolio
    """
    if token_already_bought(token["address"]):
        return False, "❌ Token sudah dibeli"

    portfolio = load_portfolio()
    entry = {
        "name": token["name"],
        "address": token["address"],
        "buy_time": int(time.time()),
        "buy_price": token.get("price", 0),
        "mc": token.get("mc", 0),
        "lp": token.get("lp", 0)
    }
    portfolio.append(entry)
    save_portfolio(portfolio)
    return True, f"✅ Membeli {token['name']} di MC ${token['mc']:,}"
