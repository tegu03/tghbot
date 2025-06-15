# utils.py
from config import GROUP_ID

client = None  # akan di-inject dari main.py

def set_client(c):
    global client
    client = c

async def send_message(text: str):
    if client is None:
        print("[ERROR] Client belum diatur di utils.py")
        return
    try:
        await client.send_message(GROUP_ID, text)
    except Exception as e:
        print(f"[ERROR] Gagal mengirim pesan: {e}")
