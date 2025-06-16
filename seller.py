# seller.py (updated)

from buyer import portfolio


def get_closed_positions():
    return [entry for entry in portfolio if entry['status'] in ('TP', 'SL')]


def get_winrate():
    closed = get_closed_positions()
    win = sum(1 for t in closed if t['status'] == 'TP')
    total = len(closed)
    wr = round((win / total) * 100, 1) if total else 0.0
    return win, total, wr


def get_trade_history():
    return [
        f"{entry['token_name']}: {entry['status']} @ ${entry['sell_price']:.2f}"
        for entry in get_closed_positions()
    ]
