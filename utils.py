# utils.py
from config import GROUP_ID

client = None  # akan di-set dari main.py
portfolio = []  # akan di-inject dari main.py
winrate_data = {}  # akan di-inject dari main.py

def inject_dependencies(c, p, w):
    global client, portfolio, winrate_data
    client = c
    portfolio = p
    winrate_data = w

async def send_message(text: str):
    if client is None:
        print("[ERROR] Client belum diatur di utils.py")
        return
    try:
        await client.send_message(GROUP_ID, text)
    except Exception as e:
        print(f"[ERROR] Gagal mengirim pesan: {e}")

async def handle_monitor_command(event):
    if client is None:
        return
    message = "**📊 Status Bot Saat Ini**\n\n"

    # Token aktif
    if portfolio:
        message += "🟢 Token Aktif (Max 5):\n"
        for idx, token in enumerate(portfolio, 1):
            message += f"{idx}. {token['name']} | Buy: {token['buy_price']}$ | Target: {token['target_price']}$\n"
    else:
        message += "⚪ Tidak ada token aktif.\n"

    # Winrate
    total = winrate_data.get("total", 0)
    wins = winrate_data.get("wins", 0)
    losses = winrate_data.get("losses", 0)
    wr = (wins / total * 100) if total else 0

    message += f"\n🏆 Winrate: {wins}/{total} ({wr:.1f}%)\n"
    message += f"📉 Rugi: {losses} token\n"

    await send_message(message)
