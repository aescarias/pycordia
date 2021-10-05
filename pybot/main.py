from pycordia.models.message import Message
import pycordia
import dotenv
import os

dotenv.load_dotenv()

client = pycordia.Client(intents=pycordia.Intents.all())

@client.event
async def on_message_create(message: pycordia.models.Message):
    if message.author.bot:
        return

    if not message.content:
        return
    
    if message.content.startswith(".ping"):
        embed = pycordia.models.Embed.create(title="Pong.", description=":ping_pong: Ping pong!")
        await pycordia.models.Message.send(message.channel_id, embeds=[embed])
    elif message.content.startswith(".servers"):
        guilds = await client.guilds
        
        embed = pycordia.models.Embed.create(title="Guilds I'm in", 
            description="\n".join(guild.name for guild in guilds),
            color=0xFF2A3C
        )
        embed.add_field("Guild Count", str(len(guilds)))
        await pycordia.models.Message.send(message.channel_id, embeds=[embed])

    elif message.content.startswith(".info"):
        embed = pycordia.models.Embed.create(
            title="PyBot",
            description=f"Running on Pycordia v{pycordia.__version__}"
        )
        await pycordia.models.Message.send(message.channel_id, embeds=[embed])

@client.event
async def on_interaction_create(data):
    print(data)

client.run(os.environ.get("DISCORD_TOKEN", ""))