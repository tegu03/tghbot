import json
import os
import re
from telethon import TelegramClient

# Private global client instance
_client = None

# ===== Telegram Client Manager =====

def set_client(client: TelegramClient):
    """Set global Telegram client instance"""
    global _client
    _client = client

def get_client():
    """Get global Telegram client instance"""
    return _client

async def send_message(message: str):
    """Kirim pesan ke grup Telegram dari bot"""
    if _client:
        from config import GROUP_ID
        try:
            await _client.send_message(GROUP_ID, message)
        except Exception as e:
            print(f"[ERROR] Failed to send message: {e}")
    else:
        print("[WARNING] Telegram client not set")

# ===== JSON File Utilities =====

def load_json(filename, default=None):
    """Load data dari file JSON"""
    if not os.path.exists(filename):
        return default
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"[JSON LOAD ERROR] {filename}: {e}")
        return default

def save_json(filename, data):
    """Simpan data ke file JSON"""
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"[JSON SAVE ERROR] {filename}: {e}")

# ===== String Parsers =====

def parse_number(s):
    """Ubah string K/M/B menjadi angka float"""
    try:
        s = str(s).replace(',', '').strip().upper()
        if s.endswith('K'):
            return float(s[:-1]) * 1_000
        elif s.endswith('M'):
            return float(s[:-1]) * 1_000_000
        elif s.endswith('B'):
            return float(s[:-1]) * 1_000_000_000
        else:
            return float(s)
    except:
        return 0.0

def parse_age(age_str):
    """Ubah usia seperti '2m 30s' jadi detik"""
    try:
        if not isinstance(age_str, str):
            return 0
        age_str = age_str.lower().replace(" ", "")
        total_seconds = 0
        time_units = {
            'mo': 2592000,
            'w': 604800,
            'd': 86400,
            'h': 3600,
            'm': 60,
            's': 1
        }
        # Tangkap semua grup angka + unit (misal: 2m, 30s)
        matches = re.findall(r'(\d+)(mo|w|d|h|m|s)', age_str)
        for value, unit in matches:
            total_seconds += int(value) * time_units.get(unit, 0)
        return total_seconds
    except Exception as e:
        print(f"[parse_age ERROR] {e}")
        return 0
