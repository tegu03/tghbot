# utils.py

import json
import os
import re
from telethon import TelegramClient

_client = None


def set_client(client: TelegramClient):
    global _client
    _client = client


def get_client():
    return _client


async def send_message(message: str):
    if _client:
        from config import GROUP_ID
        try:
            await _client.send_message(GROUP_ID, message)
        except Exception as e:
            print(f"[ERROR] Failed to send message: {e}")


def load_json(filename, default=None):
    if not os.path.exists(filename):
        return default if default is not None else []
    with open(filename, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return default if default is not None else []


def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)


def parse_number(text):
    """
    Mengubah string seperti '30.4K' menjadi float 30400.0
    """
    try:
        multipliers = {'K': 1_000, 'M': 1_000_000, 'B': 1_000_000_000}
        match = re.match(r'([0-9,.]+)([KMB]?)', text.upper().replace(',', ''))
        if not match:
            return float(text)
        number, suffix = match.groups()
        return float(number) * multipliers.get(suffix, 1)
    except Exception:
        return 0.0
