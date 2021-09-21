import enum
from typing import Dict, List, Union, Any

import aiohttp

import pycordia
from pycordia import models


class Channel:
    """
    Channel model to mirror a Discord Channel

    ---

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

    def __init__(self, client, data: dict):
        self.__client = client

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
    async def from_id(cls, client, channel_id: str):
        """
        Fetch a channel object from it's ID.

        Args:
            client (pycordia.client.Client): Object's Client instance
            channel_id (str): Channel's ID

        Returns: `pycordia.models.channel.Channel`

        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{pycordia.api_url}/channels/{channel_id}",
                headers={
                    "Authorization": f"Bot {client._Client__bot_token}"
                }
            ) as resp:

                if not resp.ok:
                    return

                return Channel(client, await resp.json())

    # TODO: Make this method support cache
    async def query_message(self, message_id: str):
        """
        Query a message from a channel

        Args:
            message_id (str): ID of message to fetch

        Returns: `pycordia.models.message.Message`
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{pycordia.api_url}/channels/{self.id}/messages/{message_id}",
                headers={
                    "Authorization": f"Bot {self.__client._Client__bot_token}"
                }
            ) as resp:
                if not resp.ok:
                    return

                return models.Message(self.__client, await resp.json())


class ChannelMention:
    """
    Represents a channel mention i.e. <#channel_id>

    ---

    Attributes:
        channel_id (str): ID of the channel
        guild_id (str): ID of the channel's guild
        channel_type (str): Type of the channel
        channel_name (str): Name of channel
    """
    def __init__(self, client, data: dict):
        """
        Args:
            client (pycordia.client.Client): Object's Client instance
            data (dict): Dictionary containing raw data
        """
        self.__client = client

        self.channel_id: Union[str, None] = data.get("id")
        self.guild_id: Union[str, None] = data.get("guild_id")
        self.channel_type: Union[str, None] = data.get("type")
        self.channel_name: Union[str, None] = data.get("name")

    async def get_channel(self) -> Channel:
        """
        Fetch the corresponding channel object.

        Returns: `pycordia.models.channel.Channel`
        """
        return await Channel.from_id(self.__client, self.channel_id)
