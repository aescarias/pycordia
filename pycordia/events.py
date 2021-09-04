import typing
from .models.guild import Member
from .models.user import User


class ReadyEvent:
    def __init__(self, data: dict):
        """Event called when the client is ready.

        Attributes
            gateway_version: The version used for the WebSockets gateway
            user: The bot using the gateway
            guilds: A list of guild IDs the bot is in
            session_id: The session ID for the WebSockets session
            shard: The number of shards and their ID for this session
            partial_application: An Application object with an ID and flags
        """
        self.gateway_version: int = data["v"]
        self.user: User = User(data["user"])
        self.guilds: typing.List[int] = [int(guild["id"]) for guild in data ["guilds"]]
        self.session_id: str = data["session_id"]
        self.shard: tuple = data.get("shard", ())

        self.partial_application: dict = data["application"]


class MessageDeleteEvent:
    """Event called when message(s) deleted individually or in bulk
        
    Attributes
        message_ids: The IDs of the message
        channel_id: The ID of the channel
        guild_id: The ID of the guild
        bulk: Whether the deletion was performed in bulk
    """     
    def __init__(self, data: dict, bulk: bool):
  
        if bulk:
            self.message_ids = data["ids"]
        else:
            self.message_ids = [data["id"]]

        self.channel_id = data["channel_id"]
        self.guild_id = data.get("guild_id")
        self.bulk = bulk


class TypingStartEvent:
    """Event called when an user starts typing a message"""
    def __init__(self, data: dict):
        """Attributes
            timestamp: The ISO8601 timestamp for the message
            member: The member that started typing
            user_id: The ID of the member
            channel_id: The ID of the channel where event was registered
            guild_id: The ID of the guild where event was registered
        """

        self.timestamp = data["timestamp"]

        self.member = Member(data.get("member", {}))
        
        self.user_id = data["user_id"]
        self.channel_id = data["channel_id"]
        self.guild_id = data["guild_id"]

