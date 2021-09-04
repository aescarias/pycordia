# Pycordia

A work-in-progress Discord API wrapper for Python with a simple gateway and some common events implemented.

## :gear: Installation

> :warning: Note!
> As of now and while this package is in early development, you'll have to install Pycordia from source.
> We don't recommend you use Pycordia in a production environment, however, feel free to test out any characteristics of the package.

Pycordia has been well tested on version 3.8, however, 3.7 and above are supported.

First, clone this repository either through Git or Github.

Next, proceed to run the `setup.py` file as in:

```sh
$ python3 setup.py sdist
running sdist
running egg_info
```

(if on Windows and have confirmed that `python --version` is greater than 3.7, use `python`)

Run the created `.tar.gz` file in the new `dist` directory created from `setup.py`

```sh
$ cd dist & python3 -m pip install pycordia-....tar.gz
...
```

(do as noted above if you're on Windows, if you can directly run PIP, use it)

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
- `on_message_delete`, `on_message_delete_bulk`: `events.MessageDeleteEvent`

For all other events as of now, you'll receive raw JSON data which you'll have to handle yourself.

## :bookmark: Things to do

- Improve currently available models
- Add slash commands
- Add all other event wrappers

## :book: Contribute

Feel free to contribute any bug fixes, new features, or general improvements to the Pycordia project.
