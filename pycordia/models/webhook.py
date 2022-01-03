from __future__ import annotations

import pycordia
import enum
from typing import List, Optional

from pycordia import models, utils


class Webhook:
    def __init__(self, data):
        self.id: str = data["id"]
        self.type = WebhookType(data["type"])
        self.guild_id: Optional[str] = data.get("guild_id")
        self.channel_id: str = data["channel_id"]
        self.user: Optional[models.User] = utils.make_optional(
            models.User, data.get("user")
        )
        
        self.name: Optional[str] = data.get("name")
        self.avatar_hash: str = data.get("avatar")
        self.token: str = data.get("token")
        self.application_id: str = data.get("application_id")
        self.source_guild: str = data.get("guild")
        self.source_channel: str = data.get("source_channel")
        self.url: str = data.get("url")

    @classmethod
    async def create(cls, channel_id: str, *, name, avatar=None) -> Webhook:
        client = models.active_client
        if not client:
            raise pycordia.errors.ClientSetupError
        
        rs = await client.http.request(
            "POST", f"channels/{channel_id}/webhooks", 
            payload_json={ "name": name, "avatar": avatar }
        )

        return Webhook(await rs.json())
    
    @classmethod
    async def from_id(cls, webhook_id: str) -> Webhook:
        client = models.fetch_client()
        rs = await client.http.request(
            "GET", f"webhooks/{webhook_id}"
        )
        return Webhook(await rs.json())

    @classmethod
    async def from_token(cls, webhook_id: str, token: str) -> Webhook:
        client = models.fetch_client()
        rs = await client.http.request(
            "GET", f"webhooks/{webhook_id}/token"
        )
        return Webhook(await rs.json())

    # async def edit(self, *, name, avatar=None, channel_id) -> None:
    #     client = models.fetch_client()

    #     rs = await client.http.request(
    #         "PATCH", f"webhooks/{self.id}", payload_json={
    #             "name": name,
    #             "avatar": avatar,
    #             "channel_id": channel_id
    #         }
    #     )

    async def delete(self, *, use_token: bool = False) -> None:
        client = models.fetch_client()

        if use_token:
            await client.http.request(
                "DELETE", f"webhooks/{self.id}/{self.token}"
            )       
        else:
            await client.http.request(
                "DELETE", f"webhooks/{self.id}"
            ) 

    async def execute(self, *, 
        content: str = "",
        username: str = None,
        avatar_url: str = None,    
        tts: bool = None,
        embeds: List[models.Embed] = None,
        allowed_mentions: dict = None,
        files: List[models.File] = None,
        wait: bool = False,
        thread_id: str = None
    ) -> models.Message:
        """Execute a webhook with a message

        All arguments are optional but one of `content`, `embeds` or `files` must be present

        Args:
            content (str, optional): The content of the message
            username (str, optional): Override username for the webhook
            avatar_url (str, optional): Override avatar for the webhook
            tts (bool, optional): Whether to send as a text-to-speech message
            embeds (List[models.Embed], optional): A list of embeds to attach. 10 at most.
            allowed_mentions (dict, optional): The allowed mentions for the message.
                Same as `pycordia.models.Message.send`
            
            files (List[models.File], optional): A list of files to attach.
            
            wait (bool, optional): Whether to wait for a confirmed message send \
                before response. Defaults to False.
            
            thread_id (str, optional): The ID of the channel thread to send \
                the webhook message in
        """

        client = models.fetch_client()

        attachments = []
        if files:
            for fl in files:
                attachments.append({
                    "filename": fl.filename,
                    "description": fl.description
                })

        await client.http.request("POST", f"webhooks/{self.id}/{self.token}",
            payload_json={
                "content": content,
                "username": username,
                "avatar_url": avatar_url,
                "tts": tts,
                "embeds": embeds,
                "allowed_mentions": allowed_mentions,
                "attachments": attachments
            },
            params={
                "wait": wait,
                "thread_id": thread_id
            },
            files=files
        )



    


class WebhookType(enum.Enum):
    incoming = 1
    channel_follower = 2
    application = 3
