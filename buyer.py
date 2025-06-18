from utils import load_json, save_json
from config import PORTFOLIO_FILE

def is_already_bought(symbol: str):
    """Cek apakah token dengan symbol ini sudah dibeli dan statusnya masih OPEN"""
    portfolio = load_json(PORTFOLIO_FILE, default=[])
    return any(t for t in portfolio if t["symbol"] == symbol and t["status"] == "OPEN")

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
    """Tambahkan token ke dalam portfolio dengan data lengkap jika belum ada"""
    portfolio = load_json(PORTFOLIO_FILE, default=[])

    # Hindari duplikat token OPEN
    for token in portfolio:
        if token["symbol"] == symbol and token["status"] == "OPEN":
            return  # sudah dibeli

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
    portfolio = load_json(PORTFOLIO_FILE, default=[])
    return [t for t in portfolio if t.get("status") == "OPEN"]

def reset_portfolio():
    """Reset semua isi portfolio menjadi kosong"""
    save_json(PORTFOLIO_FILE, [])

def remove_position(symbol: str):
    """Hapus token berdasarkan symbol"""
    portfolio = load_json(PORTFOLIO_FILE, default=[])
    new_portfolio = [t for t in portfolio if t["symbol"] != symbol]
    save_json(PORTFOLIO_FILE, new_portfolio)

def update_token_status(symbol: str, status: str, sell_price: float = None):
    """Update status dan harga jual token di portfolio"""
    portfolio = load_json(PORTFOLIO_FILE, default=[])
    updated = False
    for token in portfolio:
        if token["symbol"] == symbol and token["status"] == "OPEN":
            token["status"] = status
            token["sell_price"] = round(sell_price, 4) if sell_price else None
            updated = True
            break
    if updated:
        save_json(PORTFOLIO_FILE, portfolio)
