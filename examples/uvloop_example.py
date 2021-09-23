import asyncio

# A simple example of using uvloop to speed up our bot
try:
    import uvloop
except ImportError:
    print("Using default asyncio event loop")
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    print("Using uvloop's event loop")

from pycordia import events, models
import pycordia
import dotenv
import os

dotenv.load_dotenv()
client = pycordia.Client(intents=pycordia.Intents.all())


@client.event
async def on_ready(event: events.ReadyEvent):
    print(f"{event.user} ready to do stuff!", client.intents)


@client.event
async def on_message_create(msg: models.Message):
    if msg.author.bot or not msg.content:
        return

    if msg.content == ".info":
        content = "Using default asyncio event loop. Very very slow :("

        if "uvloop" in str(asyncio.get_event_loop()):
            content = "Using uvloop's event loop!\nSpeed += 100!"

        await models.Message.create(
            client,
            content=content
        ).send(msg.channel_id)

client.run(os.getenv("DISCORD_TOKEN"))
