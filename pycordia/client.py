# Pycordia v0.1.1 - The Discord bot framework
# Developed by Angel Carias and it's contributors. 2021.

# client.py
#   Handles bot creation


import aiohttp
import asyncio
import enum

import typing

from . import events, models, websocket
import pycordia


class Intents(enum.Enum):
    guilds = 1 << 0
    guild_members = 1 << 1
    guild_bans = 1 << 2
    guild_emojis_and_stickers = 1 << 3
    guild_integrations = 1 << 4
    guild_webhooks = 1 << 5
    guild_invites = 1 << 6
    guild_voice_states = 1 << 7
    guild_presences = 1 << 8
    guild_messages = 1 << 9
    guild_message_reactions = 1 << 10
    guild_message_typing = 1 << 11
    direct_messages = 1 << 12
    direct_message_reactions = 1 << 13
    direct_message_typing = 1 << 14

    @classmethod
    def all(cls) -> int:
        """Enables all registered intents, including privileged ones"""
        return cls.merge_intents(cls)
    
    @classmethod
    def merge_intents(cls, intent_list) -> int:
        """Convert a list of intents into a number

        ---        
        Args:
            intent_list: A list of intents
        """
        result = 0
        for value in intent_list:
            result |= value.value
        return result


class Client:
    """
    A WebSockets client for the Discord Gateway API

    ---

    Attributes:
        cache_size (int): Maz size of user and message caches
        message_cache (Dict[str, Message]): Client's message cache - a dictionary of string - `pycordia.models.message.Message` mappings
        user_cache (Dict[str, Message]): Client's user cache - a dictionary of string - `pycordia.models.user.User` mappings
    """

    def event(self, fun):
        self.events[fun.__name__] = fun

        def wrapper():
            fun()

        return wrapper

    def __init__(self, intents, cache_size: int = 1000):
        self.events = {}
        self.__bot_token: str = ""
        self.intents = intents

        self.cache_size = int(cache_size)
        self.user_cache: typing.Dict[str, models.User] = {}
        self.message_cache: typing.Dict[str, models.Message] = {}

    async def __create_ws(self, bot_token):        
        self.ws = websocket.DiscordWebSocket(self, bot_token, self.intents)
        await self.ws.listen()

    async def call_event_handler(self, event_name: str, event_data):
        func_name = f"on_{event_name.lower()}"
        
        print(event_name)
        # --- Cached methods ---
        if event_name.lower() == "message_create":
            message = models.Message(self, event_data)

            if len(self.message_cache.keys()) >= self.cache_size:
                first_message = list(self.message_cache.keys())[0]
                del self.message_cache[first_message]

            self.message_cache[message.message_id] = message

            if func_name in self.events:
                asyncio.gather(self.events[func_name](message))                
                return
        elif event_name.lower() == "message_update":

            after = models.Message(self, event_data)
            
            print(self.message_cache, after.message_id)
            
            before = self.message_cache.get(after.message_id, None)

            # Update the message cache
            if len(self.message_cache.keys()) >= self.cache_size:
                first_message = list(self.message_cache.keys())[0]
                del self.message_cache[first_message]
            
            self.message_cache[after.message_id] = after

            if func_name in self.events:
                asyncio.gather(self.events[func_name](before, after))                
                return

        # --- Uncached methods ---
        if func_name in self.events:
            func = self.events[func_name]

            if event_name.lower() == "ready":
                asyncio.gather(func(events.ReadyEvent(event_data)))

            # ---- User Related Events ----
            elif event_name.lower() == "typing_start":
                asyncio.gather(func(events.TypingStartEvent(event_data)))

            # ---- Message Related Events ----
            elif event_name.lower() == "message_delete":
                asyncio.gather(func(
                    events.MessageDeleteEvent(event_data, False, [self.message_cache[event_data["id"]]])
                ))
            elif event_name.lower() == "message_delete_bulk":
                ids = event_data.get("ids", [])
                asyncio.gather(func(
                    events.MessageDeleteEvent(event_data, True, 
                        list(filter(lambda key: key in ids, self.message_cache))
                )))
            
            # ---- Channel Related Events ----
            elif event_name.lower() in ("channel_create", "channel_update", "channel_delete"):
                asyncio.gather(func(models.Channel(self, event_data)))

            # ---- Unimplemented ----
            else:
                asyncio.gather(func(event_data))

    def run(self, bot_token: str):
        """Log into discord, and start the event loop

        ---        
        Parameters:
            bot_token (str): Discord token
        """
        self.__bot_token = bot_token

        loop = asyncio.get_event_loop()
        task = loop.create_task(self.__create_ws(bot_token))

        try:
            loop.run_until_complete(task)
        except KeyboardInterrupt:
            task.cancel()

            if self.ws.sock:
                loop.run_until_complete(self.ws.sock.close())

    @property
    async def guilds(self) -> typing.List[models.PartialGuild]:
        """List of guilds of which the bot is a member"""

        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"{pycordia.api_url}/users/@me/guilds",
                    headers={
                        "Authorization": f"Bot {self.__bot_token}"
                    }
            ) as resp:

                if not resp.ok:
                    content = await resp.text()
                    raise Exception(content)

                guilds = await resp.json()
                guilds = list(map(models.PartialGuild, guilds))

                return guilds

    @property
    async def user(self) -> models.User:
        """Bot's `pycordia.models.user.User` object"""

        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"{pycordia.api_url}/users/@me",
                    headers={
                        "Authorization": f"Bot {self.__bot_token}"
                    }
            ) as resp:

                if not resp.ok:
                    content = await resp.text()
                    raise Exception(content)

                return models.User(await resp.json())

    # TODO: Modify current user
    # TODO: Create DM
    # TODO: Leave Guild
    # TODO: Get User Connections
