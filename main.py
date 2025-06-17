# main.py

import asyncio
from datetime import datetime
from telethon import TelegramClient, events
from config import (
    API_ID, API_HASH, SESSION_NAME, CHANNELS, GROUP_ID,
    MAX_OPEN_POSITIONS, MIN_SCORE_TO_BUY, MAX_MARKETCAP,
    TP_MULTIPLIER, SL_MULTIPLIER, MOONBAG_RATIO
)
from parser import extract_token_info
from scorer import score_token
from buyer import is_already_bought, add_to_portfolio, get_open_positions, reset_portfolio
from seller import update_position_status, get_winrate, get_closed_positions
from pumpportal import fetch_token_price_by_address
from utils import send_message, set_client

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
set_client(client)

async def handle_new_message(event):
    sender_username = getattr(event.chat, 'username', None)
    chat_id = event.chat_id

    if not (sender_username and sender_username.lower() in [c.lower() for c in CHANNELS] or chat_id == GROUP_ID):
        print("[SKIP] 🚫 Bukan dari channel/grup yang diizinkan.")
        return

    text = event.raw_text
    data = extract_token_info(text)
    if not data:
        print("[SKIP] ❌ Parsing gagal.")
        return

    score, reasons = score_token(data)
    if score < MIN_SCORE_TO_BUY:
        print(f"[SKIP] ⛔ Skor {score} kurang dari {MIN_SCORE_TO_BUY}")
        return

    if data['marketcap'] > MAX_MARKETCAP:
        print(f"[SKIP] 💸 Marketcap terlalu besar: ${data['marketcap']}")
        return

    if is_already_bought(data['token_name']):
        print(f"[SKIP] 🔁 Token {data['token_name']} sudah dibeli.")
        return

    if len(get_open_positions()) >= MAX_OPEN_POSITIONS:
        print("[SKIP] 📦 Posisi maksimum tercapai.")
        return

    # Simulasi harga beli awal
    buy_price = data['marketcap'] / 1000

    add_to_portfolio(
        token_name=data['token_name'],
        token_address=data['symbol'],
        symbol=data['symbol'],
        buy_price=buy_price,
        buy_time=datetime.now().isoformat(),
        marketcap=data['marketcap'],
        liquidity=data['liquidity'],
        volume=data['volume'],
        wallet=data['wallet'],
        age=data['age'],
        score=score
    )

    await send_message(
        f"✅ Beli token: {data['token_name']}\n"
        f"Skor: {score}/7\n"
        f"MC: ${data['marketcap']} | LP: ${data['liquidity']}\n"
        f"Vol: ${data['volume']} | Usia: {data['age']}\n"
        f"Whale: {data['wallet']} SOL\n"
        f"🔗 https://pump.fun/{data['symbol']}\n"
        + "\n".join(reasons)
    )

async def monitor_positions():
    while True:
        try:
            for entry in get_open_positions():
                now_price = await fetch_token_price_by_address(entry['token_address'])
                if not now_price:
                    continue

                buy_price = entry['buy_price']
                token = entry['token_name']

                if now_price >= buy_price * TP_MULTIPLIER:
                    sell_price = now_price * (1 - MOONBAG_RATIO)
                    update_position_status(token, "TP", sell_price)
                    await send_message(f"🎯 TP 80%: {token} @ ${sell_price:.4f} ✅\n20% disimpan sebagai moonbag.")
                elif now_price <= buy_price * SL_MULTIPLIER:
                    update_position_status(token, "SL", now_price)
                    await send_message(f"🛑 SL: {token} @ ${now_price:.4f} ❌")
        except Exception as e:
            print(f"[monitor_positions] ⚠️ Error: {e}")
        await asyncio.sleep(30)

@client.on(events.NewMessage(pattern='/cek'))
async def monitor_status(event):
    open_tokens = get_open_positions()
    closed_tokens = get_closed_positions()
    win, total, wr = get_winrate()

    msg = f"📊 Monitoring\nOpen: {len(open_tokens)} token\nWinrate: {win}/{total} = {wr:.1f}%\n\n"

    if open_tokens:
        msg += "📥 Dibeli:\n"
        for t in open_tokens:
            short_name = t['token_name'].split()[0].upper()
            symbol = t['symbol']
            msg += f"- {short_name} (`{symbol}`) Buy! @ ${t['buy_price']:.4f}\n"

    if closed_tokens:
        msg += "\n📤 Terjual:\n"
        for t in closed_tokens[-5:]:
            short_name = t['token_name'].split()[0].upper()
            symbol = t['symbol']
            status = "TP" if t["status"] == "TP" else "SL"
            msg += f"- {short_name} (`{symbol}`) {status} @ ${t['sell_price']:.4f}\n"

    await event.reply(msg)

@client.on(events.NewMessage(pattern='/reset'))
async def reset_handler(event):
    reset_portfolio()
    await event.reply("🔄 Portfolio telah di-reset.")

@client.on(events.NewMessage)
async def handler(event):
    await handle_new_message(event)

async def main():
    while True:
        try:
            await client.start()
            print("✅ Bot aktif dan monitoring berjalan...")
            asyncio.create_task(monitor_positions())
            await client.run_until_disconnected()
        except Exception as e:
            print(f"[RESTART] 🔁 Bot restart karena error: {e}")
            await asyncio.sleep(5)

if __name__ == '__main__':
    asyncio.run(main())
