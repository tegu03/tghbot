import json
import re

# Parser untuk mengekstrak data token dari pesan teks

def extract_token_info(text):
    try:
        # Token Name
        token_match = re.search(r'\$([A-Za-z0-9&$]+)', text)
        token_name = token_match.group(1) if token_match else 'UNKNOWN'

        # Age (detik)
        age_match = re.search(r'Age: (\d+)([smh])', text)
        if age_match:
            value, unit = int(age_match.group(1)), age_match.group(2)
            if unit == 's': age = value
            elif unit == 'm': age = value * 60
            elif unit == 'h': age = value * 3600
        else:
            age = 0

        # Wallet (SOL)
        wallet_match = re.search(r'Wallet: ([\d\.]+) SOL', text)
        wallet = float(wallet_match.group(1)) if wallet_match else 0

        # Marketcap
        mc_match = re.search(r'MC: \$([\d,\.Kk]+)', text)
        mc = parse_dollar_value(mc_match.group(1)) if mc_match else 0

        # Liquidity
        lp_match = re.search(r'Liq: \$([\d,\.Kk]+)', text)
        lp = parse_dollar_value(lp_match.group(1)) if lp_match else 0

        # Volume 1h
        vol_match = re.search(r'Vol: \$([\d,\.Kk]+)', text)
        volume = parse_dollar_value(vol_match.group(1)) if vol_match else 0

        # Renounced
        renounced = '🔒' in text or 'Renounced' in text

        # Return dictionary
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
    if 'K' in val:
        return float(val.replace('K', '')) * 1000
    elif 'M' in val:
        return float(val.replace('M', '')) * 1000000
    return float(val)
