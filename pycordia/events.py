import typing
from datetime import datetime

from .models import Member, User, Message
from . import utils


class ReadyEvent:
    """
    Event called when the client is ready.

    Attributes:
        gateway_version (int): The version used for the WebSockets gateway
        user (User): The bot using the gateway
        guilds (typing.List[int]): A list of guild IDs the bot is in
        session_id (str): The session ID for the WebSockets session
        shard (tuple): The number of shards and their ID for this session
        partial_application (dict): An Application object with an ID and flags
    """
    def __init__(self, data: dict):
        self.gateway_version: int = data["v"]
        self.user: User = User(data["user"])
        self.guilds: typing.List[int] = [int(guild["id"]) for guild in data ["guilds"]]
        self.session_id: str = data["session_id"]

        # NOTE: unimplemented
        self.shard: tuple = data.get("shard", ())
        self.partial_application: dict = data["application"]


class MessageDeleteEvent:
    """Event called when message(s) deleted individually or in bulk
        
    Attributes:
        message_ids: The IDs of the message
        channel_id: The ID of the channel
        guild_id: The ID of the guild
        bulk: Whether the deletion was performed in bulk
        cached_message: The message, if it was cached by Pycordia
    """     
    def __init__(self, data: dict, bulk: bool, messages):
  
        if bulk:
            self.message_ids = data["ids"]
        else:
            self.message_ids = [data["id"]]

        self.cached_messages: typing.List[Message] = messages
        self.channel_id = data["channel_id"]
        self.guild_id = data.get("guild_id")
        self.bulk = bulk


class TypingStartEvent:
    """Event called when an user starts typing a message

    Attributes:
        timestamp: The timestamp for the message as a datetime object
        member: The member that started typing
        user_id: The ID of the member
        channel_id: The ID of the channel where event was registered
        guild_id: The ID of the guild where event was registered
    """

    def __init__(self, data: dict):
        self.timestamp = datetime.fromtimestamp(data["timestamp"])
        self.member = utils.make_optional(Member, data.get("member"))

        self.user_id = data["user_id"]
        self.channel_id = data["channel_id"]
        self.guild_id = data["guild_id"]

