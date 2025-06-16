# buyer.py

from utils import load_json, save_json
from config import PORTFOLIO_FILE

portfolio = load_json(PORTFOLIO_FILE, default=[]) or []

def add_to_portfolio(token_name, symbol, buy_price, marketcap, liquidity, volume, wallet, age, buy_time):
    portfolio.append({
        "token_name": token_name,
        "symbol": symbol,
        "buy_price": buy_price,
        "marketcap": marketcap,
        "liquidity": liquidity,
        "volume": volume,
        "wallet": wallet,
        "age": age,
        "buy_time": buy_time,
        "status": "OPEN"
    })
    save_json(PORTFOLIO_FILE, portfolio)

def get_open_positions():
    return [t for t in portfolio if t['status'] == 'OPEN']

def is_already_bought(symbol):
    return any(token["symbol"] == symbol and token["status"] == "OPEN" for token in portfolio)

def reset_portfolio():
    global portfolio
    portfolio = []
    save_json(PORTFOLIO_FILE, portfolio)
