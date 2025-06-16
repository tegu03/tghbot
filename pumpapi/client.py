# pumpapi/client.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()

# URL dasar dari PumpPortal API (ganti dengan URL sebenarnya jika berbeda)
BASE_URL = os.getenv("PUMPPORTAL_API_URL", "https://api.pumpportal.io")

def get_token_data_by_name(token_name):
    """
    Mengambil data token dari PumpPortal API berdasarkan nama token.
    """
    try:
        response = requests.get(f"{BASE_URL}/token?name={token_name}")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"[ERROR] Gagal fetch data token: {response.status_code}")
            return None
    except Exception as e:
        print(f"[ERROR] Exception saat fetch data: {e}")
        return None

def get_token_data_by_address(address):
    """
    Mengambil data token berdasarkan contract address (jika diperlukan).
    """
    try:
        response = requests.get(f"{BASE_URL}/token?address={address}")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"[ERROR] Gagal fetch data token by address: {response.status_code}")
            return None
    except Exception as e:
        print(f"[ERROR] Exception saat fetch data by address: {e}")
        return None
