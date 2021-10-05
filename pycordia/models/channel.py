import enum
from pycordia import api
from pycordia.utils import mutually_exclusive
from typing import Dict, List, Union, Any

import aiohttp
import pycordia


class Channel:
    """
    Channel model to mirror a Discord Channel

    Operations:
        - str(x): Returns the channel name following a `#`
        - x == y: Checks if two channels are the same
    """
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

    def __init__(self, data: dict):
        self.__client = pycordia.models.active_client

        self.name: str = data.get("name")
        self.topic: str = data.get("topic")
        self.id: str = data.get("id")
        self.type: Channel.ChannelType = Channel.ChannelType(int(data.get("type", 0)))

        self.nsfw: bool = data.get("nsfw")
        self.guild_id: Union[str, None] = data.get("guild_id")
        self.position: int = data.get("position")

        # TODO: Define overwrite model
        self.permission_overwrites: List[Dict] = data.get("permission_overwrites")

        self.permissions: str = data.get("permissions")

        # Voice channel attributes
        self.bitrate: Union[int, None] = data.get("bitrate")
        self.user_limit: Union[int, None] = data.get("user_limit")
        self.rtc_region: Union[str, None] = data.get("rtc_region")

        self.slowmode_count: Union[int, None] = data.get("rate_limit_per_user")
        self.recipients: List = data.get("recipients")
        self.icon: Union[str, None] = data.get("icon")

        self.owner_id: Union[str, None] = data.get("owner_id")
        self.application_id: Union[str, None] = data.get("application_id")
        self.parent_id: Union[str, None] = data.get("parent_id")

        self.last_pinned_at: str = data.get("last_pin_timestamp")

        self.message_count: int = data.get("message_count", -1)  # -1 if the count was not provided
        self.member_count: int = data.get("member_count", -1)

        # Thread specific stuff
        # TODO: Define models for these types
        self.thread_metadata: Dict[str, Any] = data.get("thread_metadata", {})
        self.thread_member: Dict[str, Any] = data.get("member", {})
        self.thread_default_auto_archive_duration: int = data.get("default_auto_archive_duration", -1)

    def __repr__(self):
        return f"#{self.name}"
    
    def __eq__(self, channel) -> bool:
        return self.guild_id == channel.guild_id and self.id == channel.id

    @property
    def mention(self) -> str:
        """
        Mention a channel

        Returns: str
        """
        return f"<#{self.id}>"

    @classmethod
    async def from_id(cls, channel_id: str):
        """
        Fetch a channel object from its ID.

        Args:
            channel_id (str): Channel's ID

        Returns: `pycordia.models.channel.Channel`
        """
        return Channel(await api.request("GET", f"channels/{channel_id}"))

    # TODO: Make this method support cache
    async def get_message(self, message_id: str) -> 'pycordia.models.Message':
        """ 
        Get message by ID

        Args:
            message_id (str): The message ID as a string

        Raises: `Exception` if no initialized client is found
        Returns: A `pycordia.models.Message` object
        """
        return pycordia.models.Message(
            await api.request("GET", f"channels/{self.id}/mesages/{message_id}")
        )


    @mutually_exclusive("before", "around", "after")
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

        Raises: `Exception` if no initialized client is found
        Returns: A list of `pycordia.models.Message` objects
        """
        inf: Dict[str, 'int | str'] = {
            "limit": limit,
        }

        if before: inf["before"] = before
        if around: inf["around"] = around
        if after: inf["after"] = after
        
        rs = await api.request("GET", f"channels/{self.id}/messages", json_data=inf)
        return list(map(pycordia.models.Message, rs))

    async def get_pinned_messages(self) -> List['pycordia.models.Message']:
        """ 
        Get the most recent messages, given a limit (by default 50)

        Raises: `Exception` if no initialized client is found
        Returns: A list of `pycordia.models.Message` objects
        """
        rs = await api.request("GET", f"channels/{self.id}/pins/")
        return list(map(pycordia.models.Message, rs))


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
        """
        Args:
            data (dict): Dictionary containing raw data
        """
        self.channel_id: Union[str, None] = data.get("id")
        self.guild_id: Union[str, None] = data.get("guild_id")
        self.channel_type: Union[str, None] = data.get("type")
        self.channel_name: Union[str, None] = data.get("name")

    async def get_channel(self) -> Channel:
        """
        Fetch the corresponding channel object.

        Returns: `pycordia.models.channel.Channel`
        """
        return await Channel.from_id(self.channel_id)
        