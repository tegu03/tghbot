import re
from utils import parse_number

def extract_token_info(message: str):
    try:
        token_name_match = re.search(r"🔥\s*(.+?)\s*(?:New Whale Buy|Swap|Launch|Buy|🚀)?\s*[\n|$]", message)
        token_name = token_name_match.group(1).strip() if token_name_match else "Unknown"

        mc_match = re.search(r"MC:.*?\$([0-9.,KMB]+)", message)
        mc = parse_number(mc_match.group(1)) if mc_match else 0

        liq_match = re.search(r"Liq:.*?\$([0-9.,KMB]+)", message)
        liq = parse_number(liq_match.group(1)) if liq_match else 0

        vol_match = re.search(r"Vol:.*?\$([0-9.,KMB]+)", message)
        vol = parse_number(vol_match.group(1)) if vol_match else 0

        age_match = re.search(r"Age: ([^\n|]+)", message)
        age = age_match.group(1).strip() if age_match else "0"

        wallet_match = re.search(r"Wallet: (\d+)", message)
        wallet = int(wallet_match.group(1)) if wallet_match else 0

        contact_match = re.search(r"\$([A-Z0-9]{3,})", message)
        token_symbol = contact_match.group(1).strip() if contact_match else "UNKNOWN"

        return {
            "token_name": token_name,
            "symbol": token_symbol,
            "marketcap": mc,
            "liquidity": liq,
            "volume": vol,
            "wallet": wallet,
            "age": age
        }
    except Exception as e:
        print(f"[Parser Error] {e}")
        return None
