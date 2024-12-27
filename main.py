import aiohttp
import asyncio

happy = "put your webhook"

new = "vanity.txt"

years = "https://discord.com/api/v10/invites/"

async def check_invites():
    try:
        with open(new, "r") as file:
            invite_codes = [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"❌ Err: '{new}' file not found.")
        return

    if not invite_codes:
        print("⚠️ Vanity list is empty.")
        return

    results = []

    async with aiohttp.ClientSession() as session:
        for code in invite_codes:
            async with session.get(years + code) as response:
                if response.status == 200:
                    data = await response.json()
                    guild_name = data.get("guild", {}).get("name", "Doesnt exist.")
                    channel_name = data.get("channel", {}).get("name", "Doesnt exist.")
                    results.append(f"❌ Vanity is being used: https://discord.gg/{code} | Server: **{guild_name}**, Channel: **{channel_name}**")
                elif response.status == 404:
                    results.append(f"✅ Vanity not used or banned: https://discord.gg/{code}")
                else:
                    results.append(f"⚠️ Err: https://discord.gg/{code} | HTTP Status Code: {response.status}")

    await send_to_webhook(results)

async def send_to_webhook(results):
    if not happy:
        print("❌ Webhook URL doesnt exist.")
        return

    content = "\n".join(results)

    async with aiohttp.ClientSession() as session:
        payload = {"content": content}
        async with session.post(happy, json=payload) as response:
            if response.status != 204:
                print(f"❌ Webhook sending error: HTTP {response.status}")

async def main():
    await check_invites()

if __name__ == "__main__":
    asyncio.run(main())
