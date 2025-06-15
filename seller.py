import json
import os
from datetime import datetime

PORTFOLIO_FILE = 'portfolio.json'
WINRATE_FILE = 'winrate.json'

# Struktur data sementara coin yang disimpan
portfolio = []
if os.path.exists(PORTFOLIO_FILE):
    with open(PORTFOLIO_FILE, 'r') as f:
        try:
            portfolio = json.load(f)
        except:
            portfolio = []

def save_portfolio():
    with open(PORTFOLIO_FILE, 'w') as f:
        json.dump(portfolio, f, indent=2)

def is_already_bought(token_name):
    return any(entry['token_name'] == token_name for entry in portfolio)

def add_to_portfolio(token_name, mc, lp, volume, age, wallet, score, buy_price):
    entry = {
        'token_name': token_name,
        'mc': mc,
        'lp': lp,
        'volume': volume,
        'age': age,
        'wallet': wallet,
        'score': score,
        'buy_price': buy_price,
        'buy_time': datetime.utcnow().isoformat(),
        'status': 'open'
    }
    portfolio.append(entry)
    save_portfolio()

def get_open_positions():
    return [entry for entry in portfolio if entry['status'] == 'open']

def update_position_status(token_name, status, sell_price=None):
    for entry in portfolio:
        if entry['token_name'] == token_name and entry['status'] == 'open':
            entry['status'] = status
            if sell_price:
                entry['sell_price'] = sell_price
                entry['result'] = 'win' if sell_price >= entry['buy_price'] * 2 else 'loss'
            break
    save_portfolio()
    update_winrate()

def get_winrate():
    closed = [e for e in portfolio if e['status'] != 'open']
    if not closed:
        return 0, 0, 0.0
    wins = sum(1 for e in closed if e.get('result') == 'win')
    total = len(closed)
    winrate = round((wins / total) * 100, 2)
    return wins, total, winrate

def update_winrate():
    wins, total, winrate = get_winrate()
    data = {
        'wins': wins,
        'total': total,
        'winrate': winrate,
        'last_updated': datetime.utcnow().isoformat()
    }
    with open(WINRATE_FILE, 'w') as f:
        json.dump(data, f, indent=2)
