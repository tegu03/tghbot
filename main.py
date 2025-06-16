# main.py

import asyncio
import os
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

    print(f"[LOG] 🔔 Pesan masuk dari: {sender_username or chat_id}")

    # Izinkan jika dari channel whitelist ATAU grup pribadi
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

    if is_already_bought(data['token_name']):
        print(f"[SKIP] 🔁 Token {data['token_name']} sudah dibeli.")
        return

    if len(get_open_positions()) >= MAX_OPEN_POSITIONS:
        print("[SKIP] 📦 Posisi maksimum tercapai.")
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

@client.on(events.NewMessage(pattern='/reset'))
async def reset_bot(event):
    try:
        for file in ["portfolio.json", "winrate.json"]:
            file_path = os.path.join(os.path.dirname(__file__), file)
            if os.path.exists(file_path):
                os.remove(file_path)
        await event.reply("✅ Bot telah di-reset. Portfolio dan winrate dikosongkan.")
        print("[INFO] Bot direset manual via /reset")
    except Exception as e:
        await event.reply(f"❌ Gagal mereset bot: {e}")

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
