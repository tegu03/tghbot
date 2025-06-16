import re
from utils import parse_number

def extract_token_info(message: str):
    try:
        token_name_match = re.search(r"🔥\s*(.+?)(?:\s*New Whale Buy|\s*Swap|\s*Launch|\s*Buy|🚀)?\s*\n", message)
        token_name = token_name_match.group(1).strip() if token_name_match else "Unknown"

        mc_match = re.search(r"MC:\s*\$([0-9.,KMB]+)", message)
        mc = parse_number(mc_match.group(1)) if mc_match else 0

        liq_match = re.search(r"Liq:\s*\$([0-9.,KMB]+)", message)
        liq = parse_number(liq_match.group(1)) if liq_match else 0

        vol_match = re.search(r"Vol:.*?\$([0-9.,KMB]+)", message)
        vol = parse_number(vol_match.group(1)) if vol_match else 0

        age_match = re.search(r"Age:\s*([^\n|]+)", message)
        age = age_match.group(1).strip() if age_match else "Unknown"

        wallet_match = re.search(r"Wallet:\s*([0-9.]+)\s*SOL", message)
        wallet = float(wallet_match.group(1)) if wallet_match else 0

        symbol_match = re.search(r"https://pump.fun/([a-zA-Z0-9]+)", message)
        token_symbol = symbol_match.group(1).strip() if symbol_match else "UNKNOWN"

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
