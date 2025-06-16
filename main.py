# main.py

import asyncio
from telethon import TelegramClient, events
from config import API_ID, API_HASH, SESSION_NAME, CHANNELS, GROUP_ID
from parser import extract_token_info
from scorer import score_token
from buyer import add_to_portfolio, get_open_positions, reset_portfolio
from seller import update_position_status, get_winrate
from utils import send_message, set_client
from price_fetcher import get_price_by_token_name  # Harga real-time

MAX_OPEN_POSITIONS = 5

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
set_client(client)

async def handle_new_message(event):
    sender_username = getattr(event.chat, 'username', None)
    chat_id = event.chat_id

    print(f"[LOG] 🔔 Pesan masuk dari: {sender_username or chat_id}")

    allowed = False
    if sender_username and sender_username.lower() in [c.lower() for c in CHANNELS]:
        allowed = True
    elif chat_id == GROUP_ID:
        allowed = True

    if not allowed:
        print("[SKIP] 🚫 Bukan dari channel/grup yang diizinkan.")
        return

    text = event.raw_text
    print("[DEBUG] ✉️ Teks pesan:")
    print(text)

    data = extract_token_info(text)
    print(f"[DEBUG] 🔍 Parsed data: {data}")

    if not data:
        print("[SKIP] ❌ Parsing gagal.")
        return

    score, reason = score_token(data)
    print(f"[DEBUG] 🧠 Skor: {score} | Alasan: {reason}")

    if score < 3:
        print(f"[SKIP] ⛔ Skor terlalu rendah: {score}")
        return

    open_tokens = get_open_positions()
    if data['token_name'] in [t['token_name'] for t in open_tokens]:
        print(f"[SKIP] 🔁 Token {data['token_name']} sudah dibeli.")
        return

    if len(open_tokens) >= MAX_OPEN_POSITIONS:
        print("[SKIP] 📦 Posisi maksimum tercapai.")
        return

    # Simulasi beli berdasarkan MC
    buy_price = data['mc'] / 1000
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
            current_mc = get_price_by_token_name(entry['token_name'])
            if current_mc is None or current_mc == 0:
                continue

            now_price = current_mc / 1000
            if now_price >= entry['buy_price'] * 2:
                update_position_status(entry['token_name'], 'TP', now_price)
                await send_message(f"🎯 TP: {entry['token_name']} ✅")
            elif now_price <= entry['buy_price'] * 0.75:
                update_position_status(entry['token_name'], 'SL', now_price)
                await send_message(f"🛑 SL: {entry['token_name']} ❌")
        await asyncio.sleep(30)

@client.on(events.NewMessage(pattern='/cek'))
async def monitor_status(event):
    open_tokens = get_open_positions()
    win, total, wr = get_winrate()
    msg = f"📊 Monitoring\nOpen: {len(open_tokens)} token\nWinrate: {win}/{total} = {wr}%"
    await event.reply(msg)

@client.on(events.NewMessage(pattern='/reset'))
async def reset_command(event):
    reset_portfolio()
    await event.reply("🔄 Semua posisi telah di-reset.")

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
