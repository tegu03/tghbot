# parser.py

import re

def parse_number(value):
    value = value.replace(",", "").strip().upper()
    if value.endswith("K"):
        return float(value[:-1]) * 1_000
    elif value.endswith("M"):
        return float(value[:-1]) * 1_000_000
    elif value.endswith("B"):
        return float(value[:-1]) * 1_000_000_000
    else:
        return float(value)

def parse_age_to_seconds(age_str):
    age_str = age_str.strip().lower()
    if 'mo' in age_str:
        return int(re.search(r'(\d+)', age_str).group(1)) * 30 * 24 * 3600
    elif 'w' in age_str:
        return int(re.search(r'(\d+)', age_str).group(1)) * 7 * 24 * 3600
    elif 'd' in age_str:
        return int(re.search(r'(\d+)', age_str).group(1)) * 24 * 3600
    elif 'h' in age_str:
        return int(re.search(r'(\d+)', age_str).group(1)) * 3600
    elif 'm' in age_str:
        return int(re.search(r'(\d+)', age_str).group(1)) * 60
    else:
        return 0

def extract_token_info(text):
    try:
        token_name_match = re.search(r"🔥\s+(.*?)\s+(New|Whale|Buy|Swap)", text, re.IGNORECASE)
        token_name = token_name_match.group(1).strip() if token_name_match else "UNKNOWN"

        mc_match = re.search(r"MC:\s*\$([\d.,KMB]+)", text)
        marketcap = parse_number(mc_match.group(1)) if mc_match else 0

        liq_match = re.search(r"Liq:\s*\$([\d.,KMB]+)", text)
        liquidity = parse_number(liq_match.group(1)) if liq_match else 0

        vol_match = re.search(r"Vol:.*?\$([\d.,KMB]+)", text)
        volume = parse_number(vol_match.group(1)) if vol_match else 0

        age_match = re.search(r"Age:\s*([^\|]+)", text)
        age_str = age_match.group(1).strip() if age_match else "0m"
        age_seconds = parse_age_to_seconds(age_str)

        whale_match = re.search(r"Wallet:\s*([\d.]+)\s*SOL", text)
        whale_wallet = float(whale_match.group(1)) if whale_match else 0

        address_match = re.search(r"Wallet Address:.*?([A-Z0-9]{10,})", text)
        contact_address = address_match.group(1) if address_match else ""

        return {
            "token_name": token_name,
            "marketcap": marketcap,
            "liquidity": liquidity,
            "volume": volume,
            "age_seconds": age_seconds,
            "whale_wallet_sol": whale_wallet,
            "contact_address": contact_address
        }

    except Exception as e:
        print("[Parser Error]", e)
        return None
