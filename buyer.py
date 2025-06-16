from utils import load_json, save_json
PORTFOLIO_FILE = 'portfolio.json'
portfolio = load_json(PORTFOLIO_FILE, default=[]) or []

def reset_portfolio():
    global portfolio
    portfolio = []
    save_json(PORTFOLIO_FILE, portfolio)
