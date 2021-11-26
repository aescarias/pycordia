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


@client.event
async def on_message_create(event: models.Message):
    """Listen to message create event"""

    # Don't want to respond to ourselves, or to empty messages!
    if event.author.bot or not event.content:
        return

    # A Ping command
    if event.content.startswith(".ping"):
        embed = models.Embed.create(description=f":ping_pong: Pong with a latency of **{client.ws.latency}ms**!")
        embed.color = 0xFF123A

        await models.Message.send(event.channel_id or "", embeds=[embed])

    # Get information about a user
    elif event.content.startswith(".user"):
        if len(event.content.split()) == 2:
            user = await models.User.from_id(event.content.split()[1])

            if user:
                embed = models.Embed.create(
                    title=user.username + "#" + user.discriminator,
                    description=f"{user.mention}\nID - {user.id}\nBot - {bool(user.bot)}",
                    color=user.accent_color,
                )
            else:
                embed = models.Embed.create(
                    description="Please specify a valid user ID.",
                    color=0xFF123A
                )
            await models.Message.send(event.channel_id or "", embeds=[embed])
        else:
            embed = models.Embed.create(
                description="Please specify a user ID.",
                color=0xFF123A
            )
            await models.Message.send(event.channel_id or "", embeds=[embed])

    # Get server information
    elif event.content.startswith(".servers"):
        guilds = await client.guilds
        newline = "\n"
        guilds = newline.join(
            [
                f"Name - {guild.name}\nId - {guild.id}\nFeatures - {newline.join(guild.features) or None}"
                for guild in guilds
            ]
        )

        await models.Message.send(event.channel_id or "", content=str(guilds))
    # Get information about the bot
    elif event.content.startswith(".botinfo"):
        user = await client.user

        embed = models.Embed.create(
            title=user.username + "#" + user.discriminator,
            description=f"{user.mention}\nID - {user.id}\nBot - {bool(user.bot)}",
            color=user.accent_color,
        )

        await models.Message.send(event.channel_id or "", embeds=[embed])

    elif event.content.startswith(".pin"):
        split = event.content.split()
        if len(split) > 1:
            message_id = split[1]
            msg = await models.Message.from_id(event.channel_id or "", message_id)
            if msg:
                await msg.pin()
            else:
                embed = models.Embed.create(
                    description="Please specify a valid message ID. Make sure you're using this command in the correct channel.",
                    color=0xFF123A
                )
                await models.Message.send(event.channel_id or "", embeds=[embed])
        else:
            embed = models.Embed.create(
                description="Please specify a message ID.",
                color=0xFF123A
            )
            await models.Message.send(event.channel_id or "", embeds=[embed])

client.run(os.getenv("DISCORD_TOKEN"))
