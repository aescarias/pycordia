from typing import Dict, List, Union, Any

import aiohttp

import pycordia
from . import User


class Channel:
    def __init__(self, data: dict):
        self.name: str = data.get("name")
        self.topic: str = data.get("topic")
        self.id: str = data.get("id")
        self.type: int = data.get("type")

        self.nsfw: bool = data.get("nsfw")
        self.guild_id: Union[str, None] = data.get("guild_id")
        self.postion: int = data.get("position")

        # TODO: Define overwrite model
        self.permission_overwrites: List[Dict] = data.get("permission_overwrites")

        self.permissions: str = data.get("permissions")

        # Voice channel attributes
        self.bitrate: Union[int, None] = data.get("bitrate")
        self.user_limit: Union[int, None] = data.get("user_limit")
        self.rtc_region: Union[str, None] = data.get("rtc_region")

        self.slowmode_count: Union[int, None] = data.get("rate_limit_per_user")
        self.recipients: List[User] = data.get("recipients")
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

    @property
    def mention(self):
        return f"<#{self.id}>"

    @classmethod
    async def from_id(cls, client, channel_id: str):
        """Get a channel object given the id"""

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{pycordia.api_url}/channels/{channel_id}",
                headers={
                    "Authorization": f"Bot {client._Client__bot_token}"
                }
            ) as resp:

                if not resp.ok:
                    return

                return Channel(await resp.json())

    # TODO: All methods other than get_from_id() :)


class ChannelMention:
    def __init__(self, data: dict):
        self.channel_id: Union[str, None] = data.get("id")
        self.guild_id: Union[str, None] = data.get("guild_id")
        self.channel_type: Union[str, None] = data.get("type")
        self.channel_name: Union[str, None] = data.get("name")

    def __repr__(self):
        return f"<pycordia.models.ChannelMention - id={self.channel_id} name={self.channel_name}>"

    async def get_channel(self, client):
        return await Channel.from_id(client, self.channel_id)
