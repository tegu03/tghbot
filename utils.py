import json
import os
from telethon import TelegramClient
from config import GROUP_ID

client = None

def set_client(c):
    global client
    client = c

async def send_message(text):
    if client:
        await client.send_message(GROUP_ID, text)

def load_json(filename, default=None):
    if not os.path.exists(filename):
        return default
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except Exception:
        return default

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

def parse_number(text):
    multipliers = {'K': 1_000, 'M': 1_000_000, 'B': 1_000_000_000}
    text = text.upper().replace(",", "").strip()
    if text[-1] in multipliers:
        return float(text[:-1]) * multipliers[text[-1]]
    return float(text)
