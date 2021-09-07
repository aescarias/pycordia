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
        embed = models.Embed.create(description=":ping_pong: Pong!")
        embed.color = 0xFF123A

        await models.Message.create(embeds=[embed]).send(client, event.channel_id)
        print(f"Sent a message - {embed.description}")

    # Get information about the bot
    elif event.content.startswith(".botinfo"):
        user = await client.user

        embed = models.Embed.create(
            title=user.username + "#" + user.discriminator,
            description=f"{user.mention}\nID - {user.user_id}\nBot - {bool(user.bot)}",
            color=user.accent_color,
        )

        await models.Message.create(embeds=[embed]).send(client, event.channel_id)

# Run our bot, providing the tokem
client.run(os.getenv("DISCORD_TOKEN"))
