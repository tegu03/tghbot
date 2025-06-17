# dexscreener.py

import aiohttp

async def fetch_token_price_by_address(address: str):
    url = f"https://api.dexscreener.com/latest/dex/pairs/solana/{address}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    price = float(data['pair']['priceUsd'])
                    return price
                else:
                    print(f"[Dexscreener] ❌ Failed to fetch price for {address}: {response.status}")
    except Exception as e:
        print(f"[Dexscreener] ⚠️ Exception: {e}")
    return 0
