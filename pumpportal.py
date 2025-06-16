import aiohttp
import asyncio

BASE_URL = "https://api.pump.fun/v1"  # Gantilah jika endpoint berbeda

async def get_token_price(token_name):
    url = f"{BASE_URL}/tokens/{token_name}/price"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('price', None)
                else:
                    print(f"[ERROR] Failed to fetch price: {response.status}")
                    return None
    except Exception as e:
        print(f"[EXCEPTION] Error fetching price: {e}")
        return None

# Fungsi tambahan untuk dapatkan info token (marketcap, LP, dll jika tersedia)
async def get_token_info(token_name):
    url = f"{BASE_URL}/tokens/{token_name}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"[ERROR] Token info fetch failed: {response.status}")
                    return None
    except Exception as e:
        print(f"[EXCEPTION] Error fetching token info: {e}")
        return None

# Testing jika ingin jalankan langsung
if __name__ == "__main__":
    async def main():
        token = "BONK"
        price = await get_token_price(token)
        print(f"Price for {token}: {price}")

    asyncio.run(main())
