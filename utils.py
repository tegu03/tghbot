# utils.py

import json
import os
from telethon import TelegramClient

DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

client = None

def set_client(c):
    global client
    client = c

def send_message(message):
    from config import GROUP_ID
    if client:
        return client.send_message(GROUP_ID, message)

def load_json(filepath, default=None):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default if default is not None else {}

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def get_token_link(token_name):
    return f"https://pump.fun/{token_name.replace('$', '')}"
