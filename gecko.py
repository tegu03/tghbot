import aiohttp

async def fetch_token_price_by_address(address: str):
    try:
        url = f"https://api.geckoterminal.com/api/v2/networks/solana/tokens/{address}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    price_str = data.get("data", {}).get("attributes", {}).get("price_usd")
                    if price_str:
                        return float(price_str)
                    else:
                        print(f"[Gecko] ❌ Price not found in response.")
                else:
                    print(f"[Gecko] ❌ Failed to fetch price: {response.status}")
    except Exception as e:
        print(f"[Gecko] ⚠️ Exception: {e}")
    return 0
