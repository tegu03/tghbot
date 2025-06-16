# seller.py

from utils import load_json, save_json
from config import PORTFOLIO_FILE, MOONBAG_RATIO

portfolio = load_json(PORTFOLIO_FILE, default=[]) or []

def update_position_status(token_name, status, sell_price):
    global portfolio
    for token in portfolio:
        if token['token_name'] == token_name and token['status'] == 'OPEN':
            if status == 'TP' and MOONBAG_RATIO > 0:
                # TP with moonbag
                token['status'] = 'HOLD'
                token['sell_price'] = round(sell_price * (1 - MOONBAG_RATIO), 4)
                token['moonbag_price'] = round(sell_price * MOONBAG_RATIO, 4)
                token['moonbag_ratio'] = MOONBAG_RATIO
            else:
                # Regular TP or SL
                token['status'] = status
                token['sell_price'] = round(sell_price, 4)
            break
    save_json(PORTFOLIO_FILE, portfolio)

def get_winrate():
    total = 0
    win = 0
    for token in portfolio:
        if token['status'] in ['TP', 'SL']:
            total += 1
            if token['status'] == 'TP':
                win += 1
    if total == 0:
        return 0, 0, 0.0
    wr = round(win / total * 100, 2)
    return win, total, wr

def get_closed_positions():
    return [t for t in portfolio if t['status'] in ['TP', 'SL']]
