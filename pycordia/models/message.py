from typing import List, Union
import typing
import aiohttp
import enum
from . import embed
from .user import User
from .guild import Member, Role
from .channel import ChannelMention
from pycordia import models

# class TextChannel:
#     pass

# class GuildMember:
#     pass


class MessageActivity:
    """
    Message Activity class

    Attributes:
        activity_type (`pycordia.models.message.MessageActivity.ActivityTypes`): Type of activity
        party_id (str): ID of the party
    """

    class ActivityTypes(enum.Enum):
        join = 1
        spectate = 2
        listen = 3
        join_request = 5

    def __init__(self, data: dict):
        Activity = MessageActivity.ActivityTypes
        self.activity_type = (
            None if (data.get("type") is None) else Activity(data.get("type"))
        )

        self.party_id: Union[str, None] = data.get("party_id")

    def __repr__(self):
        return f"<pycordia.models.MessageActivity - id={self.party_id} activity={self.activity_type}>"


class Application:
    """Discord application model."""
    def __init__(self, data: dict):
        self.app_id: Union[str, None] = data.get("id")
        self.name: Union[str, None] = data.get("name")
        self.icon: Union[str, None] = data.get("icon")
        self.description: Union[str, None] = data.get("description")

        self.rpc_origins: list = data.get("rpc_origins", [])
        self.bot_public: Union[bool, None] = data.get("bot_public")
        self.bot_require_code_grant: Union[bool, None] = data.get("bot_require")

        self.terms_of_service_url: Union[str, None] = data.get("terms_of_service_url")
        self.privacy_policy_url: Union[str, None] = data.get("privacy_policy_url")
        self.owner: User = User(data.get("owner", {}))

        self.cover_image_hash: Union[str, None] = data.get("cover_image")
        self.flags: Union[int, None] = data.get("flags")

    def __repr__(self):
        return f"<pycordia.models.Application - id={self.app_id} name={self.name}>"


class RoleTags:
    def __init__(self, data: dict):
        self.bot_id = data.get("bot_id")
        self.integration_id = data.get("integration_id")
        self.premium_subscriber = data.get("premium_subscriber")

    def __repr__(self):
        return f"<pycordia.models.RoleTags - id={self.bot_id}>"


class Reaction:
    """Reaction model, to represent reactions on a message."""
    def __init__(self, data: dict):
        self.count: Union[int, None] = data.get("count")
        self.was_me: Union[bool, None] = data.get("me")
        self.emoji: Emoji = Emoji(data.get("emoji", {}))

    def __repr__(self):
        return (
            f"<pycordia.models.Reaction - emoji={self.emoji.name} count={self.count}>"
        )


class Emoji:
    """Emoji model, to represent server specific emojis."""
    def __init__(self, data: dict):
        self.emoji_id = data.get("id")
        self.name = data.get("name")
        self.roles = [Role(role) for role in data.get("roles", [])]
        self.user = User(data.get("user", {}))
        self.requires_colons = data.get("require_colons")
        self.managed = data.get("managed")
        self.animated = data.get("animated")
        self.available = data.get("available")

    def __repr__(self):
        return f"<pycordia.models.Emoji - id={self.emoji_id} name={self.name}>"


class StickerItem:
    """Sticker model, to represent discord stickers"""
    def __init__(self, data: dict):
        self.sticker_id = data.get("id")
        self.name = data.get("name")
        self.format_type = data.get("type")

    def __repr__(self):
        return f"<pycordia.models.StickerItem - id={self.sticker_id} name={self.name}>"


class Attachment:
    """
    An attachment for a message

    Attributes:
        attachment_id (int): The ID of the attachment
        filename (str): The attachment's filename
        content_type (str): The content type
        size (int): File size
        url (str): URL to the file
        proxy_url (str): Alternate URL to the file
        height (int): Height of attachment (only applies to images)
        width (int): Width of the attachment (only applies to images)
    """
    def __init__(self, data: dict):
        self.attachment_id: Union[str, None] = data.get("id")
        self.filename: Union[str, None] = data.get("filename")
        self.content_type: Union[str, None] = data.get("content_type")
        self.size: Union[int, None] = data.get("size")
        self.url: Union[str, None] = data.get("url")
        self.proxy_url: Union[str, None] = data.get("proxy_url")
        self.height: Union[int, None] = data.get("height")
        self.width: Union[int, None] = data.get("width")

    def to_dict(self):
        """
        Return raw dictionary of object
        Returns: dict
        """
        return {
            "id": self.attachment_id,
            "filename": self.filename,
            "content_type": self.content_type,
            "size": self.size,
            "url": self.url,
            "proxy_url": self.proxy_url,
            "height": self.height,
            "width": self.width,
        }


class Interaction:
    """
    Interaction model - represents discord interactions.

    Attributes:
        interaction_id (str): ID of the discord interaction
        interaction_type (str): Type of the interaction (button, slash command, etc)
        name (str): Name of the interaction
        user (`pycordia.models.user.User`): Interaction's user
    """
    def __init__(self, data: dict):
        self.interaction_id = data.get("id")
        self.interaction_type = data.get("type")
        self.name = data.get("name")
        self.user = User(data.get("user", {}))


