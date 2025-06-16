# parser.py

import re

def parse_number(s):
    """Konversi seperti '30.3K' atau '$100K' jadi float"""
    if isinstance(s, (int, float)):
        return float(s)
    s = str(s).replace('$', '').replace(',', '').strip().upper()
    multiplier = 1
    if s.endswith('K'):
        multiplier = 1_000
        s = s[:-1]
    elif s.endswith('M'):
        multiplier = 1_000_000
        s = s[:-1]
    try:
        return float(s) * multiplier
    except ValueError:
        return 0.0

def extract_token_info(text):
    try:
        # Nama token
        name_match = re.search(r"🔥\s+(.*?)\s+Swap", text)
        token_name = name_match.group(1).strip() if name_match else "UNKNOWN"

        # Marketcap
        mc_match = re.search(r"MC:\s*\$?([\d.,KkMm]+)", text)
        marketcap = parse_number(mc_match.group(1)) if mc_match else 0

        # Liquidity
        liq_match = re.search(r"Liq:\s*\$?([\d.,KkMm]+)", text)
        liquidity = parse_number(liq_match.group(1)) if liq_match else 0

        # Volume 1h
        vol_match = re.search(r"Vol.*?:\s*\$?([\d.,KkMm]+)", text)
        volume_1h = parse_number(vol_match.group(1)) if vol_match else 0

        # Age
        age_match = re.search(r"Age:\s*(.*?)\s*(\||\n|$)", text)
        age = age_match.group(1).strip() if age_match else "UNKNOWN"

        # Whale Wallet
        whale_match = re.search(r"Wallet:\s*([\d.,KkMm]+)\s*SOL", text)
        whale_wallet = parse_number(whale_match.group(1)) if whale_match else 0

        # Contact Address (jika ada)
        address_match = re.search(r"Wallet Address:.*?([A-Z0-9]{10,})", text)
        contact_address = address_match.group(1) if address_match else ""

        return {
            "token_name": token_name,
            "marketcap": marketcap,
            "liquidity": liquidity,
            "volume": volume_1h,
            "age": age,
            "whale_wallet_sol": whale_wallet,
            "contact_address": contact_address
        }

    except Exception as e:
        print("[Parser Error]", e)
        return None
