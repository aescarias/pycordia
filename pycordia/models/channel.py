import enum
from datetime import datetime
from typing import Any, Dict, List, Optional

import pycordia
from pycordia import utils


class ChannelType(enum.Enum):
    text = 0
    dm = 1
    voice = 2
    group_dm = 3
    category = 4
    news = 5
    store = 6
    news_thread = 10
    public_thread = 11
    private_thread = 12
    stage_voice = 13


class Channel:
    """
    Channel model to mirror a Discord Channel

    Operations:
        - str(x): Returns the channel name following a `#`
        - x == y: Checks if two channels are the same
    """

    def __init__(self, data: dict):
        self.__client = pycordia.models.active_client

        self.id: str = data["id"]
        self.type = ChannelType(data["type"])
        self.guild_id: Optional[str] = data.get("guild_id")
        self.position: Optional[int] = data.get("position")

        # TODO: Define overwrite model
        self.permission_overwrites: List[Dict] = data.get("permission_overwrites", [])

        self.name: Optional[str] = data.get("name")
        self.topic: Optional[str] = data.get("topic")
        self.nsfw: Optional[bool] = data.get("nsfw")
        self.last_message_id: Optional[str] = data.get("last_message_id")
       
        # -- Voice channel
        self.bitrate: Optional[int] = data.get("bitrate")
        self.user_limit: Optional[int] = data.get("user_limit")
        self.rate_limit_per_user: Optional[int] = data.get("rate_limit_per_user")

        # -- DMs
        self.recipients: list = data.get("recipients", [])
        
        self.icon_hash: Optional[str] = data.get("icon")

        self.owner_id: Optional[str] = data.get("owner_id")
        self.application_id: Optional[str] = data.get("application_id")
        self.parent_id: Optional[str] = data.get("parent_id")

        self.last_pin_timestamp: Optional[datetime] = utils.make_optional(datetime.fromisoformat, data.get("last_pin_timestamp"))
        self.rtc_region: Optional[str] = data.get("rtc_region")
        self.video_quality_mode: Optional[int] = data.get("video_quality_mode")

        self.message_count: int = data.get("message_count", -1)  # -1 if the count was not provided
        self.member_count: int = data.get("member_count", -1)

        # Thread specific stuff
        # TODO: Define models for these types
        self.thread_metadata: Dict[str, Any] = data.get("thread_metadata", {})
        self.thread_member: Dict[str, Any] = data.get("member", {})
        self.thread_default_auto_archive_duration: int = data.get("default_auto_archive_duration", -1)

        self.permissions: Optional[str] = data.get("permissions")

    def __repr__(self):
        return f"<Channel {self.type} id={self.id} name='{self.name}' topic='{self.topic}'>"

    def __str__(self):
        return f"#{self.name}"
    
    def __eq__(self, channel) -> bool:
        return self.guild_id == channel.guild_id and self.id == channel.id

    @property
    def mention(self) -> str:
        """A channel mention"""
        return f"<#{self.id}>"

    @classmethod
    async def from_id(cls, channel_id: str):
        """
        Fetch a Channel object from its ID.

        Args:
            channel_id (str): Channel ID

        Returns: `pycordia.models.channel.Channel`
        """
        if not pycordia.models.active_client:
            raise pycordia.errors.ClientSetupError

        client = pycordia.models.active_client

        rs = await client.http.request("GET", f"channels/{channel_id}")
        return Channel(await rs.json())

    async def get_message(self, message_id: str, use_cache: bool = True) -> 'pycordia.models.Message':
        """ 
        Get a Message object from its ID

        Args:
            message_id (str): The message ID as a string
            use_cache (bool, defaults to True): Whether to prefer the use of cache or not

        Returns: A `pycordia.models.Message` object
        """
        if not self.__client:
            raise pycordia.errors.ClientSetupError

        if use_cache:
            message = self.__client.message_cache.get(message_id)

            if message:
                if message.channel_id == self.id:
                    return message
                else:
                    raise ValueError("Message does not belong to this channel.")
                    
        rs = await self.__client.http.request("GET", f"channels/{self.id}/messages/{message_id}")
        return pycordia.models.Message(await rs.json())

    async def get_messages(self, limit: int = 50, *, 
        before: str = None, around: str = None, after: str = None
    ) -> List['pycordia.models.Message']:
        """ 
        Get the most recent messages, given a limit (by default 50)

        Args:
            limit (int): The amount of recent messages to get, \
                can be between 1 and 100 (by default: 50)
            before (str): Get messages before the message ID, as a string
            around (str): Get messages around the message ID, as a string
            after (str): Get messages after the message ID, as a string

        Returns: A list of `pycordia.models.Message` objects
        """
        if not self.__client:
            raise pycordia.errors.ClientSetupError
        
        param_string = f"?limit={limit}"

        if before: param_string += f"&before={before}"
        if around: param_string += f"&around={around}"
        if after:  param_string += f"&after={after}"
        
        rs = await self.__client.http.request(
            "GET", f"channels/{self.id}/messages{param_string}"
        )
        return list(map(pycordia.models.Message, await rs.json()))

    async def get_pinned_messages(self) -> List['pycordia.models.Message']:
        """ 
        Get all pinned messages in a Discord channel

        Returns: A list of `pycordia.models.Message` objects
        """
        if not self.__client:
            raise pycordia.errors.ClientSetupError
        
        rs = await self.__client.http.request("GET", f"channels/{self.id}/pins/")
        return list(map(pycordia.models.Message, await rs.json()))


class ChannelMention:
    """
    Represents a channel mention i.e. <#channel_id>

    Attributes:
        channel_id (str): ID of the channel
        guild_id (str): ID of the channel's guild
        channel_type (str): Type of the channel
        channel_name (str): Name of channel
    """
    def __init__(self, data: dict):
        self.channel_id: str = data["id"]
        self.guild_id: str = data["guild_id"]
        self.channel_type: str = data["type"]
        self.channel_name: str = data["name"]
    
    async def get_channel(self) -> Channel:
        """
        Fetch the corresponding channel object.

        Returns: `pycordia.models.channel.Channel`
        """
        return await Channel.from_id(self.channel_id)
        