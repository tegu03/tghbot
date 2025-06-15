import re

def extract_token_info(text):
    try:
        # Token Name
        token_match = re.search(r'\$([A-Za-z0-9&$]+)', text)
        token_name = token_match.group(1) if token_match else 'UNKNOWN'

        # Age (detik)
        age_match = re.search(r'Age: (\d+)([smh])', text, re.IGNORECASE)
        if age_match:
            value, unit = int(age_match.group(1)), age_match.group(2).lower()
            if unit == 's':
                age = value
            elif unit == 'm':
                age = value * 60
            elif unit == 'h':
                age = value * 3600
        else:
            age = 0

        # Wallet (SOL)
        wallet_match = re.search(r'Wallet:\s*([\d\.]+)\s*SOL', text)
        wallet = float(wallet_match.group(1)) if wallet_match else 0

        # Marketcap
        mc_match = re.search(r'MC:\s*\$([\d,\.KkMm]+)', text)
        mc = parse_dollar_value(mc_match.group(1)) if mc_match else 0

        # Liquidity
        lp_match = re.search(r'Liq:\s*\$([\d,\.KkMm]+)', text)
        lp = parse_dollar_value(lp_match.group(1)) if lp_match else 0

        # Volume
        vol_match = re.search(r'Vol:\s*\$([\d,\.KkMm]+)', text)
        volume = parse_dollar_value(vol_match.group(1)) if vol_match else 0

        # Renounced
        renounced = '🔒' in text or 'Renounced' in text

        return {
            'token_name': token_name,
            'age': age,
            'wallet': wallet,
            'mc': mc,
            'lp': lp,
            'volume': volume,
            'renounced': renounced
        }
    except Exception as e:
        print(f"[ERROR] Parsing gagal: {e}")
        return None

def parse_dollar_value(val):
    val = val.replace(",", "").replace("$", "").strip().upper()
    multiplier = 1
    if 'K' in val:
        multiplier = 1000
        val = val.replace('K', '')
    elif 'M' in val:
        multiplier = 1000000
        val = val.replace('M', '')
    return float(val) * multiplier
