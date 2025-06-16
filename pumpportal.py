# pumpportal.py

import aiohttp
import asyncio
from config import PUMPPORTAL_BASE_URL, PUMPPORTAL_API_KEY

HEADERS = {
    "Authorization": f"Bearer {PUMPPORTAL_API_KEY}",
    "Accept": "application/json"
}

async def fetch_token_price(token_name: str):
    url = f"{PUMPPORTAL_BASE_URL}/v1/token/price?name={token_name}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=HEADERS, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("price_usd", 0)
                else:
                    print(f"[PumpPortal] ❌ Failed to fetch price for {token_name}: {response.status}")
    except Exception as e:
        print(f"[PumpPortal] ⚠️ Exception during price fetch: {e}")
    return 0


async def fetch_token_price_by_address(address: str):
    url = f"{PUMPPORTAL_BASE_URL}/v1/token/price?address={address}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=HEADERS, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("price_usd", 0)
                else:
                    print(f"[PumpPortal] ❌ Failed to fetch price for {address}: {response.status}")
    except Exception as e:
        print(f"[PumpPortal] ⚠️ Exception during price fetch by address: {e}")
    return 0
