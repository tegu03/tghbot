# buyer.py (updated)

portfolio = []


def is_already_bought(token_name):
    return any(entry['token_name'].lower() == token_name.lower() for entry in portfolio)


def add_to_portfolio(token_name, mc, lp, volume, age, wallet, score, buy_price, explorer):
    portfolio.append({
        'token_name': token_name,
        'mc': mc,
        'lp': lp,
        'volume': volume,
        'age': age,
        'wallet': wallet,
        'score': score,
        'buy_price': buy_price,
        'explorer': explorer,
        'status': 'OPEN'
    })


def get_open_positions():
    return [entry for entry in portfolio if entry['status'] == 'OPEN']


def mark_as_closed(token_name, status, sell_price, moonbag=False):
    for entry in portfolio:
        if entry['token_name'].lower() == token_name.lower() and entry['status'] == 'OPEN':
            entry['status'] = status
            entry['sell_price'] = sell_price
            entry['moonbag'] = moonbag
            break


def reset_portfolio():
    global portfolio
    portfolio = []
