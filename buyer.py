import asyncio
import time
from seller import update_position_status, get_winrate
from utils import send_message
from pumpapi.client import get_token_data_by_name

CHECK_INTERVAL = 60  # Detik
TP_MULTIPLIER = 2.0
SL_MULTIPLIER = 0.75

async def monitor_positions():
    while True:
        positions = get_open_positions()
        for token in positions:
            token_name = token['token_name']
            try:
                latest_data = get_token_data_by_name(token_name)
                if not latest_data:
                    continue
                current_mc = latest_data.get('mc')
                if not current_mc:
                    continue

                buy_price = token['buy_price']
                now_price = current_mc / 1000  # Asumsikan harga berdasarkan marketcap

                if now_price >= buy_price * TP_MULTIPLIER:
                    update_position_status(token_name, 'TP', now_price)
                    await send_message(f"🎯 TP: {token_name} ✅ Harga: {now_price:.4f} SOL")
                elif now_price <= buy_price * SL_MULTIPLIER:
                    update_position_status(token_name, 'SL', now_price)
                    await send_message(f"🛑 SL: {token_name} ❌ Harga: {now_price:.4f} SOL")

            except Exception as e:
                print(f"[ERROR] Monitor gagal untuk {token_name}: {e}")
        await asyncio.sleep(CHECK_INTERVAL)

async def monitor_status(event):
    open_tokens = get_open_positions()
    win, total, wr = get_winrate()
    msg = f"📊 Monitoring\nOpen: {len(open_tokens)} token\nWinrate: {win}/{total} = {wr}%"
    await event.reply(msg)
