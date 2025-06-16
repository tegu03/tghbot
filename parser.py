# parser.py

import re

def extract_token_info(text):
    try:
        # Cari nama token dan simbol dari baris dengan swap detail
        name_match = re.search(r"🔥\s+(.*?)\s+Swap", text)
        token_name = name_match.group(1).strip() if name_match else "UNKNOWN"

        # Marketcap
        mc_match = re.search(r"MC:\s*\$(.*?)\s", text)
        marketcap = float(mc_match.group(1).replace(",", "")) if mc_match else 0

        # Liquidity
        liq_match = re.search(r"Liq:\s*\$(.*?)\n", text)
        liquidity = float(liq_match.group(1).replace(",", "")) if liq_match else 0

        # Volume 1h
        vol_match = re.search(r"Vol:\s*1h:\s*\$(.*?)\n", text)
        volume_1h = float(vol_match.group(1).replace(",", "")) if vol_match else 0

        # Age
        age_match = re.search(r"Age:\s*(.*?)\s*\|", text)
        age = age_match.group(1).strip() if age_match else "UNKNOWN"

        # Whale Wallet info
        whale_match = re.search(r"Wallet Value:\s*(.*?)\s*SOL", text)
        whale_wallet = float(whale_match.group(1)) if whale_match else 0

        # Contact Address (jika tersedia)
        address_match = re.search(r"Wallet Address:.*?([A-Z0-9]{10,})", text)
        contact_address = address_match.group(1) if address_match else ""

        return {
            "token_name": token_name,
            "marketcap": marketcap,
            "liquidity": liquidity,
            "volume_1h": volume_1h,
            "age": age,
            "whale_wallet": whale_wallet,
            "contact_address": contact_address
        }

    except Exception as e:
        print("[Parser Error]", e)
        return None
