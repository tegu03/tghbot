# utils.py

import json
import os

TOKEN_FILE = 'portfolio.json'
HISTORY_FILE = 'history.json'

client = None

def set_client(c):
    global client
    client = c

async def send_message(text):
    if client:
        from config import GROUP_ID
        await client.send_message(GROUP_ID, text)

# JSON utils

def load_json(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return []

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

# Link token Pump.fun

def get_token_link(token_name):
    slug = token_name.lower().replace(" ", "").replace("$", "")
    return f"https://pump.fun/{slug}"
