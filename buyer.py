# buyer.py (updated with moonbag, tracking, contact, and compatibility)

import json
import os
from datetime import datetime
from utils import save_json, load_json

PORTFOLIO_FILE = 'data/portfolio.json'

# Load portfolio from JSON
portfolio = load_json(PORTFOLIO_FILE, default=[]) or []

def is_already_bought(token_name):
    return any(t['token_name'] == token_name and t['status'] == 'OPEN' for t in portfolio)

def add_to_portfolio(token_name, mc, lp, vol, age, wallet, score, buy_price, ca='N/A'):
    entry = {
        'token_name': token_name,
        'buy_price': buy_price,
        'buy_time': datetime.now().isoformat(),
        'status': 'OPEN',
        'sell_price': None,
        'sell_time': None,
        'result': None,
        'ca': ca,
        'mc': mc,
        'lp': lp,
        'volume': vol,
        'age': age,
        'wallet': wallet,
        'score': score
    }
    portfolio.append(entry)
    save_json(PORTFOLIO_FILE, portfolio)

def get_open_positions():
    return [t for t in portfolio if t['status'] == 'OPEN']

def get_closed_positions():
    return [t for t in portfolio if t['status'] != 'OPEN']

def update_position_status(token_name, status, sell_price):
    for t in portfolio:
        if t['token_name'] == token_name and t['status'] == 'OPEN':
            t['status'] = status
            t['sell_price'] = sell_price
            t['sell_time'] = datetime.now().isoformat()
            t['result'] = 'WIN' if status == 'TP' else 'LOSS'
            save_json(PORTFOLIO_FILE, portfolio)
            break

def get_winrate():
    closed = get_closed_positions()
    win = sum(1 for t in closed if t['result'] == 'WIN')
    total = len(closed)
    wr = round((win / total) * 100, 2) if total > 0 else 0.0
    return win, total, wr

def reset_portfolio():
    global portfolio
    portfolio = []
    save_json(PORTFOLIO_FILE, portfolio)
