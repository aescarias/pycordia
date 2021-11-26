import aiohttp
import pycordia

import os
import dotenv
import io

from pycordia import models

dotenv.load_dotenv()

client = pycordia.Client(intents=pycordia.Intents.all())

@client.event
async def on_ready(event: pycordia.events.ReadyEvent):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://cdn.discordapp.com/emojis/727592135171244103.png?size=96") as resp:
            img_body = await resp.read()

    await models.Message.send(
        "882843456999927852", 
        content="Hello! Attachment support for `Message.send` works",
        files=[
            pycordia.models.File(filename="smilecat.png", 
                                 fp=io.BytesIO(img_body), 
                                 description="poggers"
            )
        ]
    )



client.run(os.getenv("DISCORD_TOKEN"))