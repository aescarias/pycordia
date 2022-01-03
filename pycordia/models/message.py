from __future__ import annotations

import enum
import io
from datetime import datetime
from typing import List, Optional, Union

import pycordia
from pycordia import models, utils


class MessageActivityType(enum.Enum):
    join = 1
    spectate = 2
    listen = 3
    join_request = 5

class MessageActivity:
    """
    Message Activity class

    Attributes:
        activity_type (`pycordia.models.message.MessageActivityType`): Type of activity
        party_id (str): ID of the party
    """

    def __init__(self, data: dict):
        self.activity_type = utils.make_optional(MessageActivityType, data.get("type"))
        self.party_id: Optional[str] = data.get("party_id")

    def __repr__(self):
        return f"<MessageActivity id={self.party_id} activity={self.activity_type}>"


class Application:
    """Discord application model."""
    def __init__(self, data: dict):
        self.id: str = data["id"]
        self.name: str = data["name"]
        self.icon_hash: Optional[str] = data.get("icon")
        self.description: str = data["description"]

        self.rpc_origins: list = data.get("rpc_origins", [])
        self.bot_public: bool = data["bot_public"]
        self.bot_require_code_grant: bool = data["bot_require_code_grant"]

        self.terms_of_service_url: Optional[str] = data.get("terms_of_service_url")
        self.privacy_policy_url: Optional[str] = data.get("privacy_policy_url")
        self.owner: Optional[models.User] = utils.make_optional(models.User, data.get("owner", {}))

        self.cover_image_hash: Optional[str] = data.get("cover_image")
        self.flags: Optional[int] = data.get("flags")

    def __repr__(self):
        return f"<Application id={self.id} name='{self.name}'>"

    @property
    def icon_url(self) -> Optional[str]:
        """The URL for this application's icon"""
        if self.icon_hash:
            return f"{pycordia.cdn_url}/app-icons/{self.id}/{self.icon_hash}.png"

    @property
    def cover_image_url(self) -> Optional[str]:
        """The URL for this application's cover image"""
        if self.cover_image_hash:
            return f"{pycordia.cdn_url}/app-icons/{self.id}/{self.cover_image_hash}.png"


class Reaction:
    """Represents reactions in a message."""
    def __init__(self, data: dict):
        self.count: Optional[int] = data.get("count")
        self.me: Optional[bool] = data.get("me")
        self.emoji: Optional[models.Emoji] = utils.make_optional(models.Emoji, data.get("emoji", {}))

    def __repr__(self):
        return f"<Reaction emoji={str(self.emoji)} count={self.count}"



class StickerItem:
    """Represents a Discord sticker item"""
    def __init__(self, data: dict):
        self.sticker_id = data.get("id")
        self.name = data.get("name")
        self.format_type = data.get("type")

    def __repr__(self):
        return f"<StickerItem id={self.sticker_id} name='{self.name}'>"


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
        self.id: str = data["id"]
        self.filename: str = data["filename"]
        self.content_type: Optional[str] = data.get("content_type")
        self.size: Optional[int] = data.get("size")
        self.url: Optional[str] = data.get("url")
        self.proxy_url: Optional[str] = data.get("proxy_url")
        self.height: Optional[int] = data.get("height")
        self.width: Optional[int] = data.get("width")

    def to_dict(self):
        """
        Return raw dictionary of object
        Returns: dict
        """
        return utils.obj_to_dict(self)


class File:
    """Represents a file, sent to Discord when sending an attachment
    
    Attributes
        filename (str): The filename for the attachment
        fp (io.BufferedIOBase): A file object for the attachment
        description (str): A description of the attachment used as alt text
    """
    def __init__(self, *, filename: str, fp: io.BufferedIOBase, description: str = None):
        self.filename = filename
        self.fp = fp
        self.description = description


