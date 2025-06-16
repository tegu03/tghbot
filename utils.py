# utils.py

import json
import os

client = None

PORTFOLIO_FILE = 'data/portfolio.json'
CLOSED_FILE = 'data/closed.json'


def set_client(c):
    global client
    client = c


def send_message(message):
    if client:
        from config import GROUP_ID
        return client.send_message(GROUP_ID, message)
    else:
        print("[ERROR] Client belum diatur.")


def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def get_open_positions():
    return load_json(PORTFOLIO_FILE)


def get_closed_positions():
    return load_json(CLOSED_FILE)


def save_open_positions(data):
    save_json(PORTFOLIO_FILE, data)


def save_closed_positions(data):
    save_json(CLOSED_FILE, data)


def reset_portfolio():
    save_json(PORTFOLIO_FILE, [])
    save_json(CLOSED_FILE, [])
