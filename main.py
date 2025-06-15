# main.py

import asyncio
from telethon import TelegramClient, events
from config import API_ID, API_HASH, SESSION_NAME, CHANNELS, GROUP_ID
from parser import extract_token_info
from scorer import score_token
from buyer import is_already_bought, add_to_portfolio, get_open_positions
from seller import update_position_status, get_winrate
from utils import send_message, set_client

MAX_OPEN_POSITIONS = 5

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
set_client(client)

async def handle_new_message(event):
    sender_username = getattr(event.chat, 'username', None)
    chat_id = event.chat_id

    # Debug log
    print(f"[LOG] Pesan dari: {sender_username} | Chat ID: {chat_id}")

    # Izinkan hanya jika dari channel yang diizinkan atau grup pribadi (untuk testing)
    if sender_username:
        if sender_username.lower() not in [c.lower() for c in CHANNELS]:
            return
    elif chat_id != GROUP_ID:
        return

    text = event.raw_text
    data = extract_token_info(text)
    if not data:
        return

    score, reason = score_token(data)
    if score < 3:
        return

    if is_already_bought(data['token_name']):
        return

    if len(get_open_positions()) >= MAX_OPEN_POSITIONS:
        return

    # Simulasi beli token
    buy_price = data['mc'] / 1000  # Simulasi harga beli
    add_to_portfolio(
        data['token_name'],
        data['mc'],
        data['lp'],
        data['volume'],
        data['age'],
        data['wallet'],
        score,
        buy_price
    )

    await send_message(
        f"✅ Beli token: {data['token_name']}\n"
        f"Skor: {score}/7\n"
        f"MC: ${data['mc']} | LP: ${data['lp']}\n"
        f"Vol: ${data['volume']} | Usia: {data['age']} detik\n"
        f"Whale: {data['wallet']} SOL\n"
        f"{reason}"
    )

async def monitor_positions():
    while True:
        for entry in get_open_positions():
            now_price = entry['mc'] / 1000 * 1.8  # Simulasi naik turun harga
            if now_price >= entry['buy_price'] * 2:
                update_position_status(entry['token_name'], 'TP', now_price)
                await send_message(f"🎯 TP: {entry['token_name']} ✅")
            elif now_price <= entry['buy_price'] * 0.75:
                update_position_status(entry['token_name'], 'SL', now_price)
                await send_message(f"🛑 SL: {entry['token_name']} ❌")
        await asyncio.sleep(20)

@client.on(events.NewMessage(pattern='/cek'))
async def monitor_status(event):
    open_tokens = get_open_positions()
    win, total, wr = get_winrate()
    msg = f"📊 Monitoring\nOpen: {len(open_tokens)} token\nWinrate: {win}/{total} = {wr}%"
    await event.reply(msg)

@client.on(events.NewMessage)
async def handler(event):
    await handle_new_message(event)

async def main():
    await client.start()
    print("✅ Bot aktif dan monitoring berjalan...")
    asyncio.create_task(monitor_positions())
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
