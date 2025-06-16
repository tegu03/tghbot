import asyncio
from pumpapi.client import get_token_data_by_name
from buyer import get_open_positions
from seller import update_position_status
from utils import send_message

async def monitor_positions():
    while True:
        open_positions = get_open_positions()
        for entry in open_positions:
            token_name = entry['token_name']
            token_data = get_token_data_by_name(token_name)

            if not token_data:
                continue

            current_mc = token_data.get('marketcap', 0)
            if current_mc == 0:
                continue

            now_price = current_mc / 1000
            buy_price = entry['buy_price']

            if now_price >= buy_price * 2:
                update_position_status(token_name, 'TP', now_price)
                await send_message(f"🎯 TP: {token_name} ✅ (${now_price:.2f})")
            elif now_price <= buy_price * 0.75:
                update_position_status(token_name, 'SL', now_price)
                await send_message(f"🛑 SL: {token_name} ❌ (${now_price:.2f})")

        await asyncio.sleep(60)
