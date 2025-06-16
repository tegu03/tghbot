# seller.py (updated for moonbag logic, compatible with main.py)

from buyer import portfolio, save_json
from datetime import datetime

TP_MULTIPLIER = 2.0
SL_MULTIPLIER = 0.75
MOONBAG_PERCENT = 20  # 20% token held after TP


def process_position_updates(get_price_func):
    messages = []
    for entry in portfolio:
        if entry['status'] != 'OPEN':
            continue

        token_name = entry['token_name']
        current_price = get_price_func(token_name)
        if current_price is None:
            continue

        entry['current_price'] = current_price

        if current_price >= entry['buy_price'] * TP_MULTIPLIER:
            # Hit Take Profit
            moonbag_value = current_price * MOONBAG_PERCENT / 100
            profit_value = current_price * (100 - MOONBAG_PERCENT) / 100
            entry['status'] = 'TP'
            entry['sell_price'] = profit_value
            entry['sell_time'] = datetime.now().isoformat()
            entry['result'] = 'WIN'
            messages.append(f"🎯 TP: {token_name} ✅ (80% sold at ${profit_value:.4f}, 20% hold)")

        elif current_price <= entry['buy_price'] * SL_MULTIPLIER:
            # Hit Stop Loss
            entry['status'] = 'SL'
            entry['sell_price'] = current_price
            entry['sell_time'] = datetime.now().isoformat()
            entry['result'] = 'LOSS'
            messages.append(f"🛑 SL: {token_name} ❌ (sold at ${current_price:.4f})")

    save_json('data/portfolio.json', portfolio)
    return messages


def get_winrate():
    closed = [t for t in portfolio if t['status'] in ('TP', 'SL')]
    win = sum(1 for t in closed if t['result'] == 'WIN')
    total = len(closed)
    wr = round((win / total) * 100, 2) if total > 0 else 0.0
    return win, total, wr
