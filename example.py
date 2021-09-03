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
async def on_message_create(event: models.Message):
    if event.author.bot or not event.content:
        return

    if event.content.startswith(".ping"):
        embed = models.Embed.create(description=":ping_pong: Pong!")
        embed.color = 0xFF123A

        await models.Message.create(embeds=[embed]).send(client, event.channel_id)
        print(f"Sent a message - {embed.description}")

    elif event.content.startswith(".user"):
        user = await models.User.user_from_id(client, event.content.split()[1])

        embed = models.Embed.create(
            title=user.username + "#" + user.discriminator,
            description=f"{user.mention}\nID - {user.user_id}\nBot - {bool(user.bot)}",
            color=user.accent_color,
        )

        await models.Message.create(embeds=[embed]).send(client, event.channel_id)

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

    elif event.content.startswith(".botinfo"):

        user = await client.user

        embed = models.Embed.create(
            title=user.username + "#" + user.discriminator,
            description=f"{user.mention}\nID - {user.user_id}\nBot - {bool(user.bot)}",
            color=user.accent_color,
        )

        await models.Message.create(embeds=[embed]).send(client, event.channel_id)


client.run(os.getenv("DISCORD_TOKEN"))
