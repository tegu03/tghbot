import re
from utils import parse_number, parse_age

def extract_token_info(message: str):
    try:
        token_name_match = re.search(r"🔥\s*(.+?)(?:\s*New Whale Buy|\s*Swap|\s*Launch|\s*Buy|🚀)?\s*\n", message)
        token_name = token_name_match.group(1).strip() if token_name_match else "Unknown"

        mc_match = re.search(r"MC:\s*\$([0-9.,KMB]+)", message)
        mc = parse_number(mc_match.group(1)) if mc_match else 0

        liq_match = re.search(r"Liq:\s*\$([0-9.,KMB]+)", message)
        liq = parse_number(liq_match.group(1)) if liq_match else 0

        vol_match = re.search(r"Vol.*?:\s*\$([0-9.,KMB]+)", message)
        vol = parse_number(vol_match.group(1)) if vol_match else 0

        age_match = re.search(r"Age:\s*([^\n|]+)", message)
        age_str = age_match.group(1).strip() if age_match else "Unknown"
        age_sec = parse_age(age_str)

        wallet_match = re.search(r"Wallet.*?Value:\s*([0-9.]+)", message)
        whale_wallet_sol = float(wallet_match.group(1)) if wallet_match else 0

        sniper_match = re.search(r"Sniper:\s*(\d+)", message)
        sniper_count = int(sniper_match.group(1)) if sniper_match else 0

        sniper_percent_match = re.search(r"Sniper.*?(\d{1,3})%", message)
        sniper_percent = int(sniper_percent_match.group(1)) if sniper_percent_match else 0

        renounced_match = re.search(r"Renounced|🔒", message)
        renounced = 'renounced' if renounced_match else ''

        symbol_match = re.search(r"https://pump.fun/([a-zA-Z0-9]+)", message)
        token_symbol = symbol_match.group(1).strip() if symbol_match else "UNKNOWN"

        return {
            "token_name": token_name,
            "symbol": token_symbol,
            "marketcap": mc,
            "liquidity": liq,
            "volume": vol,
            "wallet": whale_wallet_sol,
            "whale_wallet_sol": whale_wallet_sol,
            "age": age_str,
            "age_seconds": age_sec,
            "renounced": renounced,
            "sniper_count": sniper_count,
            "sniper_percent": sniper_percent
        }

    except Exception as e:
        print(f"[Parser Error] {e}")
        return None
