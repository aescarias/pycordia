import typing
import aiohttp
from typing import List, Union, Optional
from .user import User


class Member:
    """
    Model to represent Discord guild user

    Attributes:
        user (User): The `pycordia.models.user.User` instance of the member
        nick (str): Nickname of the user. Can be `None` if no nickname has been set
        roles (List[Role]): User's roles, as a list of `pycordia.models.guild.Role` objects
        joined_at (str): An ISO8601 timestamp of when the user joined
        premium_since (str): An ISO8601 timestamp of when the user started boosting the server
        deaf (bool): Whether the user has been deafened in a voice channel
        mute (bool): Whether the user has been muted in a voice channel
        pending (bool): Whether the user has not yet passed the guild's membership requirements
        permissions (string): total permissions of the member in the channel, including overwrites

    ---

    Operations:
        - x == y: Checks if two channels are the same.
        - str(x): Return username with discriminator
    """
    def __init__(self, data: dict):
        self.user: User = User(data.get("user", {}))
        self.nick: Union[str, None] = data.get("nick")
        self.roles: list = list(map(Role, data.get("roles", [])))
        self.joined_at: Union[str, None] = data.get("joined_at")
        self.premium_since: Union[str, None] = data.get("premium_since")
        self.deaf: Union[bool, None] = data.get("deaf")
        self.mute: Union[bool, None] = data.get("mute")
        self.pending: Union[bool, None] = data.get("pending")
        self.permissions: Union[str, None] = data.get("permissions")
    
    def __eq__(self, other) -> bool:
        return self.user.user_id == other.user.user_id

    def __repr__(self):
        return f"{self.user.username}#{self.user.discriminator}"


class PartialGuild:
    """
    Represents a partial guild
    
    Attributes:
        id (str): ID of the guild.
        name (str): Name of the guild.
        icon (str): URL to icon of the guild.
        owner (bool): -
        permissions_integer (Any): Permissions integer of the guild.
        features (List[str]): List of features available to the guild.
    """
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.name: str = data.get("name")
        self.icon: str = data.get("icon")
        self.owner: bool = bool(data.get("owner"))
        self.permissions_integer = data.get("permissions")
        self.features: typing.List[str] = data.get("features", [])

    def __repr__(self):
        return f"<PartialGuild - id={self.id} name={self.name}>"


class Role:
    """
    Model to represent a guild's role.

    Attributes:
        role_id (str): ID of role
        role_name (str): Name of role
        color (int): Role color
        colour (int): Role colour
        hoist (bool): Whether the role is hoisted
        position (int): Role position in the hierarchy
        permissions (str): Permissions granted to the role
        managed (bool): Whether the role is a managed role
        mentionable (bool): Whether users can mention the role
    
    ---

    Operations:
        - x == y: Checks if two roles are the same
        - x > y: Checks if role `x` is higher up than role `y`
        - x < y: Checks if role `y` is higher up than role `x`
    """
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

        self.tags = data.get("tags")
    
    def __eq__(self, other) -> bool:
        return self.role_id == other.role_id
    
    def __gt__(self, other) -> bool:
        """Check if the role is higher up than another"""
        return self.role_id > other.role_id

    def __lt__(self, other) -> bool:
        """Check if the role is lower than another"""
        return self.role_id < other.role_id

    def __repr__(self):
        return f"<pycordia.models.Role - id={self.role_id} name={self.role_name}>"