class MessageReference:
    def __init__(self, client, ref_data: dict, msg_data: dict):
        self.__client = client
        self.__msg_data = msg_data

        if ref_data:
            self.message_id: Union[str, None] = ref_data.get("message_id")
            self.channel_id: Union[str, None] = ref_data.get("channel_id")
            self.guild_id: Union[str, None] = ref_data.get("guild_id")
            self.fail_if_not_exists: Union[bool, None] = ref_data.get(
                "fail_if_not_exists"
            )
        else:
            self.message_id = (
                self.channel_id
            ) = self.guild_id = self.fail_if_not_exists = None

    @property
    def message(self):
        """Fetch the referenced message"""
        return Message(self.__client, self.__msg_data or {})

    def to_dict(self):
        return {
            "message_id": self.message_id,
            "channel_id": self.channel_id,
            "guild_id": self.guild_id,
            "fail_if_not_exists": self.fail_if_not_exists,
        }
    
    def __eq__(self, other) -> bool:
        return self.message_id == other.message_id


class Message:
    """Message model - represents a message sent in discord"""
    def __init__(self, client, data: dict):
        self.__data = data
        self.__client = client

        self.message_id: Union[str, None] = data.get("id")
        self.channel_id: Union[str, None] = data.get("channel_id")
        self.guild_id: Union[str, None] = data.get("guild_id")
        self.author: User = User(data.get("author", {}))

        self.member: Member = Member(data.get("member", {}))
        self.content: Union[str, None] = data.get("content")
        self.timestamp: Union[str, None] = data.get("timestamp")
        self.edited_timestamp: Union[str, None] = data.get("edited_timestamp")
        self.tts: Union[bool, None] = data.get("tts")

        self.mention_everyone: Union[bool, None] = data.get("mention_everyone")
        self.mentions: List[User] = [
            User(mention) for mention in data.get("mentions", [])
        ]
        self.mention_roles: List[Role] = [
            Role(role) for role in data.get("mention_roles", [])
        ]
        self.mention_channels: List[ChannelMention] = [
            ChannelMention(client, cm) for cm in data.get("mention_channels", [])
        ]

        self.attachments: List[Attachment] = data.get("attachments") or []
        self.embeds: List[embed.Embed] = data.get("embeds") or []
        self.reactions: List[Reaction] = data.get("reactions") or []
        self.nonce: Union[str, int, None] = data.get("nonce")
        self.pinned: Union[bool, None] = data.get("pinned")
        self.webhook_id: Union[str, None] = data.get("webhook_id")
        self.message_type: Union[int, None] = data.get("type")
        self.activity: MessageActivity = MessageActivity(data.get("activity", {}))

        self.application: Application = Application(data.get("application", {}))
        self.application_id: Union[str, None] = data.get("application_id")
        self.message_reference: MessageReference = MessageReference(self.__client,
            data.get("message_reference", {}), data.get("referenced_message", {})
        )

        self.interaction: Interaction = Interaction(data.get("interaction", {}))
        self.thread = None
        self.components = None
        self.sticker_items: List[StickerItem] = [
            StickerItem(stick) for stick in data.get("sticker_items", [])
        ]

    @classmethod
    def create(
        cls, client,
        *,
        content: str = None,
        reply_to: MessageReference = None,
        embeds: List[embed.Embed] = None,
        attachments: List[Attachment] = None,
    ):
        if reply_to:
            reply = reply_to.to_dict()
        else:
            reply = None

        return Message(client,
            {
                "content": content if content else "",
                "message_reference": reply,
                "embeds": embeds,
                "attachments": attachments,
            }
        )

    @classmethod
    async def get_message(cls, client, channel_id, message_id):
        async with aiohttp.ClientSession() as session:
            url = f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}"

            resp = await session.get(
                url,
                headers={"Authorization": f"Bot {client.ws.bot_token}"}
            )
            rs = await resp.json()

            if resp.ok:
                return Message(client, rs)

    async def send(
        self, channel_id: str = None, *, allowed_mentions: dict = None
    ):
        """Send a message to a channel ID, returns a Message object"""
        async with aiohttp.ClientSession() as session:
            url = f"https://discord.com/api/v9/channels/{self.channel_id or channel_id}/messages"

            resp = await session.post(
                url,
                headers={"Authorization": f"Bot {self.__client.ws.bot_token}"},
                json={
                    "content": self.content,
                    "tts": self.tts,
                    "allowed_mentions": allowed_mentions,
                    "embeds": [emb.to_dict() for emb in (self.embeds or [])],
                },
            )
            rs = await resp.json()
            print(rs)
            if resp.ok:
                return Message(self.__client, rs)
            

    async def delete(self):
        async with aiohttp.ClientSession() as session:
            url = f"https://discord.com/api/v9/channels/{self.channel_id}/messages/{self.message_id}"
            await session.delete(
                url, headers={"Authorization": f"Bot {self.__client.ws.bot_token}"}
            )

    # TODO: Implement attachments and files
    async def edit(self, *, content: str = None, 
        embeds: typing.List[models.Embed] = None,
        allowed_mentions: dict = None
    ):
        async with aiohttp.ClientSession() as session:
            url = f"https://discord.com/api/v9/channels/{self.channel_id}/messages/{self.message_id}"
            await session.patch(
                url, headers={"Authorization": f"Bot {self.__client.ws.bot_token}"},
                json={
                    "content": content if content else "",
                    "embeds": [embed.to_dict() for embed in (embeds or [])],
                    "allowed_mentions": allowed_mentions
                }
            )            

    async def pin(self):
        async with aiohttp.ClientSession() as session:
            url = f"https://discord.com/api/v9/channels/{self.channel_id}/pins/{self.message_id}"

            await session.put(
                url, headers={"Authorization": f"Bot {self.__client.ws.bot_token}"}
            )
    
    async def unpin(self):
        async with aiohttp.ClientSession() as session:
            url = f"https://discord.com/api/v9/channels/{self.channel_id}/pins/{self.message_id}"

            await session.delete(
                url, headers={"Authorization": f"Bot {self.__client.ws.bot_token}"}
            )        