class Interaction:
    """
    Represents a Discord interaction

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
        self.user = utils.make_optional(models.User, data.get("user", {}))


class MessageReference:
    def __init__(self, ref_data: dict, msg_data: dict):
        self.__msg_data = msg_data

        if ref_data:
            self.message_id: Optional[str] = ref_data.get("message_id")
            self.channel_id: Optional[str] = ref_data.get("channel_id")
            self.guild_id: Optional[str] = ref_data.get("guild_id")
            self.fail_if_not_exists: Optional[bool] = ref_data.get(
                "fail_if_not_exists"
            )
        else:
            self.message_id = (
                self.channel_id
            ) = self.guild_id = self.fail_if_not_exists = None

    @property
    def message(self):
        """The referenced message"""
        return utils.make_optional(Message, self.__msg_data)

    def to_dict(self):
        return utils.obj_to_dict(self)
    
    def __eq__(self, other) -> bool:
        return self.message_id == other.message_id


class Message:
    """Represents a message sent in Discord
    
    Attributes:
        id (str): ID of the message
        channel_id (str): ID of the channel the message was sent in
        guild_id (str): ID of the guild the message was sent in
        author (User): The author of this message
        member (Member): The author of this message, including guild information
        content (str): Content of the message
        timestamp (datetime): The time the message was sent
        edited_timestamp (datetime): The time the message was edited
        tts (bool): Whether the message supports Text to Speech
        mention_everyone (bool): Whether this message mentions everyone
        mentions (List[User]): A list of users this message mentions
        mention_roles (List[Role]): A list of roles this message mentions
        mention_channels (List[ChannelMention]): A list of channels this message mentions
        attachments (List[Attachment]): The attachments for this message
        embeds (List[embed.Embed]): The embeds for this message
        reactions (List[Reaction]): Reactions for this message
        nonce (Union[str, int, None]): Used for message verification
        pinned (bool): Whether this message is pinned
        webhook_id (str): The ID Of the webhook that sent this message
        type (int): Message type;
        activity (str): The Rich-Presence chat embed if any
        application (str): The application for the Rich-Presence chat embed
        application_id (str): The ID of the application for the embed
        message_reference (MessageReference): The message referred to
        flags (int): Flags for this message
        interaction (dict): An interaction for this message -- not implemented
        thread (dict): The thread that was started from this message -- not implemented
        components (dict): The list of components for this message -- not implemented
        sticker_items (List[StickerItem]): Stickers sent in this message
    """
    def __init__(self, data: dict):
        self.__data = data

        self.id: str = data["id"]
        self.channel_id: str = data["channel_id"]
        self.guild_id: Optional[str] = data.get("guild_id")
        self.author: models.User = models.User(data["author"])

        self.member: Optional[models.Member] = utils.make_optional(models.Member, data.get("member", {}))
        self.content: str = data["content"]
        self.timestamp: datetime = datetime.fromisoformat(data["timestamp"])
        self.edited_timestamp: Optional[datetime] = utils.make_optional(datetime.fromisoformat, data.get("edited_timestamp"))
        self.tts: bool = data["tts"]

        self.mention_everyone: bool = data["mention_everyone"]

        self.mentions: List[models.User] = list(map(models.User, data.get("mentions", [])))
        self.mention_roles: List[models.Role] = list(map(models.Role, data.get("mention_roles", [])))
        self.mention_channels: List[models.ChannelMention] = list(
            map(models.ChannelMention, data.get("mention_channels", []))
        )

        self.attachments: List[Attachment] = list(map(Attachment, data.get("attachments", [])))
        self.embeds: List[models.Embed] = list(map(models.Embed, data.get("embeds", [])))
        self.reactions: List[Reaction] = list(map(Reaction, data.get("reactions", [])))
        self.nonce: Union[str, int, None] = data.get("nonce")
        self.pinned: bool = data["pinned"]
        self.webhook_id: Optional[str] = data.get("webhook_id")
        self.type: int = data["type"]
        self.activity: Optional[MessageActivity] = utils.make_optional(MessageActivity, data.get("activity", {}))

        self.application: Optional[Application] = utils.make_optional(Application, data.get("application", {}))
        self.application_id: Optional[str] = data.get("application_id")
        self.message_reference: MessageReference = MessageReference(
            data.get("message_reference", {}), 
            data.get("referenced_message", {})
        )

        self.flags: Optional[int] = data.get("flags")

        self.interaction: dict = data.get("interaction", {})
        self.thread: dict = data.get("thread", {})
        self.components: list = data.get("components", [])

        self.sticker_items: List[StickerItem] = list(map(StickerItem, data.get("sticker_items", [])))

    @classmethod
    async def send(cls, channel_id: str, *,
        content: str = "", 
        embeds: List[models.Embed] = None,
        files: List[File] = None,
        allowed_mentions: dict = {},
        allow_tts: bool = False
    ) -> Message:
        """Send a Discord message to a channel

        Args:
            channel_id (str): The ID of the channel where the message will be sent
            content (str, optional): The content of the message.
            embeds (List[models.Embed], optional): A list of `pycordia.models.Embed` objects.
            files (List[models.File], optional): A list of `pycordia.models.File` objects
            allowed_mentions (dict, optional): \
                A dictionary of allowed mentions. Dictionary keys are as follows, \
                    dictionary values are booleans: \n
                roles: Allow role mentions \n
                users: Allow user mentions \n
                everyone: Allow @everyone and @here mentions \n
            allow_tts (bool, optional): Indicate if the message allows text-to-speech. 

        Returns: `pycordia.models.Message`
        """

        client = models.active_client
        if not client:
            raise pycordia.errors.ClientSetupError
        
        rs = await client.http.request(
            "POST",
            f"channels/{channel_id}/messages",
            payload_json={
                "content": content or "",
                "tts": allow_tts,
                "allowed_mentions": allowed_mentions,
                "embeds": [emb.to_dict() for emb in (embeds or [])]
            },
            files=files
        )

        return Message(await rs.json())
    
    @classmethod
    async def from_id(cls, channel_id: str, message_id: str) -> Message:
        """Get a message given a channel ID and a message ID
        
        Returns: `pycordia.models.Message`
        """
        client = models.active_client
        if not client:
            raise pycordia.errors.ClientSetupError

        rs = await client.http.request("GET", f"channels/{channel_id}/messages/{message_id}")
        return Message(await rs.json())

    @classmethod
    async def bulk_delete(cls, channel_id: str, *message_ids: List[str]) -> None:
        """Bulk delete multiple messages (from 2 to 100)

        Args:
            channel_id: A channel ID to remove messages from
            message_ids: A list of message IDS to delete

        Note: Messages older than two weeks will not be affected. \
            You'll receive an error if you attempt to do so.
        """
        client = models.active_client
        if not client:
            raise pycordia.errors.ClientSetupError
        
        await client.http.request(
            "POST", 
            f"/channels/{channel_id}/messages/bulk-delete", 
            payload_json={ "messages": message_ids }
        )


    async def delete(self):
        """Removes this message. Note that this action cannot be undone."""
        client = models.active_client
        if not client:
            raise pycordia.errors.ClientSetupError

        await client.http.request("DELETE", f"channels/{self.channel_id}/messages/{self.id}")

    async def edit(self, *, content: str = None, 
        embeds: List[models.Embed] = None,
        allowed_mentions: dict = None
    ):
        """Edit this message

        Args:
            content (str, optional): The new content of this message.
            embeds (typing.List[models.Embed], optional): A new list of `embed.Embed` objects 
            allowed_mentions (dict, optional): A new dictionary of allowed mentions. \
                Structure is the same as specified in `pycordia.models.Message.send`
        """
        client = models.active_client
        if not client:
            raise pycordia.errors.ClientSetupError
        
        await client.http.request("PATCH", 
            f"channels/{self.channel_id}/messages/{self.id}", 
            payload_json={
                "content": content or self.content,
                "embeds": [embed.to_dict() for embed in (embeds or self.embeds)],
                "allowed_mentions": allowed_mentions
            }
        )      

    async def pin(self):
        """Pins a message to the channel it was sent in"""
        client = models.active_client
        if not client:
            raise pycordia.errors.ClientSetupError

        await client.http.request("PUT", f"channels/{self.channel_id}/pins/{self.id}")
    
    async def unpin(self):
        """Unpins a message from the channel it was sent in"""
        client = models.active_client
        if not client:
            raise pycordia.errors.ClientSetupError
        
        await client.http.request("DELETE", f"channels/{self.channel_id}/pins/{self.id}")
    
    async def crosspost(self):
        """Crosspost this message to other following channels"""
        client = models.active_client
        if not client:
            raise pycordia.errors.ClientSetupError

        await client.http.request(
            "POST", 
            f"channels/{self.channel_id}/messages/{self.id}/crosspost"
        )
