# parser.py
import re
from datetime import datetime

def extract_token_info(message_text):
    """
    Mengekstrak informasi token dari pesan teks channel seperti @solwhaletrending atau @phanes.
    Return dict berisi info: name, symbol, address, mc, lp, age, dex.
    """
    try:
        address_match = re.search(r"https://pump\.fun/([A-Za-z0-9]+)", message_text)
        if not address_match:
            return None

        token_address = address_match.group(1)

        name_match = re.search(r"Name:\s*(.+)", message_text)
        name = name_match.group(1).strip() if name_match else "Unknown"

        symbol_match = re.search(r"Symbol:\s*(\S+)", message_text)
        symbol = symbol_match.group(1).strip() if symbol_match else "???"

        mc_match = re.search(r"MC:\s*\$?([\d,.]+)", message_text)
        mc = float(mc_match.group(1).replace(",", "")) if mc_match else 0

        lp_match = re.search(r"LP:\s*\$?([\d,.]+)", message_text)
        lp = float(lp_match.group(1).replace(",", "")) if lp_match else 0

        age_match = re.search(r"Age:\s*([\d.]+)\s*(s|sec|seconds|m|min|minutes)", message_text, re.IGNORECASE)
        if age_match:
            value, unit = float(age_match.group(1)), age_match.group(2).lower()
            if unit.startswith("s"):
                age_sec = int(value)
            else:
                age_sec = int(value * 60)
        else:
            age_sec = 0

        dex = "pump.fun"  # bisa dikembangkan nanti

        return {
            "name": name,
            "symbol": symbol,
            "address": token_address,
            "mc": mc,
            "lp": lp,
            "age": age_sec,
            "dex": dex
        }
    except Exception as e:
        print(f"[ERROR] Gagal parse token info: {e}")
        return None
