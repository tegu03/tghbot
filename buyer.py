# buyer.py

from utils import load_json, save_json
from config import PORTFOLIO_FILE

# Load data portofolio dari file
portfolio = load_json(PORTFOLIO_FILE, default=[]) or []

# Menambahkan token baru ke portofolio
def add_to_portfolio(token_name, mc, lp, volume, age, wallet, score, buy_price, ca):
    entry = {
        "token_name": token_name,
        "mc": mc,
        "lp": lp,
        "volume": volume,
        "age": age,
        "wallet": wallet,
        "score": score,
        "buy_price": buy_price,
        "status": "open",  # default status
        "ca": ca  # contact address
    }
    portfolio.append(entry)
    save_json(PORTFOLIO_FILE, portfolio)

# Cek apakah token sudah dibeli sebelumnya
def is_already_bought(token_name):
    return any(
        p['token_name'].lower() == token_name.lower() and p['status'] == 'open'
        for p in portfolio
    )

# Ambil semua posisi yang masih terbuka
def get_open_positions():
    return [p for p in portfolio if p['status'] == 'open']

# Ambil semua posisi yang sudah ditutup
def get_closed_positions():
    return [p for p in portfolio if p['status'] in ['TP', 'SL']]

# Reset portofolio ke kondisi kosong (hanya untuk testing)
def reset_portfolio():
    global portfolio
    portfolio = []
    save_json(PORTFOLIO_FILE, portfolio)
