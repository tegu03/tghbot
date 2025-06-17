# birdeye.py
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()
BIRDEYE_API_KEY = os.getenv("BIRDEYE_API_KEY")

HEADERS = {
    "X-API-KEY": BIRDEYE_API_KEY
}

async def fetch_token_price_by_address(address: str):
    url = f"https://public-api.birdeye.so/public/price?address={address}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=HEADERS) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("data", {}).get("value", 0)
                else:
                    print(f"[Birdeye] ❌ Failed to fetch price: {response.status}")
    except Exception as e:
        print(f"[Birdeye] ⚠️ Exception: {e}")
    return 0
