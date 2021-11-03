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


@client.on("message_create")
async def first_handle(message: models.Message):
    if message.author.bot or not message.content:
        return

    # A Ping command
    if message.content.startswith(".ping"):
        embed = models.Embed.create(description=":ping_pong: Pong from first cog!")
        embed.color = 0xFF123A

        await models.Message.send(message.channel_id or "", embeds=[embed])

@client.on("message_create")
async def second_handle(message: models.Message):
    if message.author.bot or not message.content:
        return

    if message.content.startswith(".pong"):
        embed = models.Embed.create(description=":ping_pong: Ping from second cog!")
        embed.color = 0xFF123A

        await models.Message.send(message.channel_id or "", embeds=[embed])

client.run(os.getenv("DISCORD_TOKEN"))
