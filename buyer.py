# buyer.py

portfolio = []

def is_already_bought(token_name):
    """Cek apakah token sudah dibeli dan statusnya masih terbuka (OPEN)"""
    return any(p['token'] == token_name and p['status'] == 'OPEN' for p in portfolio)

def add_to_portfolio(token, mc, lp, volume, age, wallet, score, buy_price):
    """Tambah token ke dalam portofolio simulasi"""
    portfolio.append({
        'token': token,
        'mc': mc,
        'lp': lp,
        'volume': volume,
        'age': age,
        'wallet': wallet,
        'score': score,
        'buy_price': buy_price,
        'status': 'OPEN'
    })

def get_open_positions():
    """Ambil semua posisi token yang masih OPEN"""
    return [p for p in portfolio if p['status'] == 'OPEN']

def update_token_status(token_name, status, price=None):
    """Update status token (TP/SL/CLOSE), bisa juga menyimpan harga jual"""
    for p in portfolio:
        if p['token'] == token_name and p['status'] == 'OPEN':
            p['status'] = status
            if price:
                p['sell_price'] = price
            break

def reset_portfolio():
    """Reset seluruh portofolio (untuk percobaan ulang)"""
    global portfolio
    portfolio = []

def get_winrate():
    """Hitung winrate berdasarkan hasil TP dan SL"""
    total = 0
    win = 0
    for p in portfolio:
        if p['status'] == 'TP':
            win += 1
            total += 1
        elif p['status'] == 'SL':
            total += 1
    if total == 0:
        return 0, 0, 0.0
    wr = (win / total) * 100
    return win, total, round(wr, 2)
