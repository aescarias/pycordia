from typing import List, Union
import aiohttp
import enum
from . import embed
from .user import User
from .guild import Member, Role

# class TextChannel:
#     pass

# class GuildMember:
#     pass


class MessageActivity:
    """A message activity object"""

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


class Role:
    def __init__(self, data: dict):
        self.role_id: Union[str, None] = data.get("id")
        self.role_name: Union[str, None] = data.get("name")

        self.color: Union[int, None] = data.get("color")
        self.colour = self.color

        self.hoist: Union[bool, None] = data.get("hoist")
        self.position: Union[int, None] = data.get("position")
        self.permissions: Union[str, None] = data.get("permissions")
        self.managed: Union[bool, None] = data.get("managed")
        self.mentionable: Union[bool, None] = data.get("mentionable")

        self.tags: Union[RoleTags, None] = data.get("tags")

    def __repr__(self):
        return f"<pycordia.models.Role - id={self.role_id} name={self.role_name}>"


class Reaction:
    def __init__(self, data: dict):
        self.count: Union[int, None] = data.get("count")
        self.was_me: Union[bool, None] = data.get("me")
        self.emoji: Emoji = Emoji(data.get("emoji", {}))

    def __repr__(self):
        return (
            f"<pycordia.models.Reaction - emoji={self.emoji.name} count={self.count}>"
        )


class Emoji:
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
    def __init__(self, data: dict):
        self.sticker_id = data.get("id")
        self.name = data.get("name")
        self.format_type = data.get("type")

    def __repr__(self):
        return f"<pycordia.models.StickerItem - id={self.sticker_id} name={self.name}>"


class Attachment:
    def __init__(self, data: dict):
        """An attachment for a message

        Arguments:
            attachment_id (int): The ID of the attachment
            filename (str): The attachment's filename
            content_type (str): The content type
            size (int):
            url (str):
            proxy_url (str):
            height (int):
            width (int):
        """
        self.attachment_id: Union[str, None] = data.get("id")
        self.filename: Union[str, None] = data.get("filename")
        self.content_type: Union[str, None] = data.get("content_type")
        self.size: Union[int, None] = data.get("size")
        self.url: Union[str, None] = data.get("url")
        self.proxy_url: Union[str, None] = data.get("proxy_url")
        self.height: Union[int, None] = data.get("height")
        self.width: Union[int, None] = data.get("width")

    def to_dict(self):
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
    def __init__(self, data: dict):
        self.interaction_id = data.get("id")
        self.interaction_type = data.get("type")
        self.name = data.get("name")
        self.user = User(data.get("user", {}))


class MessageReference:
    def __init__(self, ref_data: dict, msg_data: dict):
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
        return Message(self.__msg_data or {})

    def to_dict(self):
        return {
            "message_id": self.message_id,
            "channel_id": self.channel_id,
            "guild_id": self.guild_id,
            "fail_if_not_exists": self.fail_if_not_exists,
        }


class Message:
    def __init__(self, data: dict):
        self.__data = data

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
            ChannelMention(cm) for cm in data.get("mention_channels", [])
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
        self.message_reference: MessageReference = MessageReference(
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
        cls,
        *,
        content: str = "",
        reply_to: MessageReference = None,
        embeds: List[embed.Embed] = None,
        attachments: List[Attachment] = None,
    ):
        if reply_to:
            reply = reply_to.to_dict()
        else:
            reply = None

        return Message(
            {
                "content": content,
                "message_reference": reply,
                "embeds": embeds,
                "attachments": attachments,
            }
        )

    async def send(
        self, client, channel_id: str = None, *, allowed_mentions: dict = None
    ):
        async with aiohttp.ClientSession() as session:
            url = f"https://discord.com/api/v9/channels/{self.channel_id or channel_id}/messages"

            resp = await session.post(
                url,
                headers={"Authorization": f"Bot {client.ws.bot_token}"},
                json={
                    "content": self.content,
                    "tts": self.tts,
                    "allowed_mentions": allowed_mentions,
                    "embeds": [emb.to_dict() for emb in (self.embeds or [])],
                },
            )
            print(await resp.json())

    async def delete(self, client):
        async with aiohttp.ClientSession() as session:
            url = f"https://discord.com/api/v9/channels/{self.channel_id}/messages/{self.message_id}"
            await session.delete(
                url, headers={"Authorization": f"Bot {client.ws.bot_token}"}
            )
