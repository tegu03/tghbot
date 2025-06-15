import json
import os
from datetime import datetime

PORTFOLIO_FILE = 'portfolio.json'

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
    return any(entry['token_name'] == token_name and entry['status'] == 'open' for entry in portfolio)

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
        'sell_price': None,
        'result': None,
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
            entry['sell_price'] = sell_price
            if sell_price is not None:
                entry['result'] = 'win' if sell_price >= entry['buy_price'] * 2 else 'loss'
            break
    save_portfolio()

def get_winrate():
    finished = [entry for entry in portfolio if entry['status'] != 'open']
    if not finished:
        return 0.0, 0, 0
    wins = [e for e in finished if e['result'] == 'win']
    return round(len(wins) / len(finished) * 100, 2), len(wins), len(finished)
