# Pycordia

> ⚠️ **Note!**
> 
> As of now, this package is under early development so functionalities are bound to change drastically.
> 
> We **don't** recommend you currently use Pycordia in a production environment.

A work-in-progress Discord API wrapper for Python with a simple gateway and some common events implemented.

While there's currently no documentation available, use the examples for guidance. If you have any questions, feel free to join our [Discord server](https://discord.gg/h5JhXtGfXQ) to follow the changes we make, as well as receive help and talk with others!

Our examples (and future documentation) assume you're at a level of Python where you can comfortably work with Discord bots.

## :gear: Installation
 
As of now and while this package is in early development, you'll have to install Pycordia from source.
 
Pycordia has been well tested on Python 3.8, however, 3.7 and above are supported.

---

First, clone this repository either through Git or Github.

Next, proceed to run the `setup.py` file as in:
```sh
$ python setup.py sdist     # Should work everywhere
$ python3 setup.py sdist    # Should work on most *nix systems; use on MacOS
$ py -3 setup.py sdist      # Should work on Windows
```

`cd` into the new `dist` directory and run the created `.tar.gz` file.
```sh
$ pip install pycordia-<version>.tar.gz         # Should work everywhere
$ pip3 install pycordia-<version>.tar.gz        # Should work on most *nix systems; use on MacOS
$ python -m pip install pycordia-....tar.gz     # Alternative; should work everywhere
$ python3 -m pip install pycordia-....tar.gz    # Alternative; use on MacOS
$ py -3 -m pip install pycordia-....tar.gz      # Alternative; use on Windows
```

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
    if msg.author.bot or not msg.content:
        return

    if msg.content.startswith(".ping"):
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
- `on_message_update`: `models.Message`
- `on_channel_create`, `on_channel_update`, `on_channel_delete`: `models.Channel`

For all other undocumented events, you'll receive raw JSON data which you'll have to handle yourself.

## :bookmark: Things to do

- Improve currently available models
- Add slash commands
- Add all other event wrappers

## :book: Contribute

Feel free to contribute any bug fixes, new features, or general improvements to the Pycordia project.
