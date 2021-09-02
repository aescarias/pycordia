from typing import Union
from .user import User


class Member:
    def __init__(self, data: dict):
        self.user: User = User(data.get("user", {}))
        self.nick: Union[str, None] = data.get("nick")
        self.roles: list = data.get("roles", [])
        self.joined_at: Union[str, None] = data.get("joined_at")
        self.premium_since: Union[str, None] = data.get("premium_since")
        self.deaf: Union[bool, None] = data.get("deaf")
        self.mute: Union[bool, None] = data.get("mute")
        self.pending: Union[bool, None] = data.get("pending")
        self.permissions: Union[str, None] = data.get("permissions")