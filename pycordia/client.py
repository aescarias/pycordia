from pycordia import http
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
    def all(cls):
        """All registered intents, including privileged ones"""
        return cls.merge_intents(cls, True)

    @classmethod
    def standard(cls):
        """All non-privileged intents"""
        return cls.merge_intents(cls, False)

    @classmethod
    def merge_intents(cls, intent_list, privileged: bool = False):
        """Convert a list of intents into a number

        Parameters
        ---
            intent_list: A list of intents
            privileged (bool): Whether or not to include privileged \
                intents in the result
        """
        result = 0
        for value in intent_list:
            if not privileged and (value in (
                pycordia.Intents.guild_members, pycordia.Intents.guild_presences)): continue
            result |= value.value
        return result


class Client:
    """
    A WebSockets client for the Discord Gateway API

    Attributes:
        cache_size (int): Maz size of user and message caches
        message_cache (Dict[str, Message]): Client's message cache - a dictionary of string - `pycordia.models.message.Message` mappings
        user_cache (Dict[str, Message]): Client's user cache - a dictionary of string - `pycordia.models.user.User` mappings
    """

    def event(self, fun):
        """A decorator that registers an event"""
        self.register_event(fun.__name__, fun)

        def wrapper():
            fun()

        return wrapper

    def on(self, event_name):
        """A decorator that registers a listener for an event"""
        def factory(fun):
            self.register_listeners(event_name, fun)
            def wrapper():
                fun()
            return wrapper
        return factory

    def register_event(self, event_name: str, callable_: typing.Callable):
        """Register a callable as an event
        
        Args:
            event_name (str): The name of an event (example: `message_create` or `guild_create`)
            callable_ (typing.Callable): A callable 
        """
        if not event_name.startswith("on_"):
            name = f"on_{event_name}"
        else:
            name = event_name

        event = self.events.get(name)

        # If an event is found -- replace it
        if event:
            self.events[name]["event"] = callable_
        # Otherwise -- create a new one with no listeners
        else:
            self.events[name] = {
                "event": callable_,
                "listeners": []
            }
        

    def register_listeners(self, event_name: str, *callables: typing.Callable):
        """Register a set of callables as listeners of an event
        
        Args:
            event_name (str): The name of an event (example: `message_create` or `guild_create`)
            callables: A set of callable objects to call when `event_name` is triggered
        """
        if not event_name.startswith("on_"):
            name = f"on_{event_name}"
        else:
            name = event_name
        
        event = self.events.get(name)

        # If an event is found, and listeners are found -- add to listeners
        if event and "listeners" in event:
            self.events[event]["listeners"].extend(callables)
        else:
            # If there is an event -- replace listeners
            if event:
                self.events[event]["listeners"] = [*callables]
            # Otherwise, create new event with only listeners registered
            else:
                self.events[event] = {
                    "event": None,
                    "listeners": [*callables]
                }
        

    def __init__(self, *, intents: int, cache_size: int = 1000):
        """
        Args:
            intents (int): The intents for the bot to authenticate with. \
                Preferably obtained from `pycordia.Intents`
            cache_size (int, optional): The amount of entries \
                to store in cache at a time. Defaults to 1000.
        """

        # event_name: {
        #   "event_handler": callable,
        #   "listeners": [callable, ...]
        # }
        self.events = {}
        self.intents = intents

        self.cache_size = int(cache_size)
        self.user_cache: typing.Dict[str, models.User] = {}
        self.message_cache: typing.Dict[str, models.Message] = {}

        self.ws = websocket.DiscordWebSocket(self, "placeholder", self.intents)
        self.http = http.HTTPClient("placeholder")

    async def __create_session(self, bot_token):        
        if not bot_token:
            bot_token = ""

        self.ws.bot_token = bot_token
        self.http.bot_token = bot_token
        await self.http.login()        
        await self.ws.start()

    async def call_event_handler(self, event_name: str, event_data):
        func_name = f"on_{event_name.lower()}"
        
        def call_handlers(*args, **kwargs):
            event_data = self.events[func_name]
            if event_data["event"]:
                asyncio.gather(event_data["event"](*args, **kwargs))

            if event_data["listeners"]:
                for listener in event_data["listeners"]:
                    asyncio.gather(listener(*args, **kwargs))
    
        
        # --- Cached methods ---
        if event_name.lower() == "message_create":
            message = models.Message(event_data)

            if len(self.message_cache.keys()) >= self.cache_size:
                first_message = list(self.message_cache.keys())[0]
                del self.message_cache[first_message]

            self.message_cache[message.id] = message

            if func_name in self.events:
                call_handlers(message)
                return
        elif event_name.lower() == "message_update":
            after = models.Message(event_data)
            
            # print(self.message_cache, after.id)
            
            before = self.message_cache.get(after.id, None)

            # Update the message cache
            if len(self.message_cache.keys()) >= self.cache_size:
                first_message = list(self.message_cache.keys())[0]
                del self.message_cache[first_message]
            
            self.message_cache[after.id] = after

            if func_name in self.events:
                call_handlers(before, after)               
                return

        # --- Uncached methods ---
        if func_name in self.events:
            func = self.events[func_name]

            if event_name.lower() == "ready":
                call_handlers(events.ReadyEvent(event_data))

            # ---- User Related Events ----
            elif event_name.lower() == "typing_start":
                call_handlers(events.TypingStartEvent(event_data))

            # ---- Message Related Events ----
            elif event_name.lower() == "message_delete":
                msg = self.message_cache.get(event_data["id"])

                call_handlers(
                    events.MessageDeleteEvent(event_data, False, [msg] if msg else [])
                )
            elif event_name.lower() == "message_delete_bulk":
                ids = event_data.get("ids", [])
                call_handlers(
                    events.MessageDeleteEvent(event_data, True, 
                        list(filter(lambda key: key in ids, self.message_cache))
                ))
            
            # ---- Channel Related Events ----
            elif event_name.lower() in ("channel_create", "channel_update", "channel_delete"):
                call_handlers(models.Channel(event_data))

            # ---- Unimplemented ----
            else:
                call_handlers(event_data)

    async def setup_http(self, bot_token: str):
        """A helper method that setups the client for HTTP use
        
        Parameters:
            bot_token (str): Discord token
        """
        pycordia.models.active_client = self
        
        self.http.bot_token = bot_token
        await self.http.login()

    def run(self, bot_token: str):
        """Log into Discord, and start the event loop.

        Parameters:
            bot_token (str): Discord token
        """
        pycordia.models.active_client = self

        loop = asyncio.get_event_loop()
        task = loop.create_task(self.__create_session(bot_token))

        try:
            loop.run_until_complete(task)
        except KeyboardInterrupt:
            task.cancel()

            if self.ws and self.ws.sock:
                loop.run_until_complete(self.ws.sock.close())

            if self.http and self.http.session:
                loop.run_until_complete(self.http.session.close())

    async def get_channel(self, channel_id: str) -> models.Channel:
        return await models.Channel.from_id(channel_id)

    async def get_user(self, user_id: str, *, use_cache: bool = True) -> models.User:
        return await models.User.from_id(user_id, use_cache)

    async def get_guild(self, guild_id: str, *, with_counts: bool = False) -> models.Guild:
        return await models.Guild.from_id(guild_id, with_counts=with_counts)

    @property
    async def guilds(self) -> typing.List[models.PartialGuild]:
        """List of guilds of which the bot is a member"""

        rs = await self.http.request("GET", "users/@me/guilds")
        return list(map(models.PartialGuild, await rs.json()))

    @property
    async def user(self) -> models.User:
        """Bot's `pycordia.models.user.User` object"""
        rs = await self.http.request("GET", "users/@me")
        return models.User(await rs.json())

    @property
    async def connections(self):
        """Connections for the bot"""
        rs = await self.http.request("GET", "users/@me")
        return list(map(models.Connection, await rs.json()))
