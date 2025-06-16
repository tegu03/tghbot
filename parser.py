# parser.py

import re

def extract_token_info(text):
    try:
        token_name_match = re.search(r"Token: (.+)", text)
        if not token_name_match:
            return None

        token_name = token_name_match.group(1).strip()

        age_match = re.search(r"Age: (\d+)s", text)
        mc_match = re.search(r"MC: \$(\d+[,.]?\d*)", text)
        lp_match = re.search(r"LP: \$(\d+[,.]?\d*)", text)
        vol_match = re.search(r"Vol(?:ume)?: \$(\d+[,.]?\d*)", text)
        renounced_match = re.search(r"Renounced[:]? (.+)", text, re.IGNORECASE)
        sniper_match = re.search(r"Snipers: (\d+) \((\d+)%\)", text)
        whale_match = re.search(r"Whale: (\d+[.]?\d*) SOL", text)
        ca_match = re.search(r"https://pump.fun/([^\s]+)", text)

        age_seconds = int(age_match.group(1)) if age_match else 0
        mc = float(mc_match.group(1).replace(',', '')) if mc_match else 0
        lp = float(lp_match.group(1).replace(',', '')) if lp_match else 0
        vol = float(vol_match.group(1).replace(',', '')) if vol_match else 0
        renounced = renounced_match.group(1).strip() if renounced_match else ''
        sniper_count = int(sniper_match.group(1)) if sniper_match else 0
        sniper_percent = int(sniper_match.group(2)) if sniper_match else 0
        whale_wallet_sol = float(whale_match.group(1)) if whale_match else 0
        ca = ca_match.group(1) if ca_match else ''

        return {
            "token_name": token_name,
            "age_seconds": age_seconds,
            "marketcap": mc,
            "liquidity": lp,
            "volume": vol,
            "renounced": renounced,
            "sniper_count": sniper_count,
            "sniper_percent": sniper_percent,
            "whale_wallet_sol": whale_wallet_sol,
            "ca": ca,
        }
    except Exception as e:
        print(f"[ERROR] Failed to parse token info: {e}")
        return None
