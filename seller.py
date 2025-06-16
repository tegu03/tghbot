# seller.py

import json
from pumpportal import get_token_price

PORTFOLIO_FILE = "tghbot/data/portfolio.json"

def load_portfolio():
    try:
        with open(PORTFOLIO_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_portfolio(data):
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_open_positions():
    return [t for t in load_portfolio() if t.get("status") == "OPEN"]

def update_position_status(token_name, new_status, sell_price):
    data = load_portfolio()
    for entry in data:
        if entry["token_name"] == token_name and entry["status"] == "OPEN":
            entry["status"] = new_status
            entry["sell_price"] = sell_price
    save_portfolio(data)

def get_winrate():
    data = load_portfolio()
    wins = sum(1 for t in data if t.get("status") == "TP")
    total = sum(1 for t in data if t.get("status") in ["TP", "SL"])
    winrate = round((wins / total) * 100, 2) if total > 0 else 0
    return wins, total, winrate

# Fungsi utama untuk pengecekan TP/SL
def check_positions():
    results = []
    for entry in get_open_positions():
        info = get_token_price(entry["token_name"])
        if not info:
            continue

        current_price = info["price"]
        buy_price = entry["buy_price"]

        if current_price >= buy_price * 2:
            update_position_status(entry["token_name"], "TP", current_price)
            results.append(f"🎯 TP: {entry['token_name']} @ {current_price:.4f}")
        elif current_price <= buy_price * 0.75:
            update_position_status(entry["token_name"], "SL", current_price)
            results.append(f"🛑 SL: {entry['token_name']} @ {current_price:.4f}")
    
    return results
