# dexscreener.py

import aiohttp

async def fetch_token_price_by_address(address: str):
    url = f"https://api.dexscreener.com/latest/dex/pairs/solana/{address}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    pair_data = data.get('pair')
                    if pair_data and 'priceUsd' in pair_data:
                        return float(pair_data['priceUsd'])
                    else:
                        print(f"[Dexscreener] ⚠️ Pair not found for {address}")
                else:
                    print(f"[Dexscreener] ❌ HTTP {response.status}")
    except Exception as e:
        print(f"[Dexscreener] ⚠️ Exception: {e}")
    return 0
