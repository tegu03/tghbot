# seller.py

portfolio = []
closed_positions = []

def get_open_positions():
    return [entry for entry in portfolio if entry['status'] == 'OPEN']

def get_closed_positions():
    return closed_positions

def is_already_bought(token_name):
    return any(entry['token_name'] == token_name and entry['status'] == 'OPEN' for entry in portfolio)

def add_to_portfolio(token_name, mc, lp, vol, age, wallet, score, buy_price, contact_address):
    portfolio.append({
        'token_name': token_name,
        'mc': mc,
        'lp': lp,
        'volume': vol,
        'age': age,
        'wallet': wallet,
        'score': score,
        'buy_price': buy_price,
        'contact_address': contact_address,
        'status': 'OPEN'
    })

def update_position_status(token_name, status, sell_price):
    for entry in portfolio:
        if entry['token_name'] == token_name and entry['status'] == 'OPEN':
            entry['status'] = status
            entry['sell_price'] = sell_price
            closed_positions.append(entry)
            break

def reset_portfolio():
    portfolio.clear()
    closed_positions.clear()

def get_winrate():
    total = len(closed_positions)
    win = sum(1 for entry in closed_positions if entry['status'] == 'TP')
    wr = round((win / total) * 100, 2) if total > 0 else 0.0
    return win, total, wr
