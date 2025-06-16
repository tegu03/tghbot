# seller.py (versi dengan moonbag dan logging detail jual)

import time
from utils import load_json, save_json

TOKEN_FILE = 'portfolio.json'
HISTORY_FILE = 'history.json'

# Status: OPEN, TP, SL, MOONBAG

def get_open_positions():
    return [x for x in load_json(TOKEN_FILE) if x['status'] == 'OPEN']

def get_history():
    return load_json(HISTORY_FILE)

def save_portfolio(data):
    save_json(TOKEN_FILE, data)

def save_history(entry):
    history = load_json(HISTORY_FILE)
    history.append(entry)
    save_json(HISTORY_FILE, history)

def update_position_status(token_name, status, sell_price):
    portfolio = load_json(TOKEN_FILE)
    for entry in portfolio:
        if entry['token_name'] == token_name and entry['status'] == 'OPEN':
            entry['status'] = status
            entry['sell_price'] = round(sell_price, 4)
            entry['sell_time'] = int(time.time())
            entry['profit_pct'] = round(((sell_price - entry['buy_price']) / entry['buy_price']) * 100, 2)

            # Jika TP dan moonbag diaktifkan
            if status == 'TP':
                entry['moonbag'] = {
                    'amount_percent': 20,
                    'hold_start_time': int(time.time())
                }

            save_history(entry)
            break
    save_portfolio(portfolio)

def get_winrate():
    history = get_history()
    total = len([x for x in history if x['status'] in ['TP', 'SL']])
    win = len([x for x in history if x['status'] == 'TP'])
    wr = round((win / total) * 100, 2) if total > 0 else 0
    return win, total, wr
