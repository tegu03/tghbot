# monitor.py

from buyer import get_open_positions
from seller import update_position_status
from utils import send_message
from pumpapi.client import get_token_data_by_name
import asyncio

async def monitor_positions():
    while True:
        open_tokens = get_open_positions()
        for entry in open_tokens:
            token_name = entry['token_name']
            data = get_token_data_by_name(token_name)
            if not data:
                continue

            current_mc = data.get('marketcap', 0)
            current_price = current_mc / 1000

            if current_price >= entry['buy_price'] * 2:
                update_position_status(token_name, 'TP', current_price)
                await send_message(f"🎯 TP: {token_name} ✅ (Price: ${current_price:.2f})")
            elif current_price <= entry['buy_price'] * 0.75:
                update_position_status(token_name, 'SL', current_price)
                await send_message(f"🛑 SL: {token_name} ❌ (Price: ${current_price:.2f})")

        await asyncio.sleep(20)
