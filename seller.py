from utils import load_json, save_json
from config import PORTFOLIO_FILE, MOONBAG_RATIO, STATUS_FILE

def update_position_status(token_name, status, sell_price):
    """Update status posisi berdasarkan token name"""
    portfolio = load_json(PORTFOLIO_FILE, default=[])
    updated = False

    for token in portfolio:
        if token['token_name'] == token_name and token['status'] == 'OPEN':
            if status == 'TP' and MOONBAG_RATIO > 0:
                token['status'] = 'HOLD'
                token['sell_price'] = round(sell_price * (1 - MOONBAG_RATIO), 4)
                token['moonbag_price'] = round(sell_price * MOONBAG_RATIO, 4)
                token['moonbag_ratio'] = MOONBAG_RATIO
            else:
                token['status'] = status
                token['sell_price'] = round(sell_price, 4)
            updated = True
            break

    if updated:
        save_json(PORTFOLIO_FILE, portfolio)
        write_status_json()

def get_winrate():
    """Hitung winrate (TP/SL)"""
    portfolio = load_json(PORTFOLIO_FILE, default=[])
    total = sum(1 for t in portfolio if t['status'] in ['TP', 'SL'])
    win = sum(1 for t in portfolio if t['status'] == 'TP')
    wr = round((win / total) * 100, 2) if total > 0 else 0.0
    return win, total, wr

def get_closed_positions():
    """Ambil semua posisi yang statusnya bukan OPEN"""
    portfolio = load_json(PORTFOLIO_FILE, default=[])
    return [t for t in portfolio if t['status'] in ['TP', 'SL', 'HOLD']]

def write_status_json():
    """Simpan status.json untuk visual log"""
    portfolio = load_json(PORTFOLIO_FILE, default=[])
    win, total, wr = get_winrate()
    status_data = {
        "win": win,
        "total": total,
        "winrate_percent": wr,
        "open_positions": [t for t in portfolio if t.get("status") == "OPEN"],
        "closed_positions": [t for t in portfolio if t.get("status") in ("TP", "SL", "HOLD")]
    }
    save_json(STATUS_FILE, status_data)
