# Pycordia v0.1.0 - The Discord bot framework
# Developed by Angel Carias and it's contributors. 2021.

# client.py
#   Handles bot creation


import asyncio
import aiohttp
import enum

from . import events, models, websocket

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
        """Enables all registered intents, including privileged ones"""
        return cls.merge_intents(cls)
    
    @classmethod
    def merge_intents(cls, intent_list):
        """Convert a list of intents into a number

        ---        
        Parameters:
            intent_list: A list of intents
        """
        result = 0
        for value in intent_list:
            result |= value.value
        return result

class Client:
    """A WebSockets client for the Discord Gateway API"""

    def event(self, fun):
        self.events[fun.__name__] = fun        
        def wrapper():
            fun()
        return wrapper    

    def __init__(self, intents):
        self.events = {}
        self.intents = intents

    async def __create_ws(self, bot_token):
        self.ws = websocket.DiscordWebSocket(self, bot_token, self.intents)
        await self.ws.listen()
        
    async def call_event_handler(self, event_name: str, event_data):
        func_name = f"on_{event_name.lower()}"

        print(event_name)
        if func_name in self.events:
            func = self.events[func_name]

            if event_name.lower() == "ready":
                await func( events.ReadyEvent(event_data) )
            elif event_name.lower() == "typing_start":
                await func( events.TypingStartEvent(event_data) )
            elif event_name.lower() == "message_create":
                await func( models.Message(event_data) )
            elif event_name.lower() in ("message_delete", "message_delete_bulk"):
                await func(
                    events.MessageDeleteEvent(
                        event_data, event_name.lower() == "message_delete_bulk"
                    ) 
                )
            else:
                await func( event_data )
            

    def run(self, bot_token):
        asyncio.get_event_loop().run_until_complete(self.__create_ws(bot_token))


