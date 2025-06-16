# buyer.py

from utils import load_json, save_json
from config import PORTFOLIO_FILE

# Load portfolio saat inisialisasi
portfolio = load_json(PORTFOLIO_FILE, default=[]) or []

def is_already_bought(symbol: str):
    """Cek apakah token dengan symbol ini sudah dibeli dan statusnya masih OPEN"""
    for token in portfolio:
        if token["symbol"] == symbol and token["status"] == "OPEN":
            return True
    return False

def add_to_portfolio(
    token_name,
    token_address,
    symbol,
    buy_price,
    buy_time,
    marketcap,
    liquidity,
    volume,
    wallet,
    age,
    score
):
    """Tambahkan token ke dalam portfolio dengan data lengkap"""
    token = {
        "token_name": token_name,
        "token_address": token_address,
        "symbol": symbol,
        "buy_price": buy_price,
        "buy_time": buy_time,
        "marketcap": marketcap,
        "liquidity": liquidity,
        "volume": volume,
        "wallet": wallet,
        "age": age,
        "score": score,
        "status": "OPEN",
        "sell_price": None
    }
    portfolio.append(token)
    save_json(PORTFOLIO_FILE, portfolio)

def get_open_positions():
    """Ambil semua token dengan status OPEN"""
    return [t for t in portfolio if t["status"] == "OPEN"]

def reset_portfolio():
    """Reset semua isi portfolio menjadi kosong"""
    global portfolio
    portfolio = []
    save_json(PORTFOLIO_FILE, portfolio)
