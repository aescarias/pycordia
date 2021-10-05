import asyncio
from pycordia import events, models
import pycordia
import dotenv
import os

dotenv.load_dotenv()
client = pycordia.Client(intents=pycordia.Intents.all())


@client.event
async def on_ready(event: events.ReadyEvent):
    """The bot is up and running! Yippee!"""
    print(f"{event.user} ready to do stuff!", client.intents)



async def first_handle(message: models.Message):
    if message.author.bot or not message.content:
        return

    # A Ping command
    if message.content.startswith(".ping"):
        embed = models.Embed.create(description=":ping_pong: Pong from first cog!")
        embed.color = 0xFF123A

        await models.Message.send(message.channel_id or "", embeds=[embed])


async def second_handle(message: models.Message):
    if message.author.bot or not message.content:
        return

    if message.content.startswith(".pong"):
        embed = models.Embed.create(description=":ping_pong: Ping from second cog!")
        embed.color = 0xFF123A

        await models.Message.send(message.channel_id or "", embeds=[embed])

client.register_events("message_create", first_handle, second_handle)
client.run(os.getenv("DISCORD_TOKEN"))
