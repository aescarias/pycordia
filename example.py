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
    if event.author.bot:
        return

    if event.content and (".ping" in event.content):
        embed1 = models.Embed.create(description=":ping_pong: Pong!")
        embed1.color = 0xFF123A

        embed2 = models.Embed.create(description=":gear: Doing stuff!")
        embed2.color = 0x1FA2E8

        await models.Message.create(embeds=[embed1, embed2]).send(client, event.channel_id)
        print("Sent it?")

client.run(os.getenv("DISCORD_TOKEN"))