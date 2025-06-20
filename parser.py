import re
from utils import parse_number, parse_age

def extract_token_info(message: str, raw_entities=None):
    try:
        # 1. Nama token (dari baris awal dengan kata “New Whale Buy” atau “Swap”)
        token_name_match = re.search(r"🔥\s*\"?(.+?)\"?\s*(?:New Whale Buy|Swap|Launch|Buy|🚀)?\s*\n", message)
        token_name = token_name_match.group(1).strip() if token_name_match else "Unknown"

        # 2. Marketcap
        mc_match = re.search(r"MC:\s*\$([0-9.,KMB]+)", message)
        marketcap = parse_number(mc_match.group(1)) if mc_match else 0

        # 3. Liquidity
        liq_match = re.search(r"Liq:\s*\$([0-9.,KMB]+)", message)
        liquidity = parse_number(liq_match.group(1)) if liq_match else 0

        # 4. Volume 1h
        vol_match = re.search(r"Vol.*?:\s*\$([0-9.,KMB]+)", message)
        volume = parse_number(vol_match.group(1)) if vol_match else 0

        # 5. Age
        age_match = re.search(r"Age:\s*([^\n|]+)", message)
        age_str = age_match.group(1).strip() if age_match else "Unknown"
        age_seconds = parse_age(age_str)

        # 6. Whale Wallet
        wallet_match = re.search(r"Wallet.*?([\d.]+)\s*SOL", message)
        whale_wallet_sol = float(wallet_match.group(1)) if wallet_match else 0

        # 7. Sniper info
        sniper_count_match = re.search(r"Snipers?:\s*(\d+)", message)
        sniper_count = int(sniper_count_match.group(1)) if sniper_count_match else 0

        sniper_percent_match = re.search(r"Snipers?.*?(\d{1,3}(?:\.\d{1,2})?)%", message)
        sniper_percent = float(sniper_percent_match.group(1)) if sniper_percent_match else 0.0

        # 8. Renounced (deteksi kata atau emoji)
        renounced_match = re.search(r"(renounced|🔒)", message, re.IGNORECASE)
        renounced = 'renounced' if renounced_match else ''

        # 9. Token address/symbol (solana token hash)
        token_symbol = "UNKNOWN"

        # A. pump.fun
        pump_match = re.search(r"https://pump.fun/([a-zA-Z0-9]{30,})", message)
        if pump_match:
            token_symbol = pump_match.group(1).strip()

        # B. Soul Sniper
        elif re.search(r"https://t\.me/Soul_Sniper_Bot\?start=\d+_([a-zA-Z0-9]{30,})", message):
            token_symbol = re.search(r"https://t\.me/Soul_Sniper_Bot\?start=\d+_([a-zA-Z0-9]{30,})", message).group(1)

        # C. Dexscreener
        elif re.search(r"https://dexscreener\.com/solana/([a-zA-Z0-9]{30,})", message):
            token_symbol = re.search(r"https://dexscreener\.com/solana/([a-zA-Z0-9]{30,})", message).group(1)

        # D. Geckoterminal via hyperlink (raw_entities)
        elif raw_entities:
            for entity in raw_entities:
                if hasattr(entity, 'url') and entity.url:
                    match = re.search(r'/tokens/([a-zA-Z0-9]{30,})', entity.url)
                    if match:
                        token_symbol = match.group(1)
                        break

        # Final validasi
        if len(token_symbol) < 30:
            print("[Parser] ❗ Token symbol not found or invalid.")
            token_symbol = "UNKNOWN"

        return {
            "token_name": token_name,
            "symbol": token_symbol,
            "marketcap": marketcap,
            "liquidity": liquidity,
            "volume": volume,
            "wallet": whale_wallet_sol,
            "whale_wallet_sol": whale_wallet_sol,
            "age": age_str,
            "age_seconds": age_seconds,
            "renounced": renounced,
            "sniper_count": sniper_count,
            "sniper_percent": sniper_percent
        }

    except Exception as e:
        print(f"[Parser Error] {e}")
        return None
