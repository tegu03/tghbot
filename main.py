# main.py

import asyncio
from telethon import TelegramClient, events
from config import API_ID, API_HASH, SESSION_NAME, CHANNELS, GROUP_ID
from parser import extract_token_info
from scorer import score_token
from buyer import add_to_portfolio, get_open_positions, is_already_bought
from seller import update_position_status, get_winrate, get_sell_history
from utils import send_message, set_client, generate_explorer_link

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
    data = extract_token_info(text)
    print(f"[DEBUG] 🔍 Parsed data: {data}")

    if not data:
        print("[SKIP] ❌ Parsing gagal.")
        return

    if data['mc'] > 100000:
        print("[SKIP] ⛔ MC terlalu besar")
        return

    score, reason = score_token(data)
    print(f"[DEBUG] 🧠 Skor: {score} | Alasan: {reason}")

    if score < 5:
        print(f"[SKIP] ⛔ Skor terlalu rendah: {score}")
        return

    if is_already_bought(data['token_name']):
        print(f"[SKIP] 🔁 Token {data['token_name']} sudah dibeli.")
        return

    if len(get_open_positions()) >= MAX_OPEN_POSITIONS:
        print("[SKIP] 📦 Posisi maksimum tercapai.")
        return

    buy_price = data['mc'] / 1000
    explorer_link = generate_explorer_link(data['token_name'])

    add_to_portfolio(
        data['token_name'],
        data['mc'],
        data['lp'],
        data['volume'],
        data['age'],
        data['wallet'],
        score,
        buy_price,
        explorer_link
    )

    await send_message(
        f"✅ Beli token: {data['token_name']}\n"
        f"Skor: {score}/7\n"
        f"MC: ${data['mc']} | LP: ${data['lp']}\n"
        f"Vol: ${data['volume']} | Usia: {data['age']} detik\n"
        f"Whale: {data['wallet']} SOL\n"
        f"{reason}\n"
        f"🔗 {explorer_link}"
    )

async def monitor_positions():
    while True:
        try:
            for entry in get_open_positions():
                now_price = entry['mc'] / 1000 * 1.8
                if now_price >= entry['buy_price'] * 2:
                    update_position_status(entry['token_name'], 'TP', now_price, moonbag=True)
                    await send_message(f"🎯 TP (80%): {entry['token_name']} ✅ @$now_price")
                elif now_price <= entry['buy_price'] * 0.75:
                    update_position_status(entry['token_name'], 'SL', now_price)
                    await send_message(f"🛑 SL: {entry['token_name']} ❌ @$now_price")
            await asyncio.sleep(20)
        except Exception as e:
            print(f"[ERROR] monitor_positions: {e}")
            await asyncio.sleep(5)

@client.on(events.NewMessage(pattern='/cek'))
async def monitor_status(event):
    open_tokens = get_open_positions()
    sell_tokens = get_sell_history()
    win, total, wr = get_winrate()
    msg = f"📊 Monitoring\nOpen: {len(open_tokens)} token\nWinrate: {win}/{total} = {wr}%\n\n"
    if open_tokens:
        msg += "📈 Dibeli:\n"
        for t in open_tokens:
            msg += f"- {t['token_name']} @${t['buy_price']}\n🔗 {t['explorer']}\n"
    if sell_tokens:
        msg += "\n💸 Terjual:\n"
        for t in sell_tokens[-5:]:
            msg += f"- {t['token_name']} @${t['sell_price']} ({t['status']})\n"
    await event.reply(msg)

@client.on(events.NewMessage(pattern='/reset'))
async def reset_positions(event):
    from buyer import reset_portfolio
    reset_portfolio()
    await event.reply("🔄 Portofolio direset untuk uji coba.")

@client.on(events.NewMessage)
async def handler(event):
    try:
        await handle_new_message(event)
    except Exception as e:
        print(f"[ERROR] handler: {e}")

async def main():
    while True:
        try:
            await client.start()
            print("✅ Bot aktif dan monitoring berjalan...")
            asyncio.create_task(monitor_positions())
            await client.run_until_disconnected()
        except Exception as e:
            print(f"[RECONNECT] {e}")
            await asyncio.sleep(5)

if __name__ == '__main__':
    asyncio.run(main())
