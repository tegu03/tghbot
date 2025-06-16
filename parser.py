# parser.py

import re
from utils import parse_number

def parse_token_data(message: str) -> dict:
    try:
        data = {
            "token_name": "",
            "marketcap": 0.0,
            "liquidity": 0.0,
            "volume_1h": 0.0,
            "snipers": 0,
            "holders": 0,
            "wallet_value": 0.0,
            "wallet_sol": 0.0,
            "dev_sol": 0.0,
            "bundled": 0.0,
            "airdrops": 0.0,
            "age": "",
            "contract": ""
        }

        # Token name
        lines = message.splitlines()
        if lines:
            data["token_name"] = lines[0].strip().split("New Whale Buy!")[0].strip("🔥🐳")

        # Age
        age_match = re.search(r"Age:\s*([\w\s]+)\s*\|", message)
        if age_match:
            data["age"] = age_match.group(1).strip()

        # Marketcap
        mc_match = re.search(r"MC:\s*\$([\d\.KMB]+)", message)
        if mc_match:
            data["marketcap"] = parse_number(mc_match.group(1))

        # Liquidity
        liq_match = re.search(r"Liq:\s*\$([\d\.KMB]+)", message)
        if liq_match:
            data["liquidity"] = parse_number(liq_match.group(1))

        # Volume
        vol_match = re.search(r"Vol:\s*\$([\d\.KMB]+)\s*\[1h\]", message)
        if vol_match:
            data["volume_1h"] = parse_number(vol_match.group(1))

        # Snipers
        snipers_match = re.search(r"Snipers:\s*(\d+)", message)
        if snipers_match:
            data["snipers"] = int(snipers_match.group(1))

        # Holders
        holders_match = re.search(r"Hodls:\s*(\d+)", message)
        if holders_match:
            data["holders"] = int(holders_match.group(1))

        # Wallet
        wallet_match = re.search(r"Wallet:\s*([\d\.]+)\s*SOL", message)
        if wallet_match:
            data["wallet_sol"] = float(wallet_match.group(1))

        # Wallet value (optional if ada value USD)
        value_match = re.search(r"\$([\d\.KMB]+)", message)
        if value_match:
            try:
                data["wallet_value"] = parse_number(value_match.group(1))
            except:
                pass

        # Dev SOL
        dev_match = re.search(r"Dev:\s*([\d\.]+)\s*SOL", message)
        if dev_match:
            data["dev_sol"] = float(dev_match.group(1))

        # Bundled
        bundled_match = re.search(r"Bundled:\s*([\d\.]+)%", message)
        if bundled_match:
            data["bundled"] = float(bundled_match.group(1))

        # Airdrops
        airdrop_match = re.search(r"Airdrops:\s*([\d\.]+)%", message)
        if airdrop_match:
            data["airdrops"] = float(airdrop_match.group(1))

        # Contract address (optional if tersedia)
        contract_match = re.search(r"Contract: (https?://\S+)", message)
        if contract_match:
            data["contract"] = contract_match.group(1)

        return data
    except Exception as e:
        print(f"[Parser Error] {e}")
        return {}
