# main.py (final updated)

import asyncio
from telethon import TelegramClient, events
from config import API_ID, API_HASH, SESSION_NAME, CHANNELS, GROUP_ID
from parser import extract_token_info
from scorer import score_token
from buyer import is_already_bought, add_to_portfolio, get_open_positions
from seller import update_position_status, get_winrate, get_closed_positions
from utils import send_message, set_client, generate_explorer_link
from pumpportal import get_realtime_price

MAX_OPEN_POSITIONS = 5
TP_MULTIPLIER = 2.0
SL_MULTIPLIER = 0.75
MOONBAG_PERCENTAGE = 0.2

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
    data = extract_token_info(text)

    if not data:
        print("[SKIP] ❌ Parsing gagal.")
        return

    # Filter Marketcap < $100K
    if data['mc'] > 100000:
        print(f"[SKIP] 💸 Marketcap terlalu besar: ${data['mc']}")
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

    # Simulasi beli token
    buy_price = data['mc'] / 1000
    explorer = generate_explorer_link(data['token_name'])

    add_to_portfolio(
        token_name=data['token_name'],
        mc=data['mc'],
        lp=data['lp'],
        volume=data['volume'],
        age=data['age'],
        wallet=data['wallet'],
        score=score,
        buy_price=buy_price,
        explorer=explorer
    )

    await send_message(
        f"✅ Beli token: {data['token_name']}\n"
        f"Skor: {score}/7\n"
        f"MC: ${data['mc']} | LP: ${data['lp']}\n"
        f"Vol: ${data['volume']} | Usia: {data['age']} detik\n"
        f"Whale: {data['wallet']} SOL\n"
        f"🔗 [Explorer Link]({explorer})\n"
        f"{reason}"
    )

async def monitor_positions():
    while True:
        try:
            for entry in get_open_positions():
                token = entry['token_name']
                current_price = get_realtime_price(token)
                if current_price is None:
                    continue

                buy_price = entry['buy_price']
                tp_price = buy_price * TP_MULTIPLIER
                sl_price = buy_price * SL_MULTIPLIER

                if current_price >= tp_price:
                    moonbag_amount = current_price * MOONBAG_PERCENTAGE
                    update_position_status(token, 'TP', current_price, moonbag=True)
                    await send_message(f"🎯 TP 80%: {token} ✅ @ ${current_price:.4f} (+20% moonbag)")
                elif current_price <= sl_price:
                    update_position_status(token, 'SL', current_price)
                    await send_message(f"🛑 SL: {token} ❌ @ ${current_price:.4f}")

        except Exception as e:
            print(f"[ERROR] Monitor error: {e}")

        await asyncio.sleep(20)

@client.on(events.NewMessage(pattern='/cek'))
async def monitor_status(event):
    open_tokens = get_open_positions()
    closed_tokens = get_closed_positions()
    win, total, wr = get_winrate()

    msg = "📊 Monitoring\n"
    msg += f"Open: {len(open_tokens)} token\n"
    for o in open_tokens:
        msg += f"🔹 {o['token_name']} @ ${o['buy_price']:.4f}\n"
    msg += f"\nClosed: {len(closed_tokens)} token\n"
    for c in closed_tokens:
        status = c['status']
        msg += f"{('✅' if status == 'TP' else '❌')} {c['token_name']} @ ${c['sell_price']:.4f}\n"
    msg += f"\nWinrate: {win}/{total} = {wr}%"

    await event.reply(msg)

@client.on(events.NewMessage(pattern='/reset'))
async def reset_portfolio_cmd(event):
    from buyer import reset_portfolio
    from seller import reset_closed
    reset_portfolio()
    reset_closed()
    await event.reply("🔄 Portofolio & histori penjualan direset.")

@client.on(events.NewMessage)
async def handler(event):
    try:
        await handle_new_message(event)
    except Exception as e:
        print(f"[ERROR] Unhandled: {e}")

async def main():
    while True:
        try:
            await client.start()
            print("✅ Bot aktif dan monitoring berjalan...")
            asyncio.create_task(monitor_positions())
            await client.run_until_disconnected()
        except Exception as e:
            print(f"[ERROR] Reconnecting in 10s: {e}")
            await asyncio.sleep(10)

if __name__ == '__main__':
    asyncio.run(main())
