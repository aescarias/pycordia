import aiohttp
import asyncio
import os
import dotenv

dotenv.load_dotenv()

data =  {
    "name": "blep",
    "type": 1,
    "description": "Send a random adorable animal photo",
    "options": [
        {
            "name": "animal",
            "description": "The type of animal",
            "type": 3,
            "required": True,
            "choices": [
                {
                    "name": "Dog",
                    "value": "animal_dog"
                },
                {
                    "name": "Cat",
                    "value": "animal_cat"
                },
                {
                    "name": "Penguin",
                    "value": "animal_penguin"
                }
            ]
        },
        {
            "name": "only_smol",
            "description": "Whether to show only baby animals",
            "type": 5,
            "required": False
        }
    ]
}

async def main():
    async with aiohttp.ClientSession(headers={"Authorization": f"Bot {os.getenv('DISCORD_TOKEN')}"}) as session:
        async with session.post(f"https://discord.com/api/v9//channels/789638159104868412/messages", json={
            "content": "This is a message with components",
            "components": [
                {
                    "type": 1,
                    "components": [
                    ]
                }
            ]
        }) as data:
            print(await data.json())

    # async with aiohttp.ClientSession() as session:
    #     url = f"https://discord.com/api/v9/applications/{os.getenv('APP_ID')}/commands"
    #     async with session.post(url, headers={"Authorization": f"Bot {os.getenv('DISCORD_TOKEN')}"}, json=data) as resp:
    #         if resp.ok:
    #             print(await resp.json())
    #         else:
    #             print(resp)
    #     async with session.post(url, headers={
    #         "Authorization": f"Bot {os.getenv('DISCORD_TOKEN')}"
    #     }, json=data) as resp:
    #         print(resp)
    #         if resp.ok:
    #             print(await resp.json())
    #         else:
    #             print(resp.status, resp.reason)



asyncio.get_event_loop().run_until_complete(main())