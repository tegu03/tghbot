# buyer.py (final updated with score + MC filter + contact + buy log)

from datetime import datetime
from utils import load_json, save_json

PORTFOLIO_FILE = 'data/portfolio.json'

portfolio = load_json(PORTFOLIO_FILE, default=[]) or []

def is_already_bought(token_name):
    return any(t for t in portfolio if t['token_name'] == token_name and t['status'] == 'OPEN')

def add_to_portfolio(token_name, mc, lp, vol, age, wallet, score, buy_price, contact):
    token = {
        'token_name': token_name,
        'marketcap': mc,
        'liquidity': lp,
        'volume': vol,
        'age': age,
        'wallet': wallet,
        'score': score,
        'buy_price': buy_price,
        'buy_time': datetime.now().isoformat(),
        'status': 'OPEN',
        'contact': contact
    }
    portfolio.append(token)
    save_json(PORTFOLIO_FILE, portfolio)
    return token

def get_open_positions():
    return [t for t in portfolio if t['status'] == 'OPEN']
