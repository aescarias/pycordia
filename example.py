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
async def on_message_update(before: models.Message, after: models.Message):
    """Log edited messages, for moderation purposes"""
    await models.Message.create(
        content=f"Edited Message!\nBefore: {before.content}\nAfter: {after.content}"
    ).send(client, before.channel_id)


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

    # Get information about a user
    elif event.content.startswith(".user"):
        if len(event.content.split()) == 2:                
            user = await models.User.user_from_id(client, event.content.split()[1])

            if user:
                embed = models.Embed.create(
                    title=user.username + "#" + user.discriminator,
                    description=f"{user.mention}\nID - {user.user_id}\nBot - {bool(user.bot)}",
                    color=user.accent_color,
                )
            else:
                embed = models.Embed.create(
                    description="Please specify a valid user ID.",
                    color=0xFF123A
                )               
            await models.Message.create(embeds=[embed]).send(client, event.channel_id)
        else:
            embed = models.Embed.create(
                description="Please specify a user ID.",
                color=0xFF123A
            )
            await models.Message.create(embeds=[embed]).send(client, event.channel_id)

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

        await models.Message.create(content=str(guilds)).send(client, event.channel_id)

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
