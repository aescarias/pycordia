# Pycordia

A work-in-progress Discord API wrapper for Python with a simple gateway and some common events implemented.

## :ping_pong: Example of a simple Ping-Pong Bot

```py
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
    if msg.author.bot:
        return

    if msg.content and (".ping" in msg.content):
        embed = models.Embed.create(description=":ping_pong: Pong!")
        embed.color = 0xFF123A

        await models.Message.create(embeds=[embed]).send(client, msg.channel_id)

client.run(os.getenv("DISCORD_TOKEN"))
```

## Events

- `on_ready`: `events.ReadyEvent`
- `on_message_create`: `models.Message`
- `on_typing_start`: `events.TypingStartEvent`

For all other events as of now, you'll receive raw JSON data which you'll have to handle yourself.

## Things to do

- Improve currently available models
- Add slash commands
- Add all other event wrappers

## Contribute

Feel free to contribute any bug fixes, new features, or general improvements to the Pycordia project.
