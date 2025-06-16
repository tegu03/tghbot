# parser.py (diperbarui untuk mendukung parsing contract address + whale + volume + sniper)

import re

def extract_token_info(text):
    try:
        # Token name
        name_match = re.search(r'\$([A-Z0-9]+)', text)
        token_name = name_match.group(1) if name_match else 'UNKNOWN'

        # Contact / contract link
        contract_match = re.search(r'(https://pump\.fun/\w+/[A-Za-z0-9]+)', text)
        contact = contract_match.group(1) if contract_match else 'N/A'

        # Age in minutes/seconds
        age_match = re.search(r'Age:\s*(\d+)m', text)
        age_min = int(age_match.group(1)) if age_match else 0
        age_sec_match = re.search(r'Age:.*?(\d+)s', text)
        age_sec = int(age_sec_match.group(1)) if age_sec_match else 0
        age_total_seconds = age_min * 60 + age_sec

        # Whale Wallet
        whale_match = re.search(r'Wallet:\s*(\d+(\.\d+)?)\s*SOL', text)
        whale = float(whale_match.group(1)) if whale_match else 0

        # Marketcap
        mc_match = re.search(r'MC:\s*\$([\d,.]+)', text)
        marketcap = int(mc_match.group(1).replace(',', '')) if mc_match else 0

        # Liquidity
        liq_match = re.search(r'Liq:\s*\$([\d,.]+)', text)
        liquidity = int(liq_match.group(1).replace(',', '')) if liq_match else 0

        # Volume
        vol_match = re.search(r'Vol:\s*\$([\d,.]+)', text)
        volume = int(vol_match.group(1).replace(',', '')) if vol_match else 0

        # Sniper
        sniper_count = len(re.findall(r'🍤', text))
        sniper_percent_match = re.search(r'Snipers:.*?(\d+(\.\d+)?)%', text)
        sniper_percent = float(sniper_percent_match.group(1)) if sniper_percent_match else 0

        # Renounced / locked
        security_match = re.search(r'Security:\s*(.*?)\n', text)
        renounced = security_match.group(1) if security_match else ''

        return {
            'token_name': token_name,
            'contact': contact,
            'age': age_total_seconds,
            'wallet': whale,
            'mc': marketcap,
            'lp': liquidity,
            'volume': volume,
            'renounced': renounced,
            'sniper_count': sniper_count,
            'sniper_percent': sniper_percent
        }

    except Exception as e:
        print(f"[ERROR] Parsing gagal: {e}")
        return None
