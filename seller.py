# seller.py (final updated with moonbag, TP/SL handling)

from datetime import datetime
from utils import load_json, save_json

PORTFOLIO_FILE = 'data/portfolio.json'

portfolio = load_json(PORTFOLIO_FILE, default=[]) or []

def get_open_positions():
    return [t for t in portfolio if t['status'] == 'OPEN']

def get_closed_positions():
    return [t for t in portfolio if t['status'] != 'OPEN']

def get_winrate():
    closed = get_closed_positions()
    win = sum(1 for t in closed if t['result'] == 'WIN')
    total = len(closed)
    wr = round((win / total) * 100, 2) if total > 0 else 0.0
    return win, total, wr

def update_position_status(token_name, status, sell_price):
    for t in portfolio:
        if t['token_name'] == token_name and t['status'] == 'OPEN':
            t['status'] = status
            t['sell_price'] = sell_price
            t['sell_time'] = datetime.now().isoformat()
            t['result'] = 'WIN' if status == 'TP' else 'LOSS'
            save_json(PORTFOLIO_FILE, portfolio)
            break

def reset_portfolio():
    global portfolio
    portfolio = []
    save_json(PORTFOLIO_FILE, portfolio)

def process_position_updates(get_price_func):
    closed_tokens = []
    for entry in get_open_positions():
        now_price = get_price_func(entry['token_name'])
        if not now_price:
            continue
        buy = entry['buy_price']

        if now_price >= buy * 2:
            update_position_status(entry['token_name'], 'TP', now_price)
            closed_tokens.append((entry['token_name'], 'TP', now_price))

        elif now_price <= buy * 0.75:
            update_position_status(entry['token_name'], 'SL', now_price)
            closed_tokens.append((entry['token_name'], 'SL', now_price))

    return closed_tokens
