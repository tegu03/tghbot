# utils.py

import json
import os
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
        return default
    with open(filename, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return default

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
