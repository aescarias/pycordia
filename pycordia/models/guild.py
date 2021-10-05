from __future__ import annotations
import typing
import aiohttp
import enum
from typing import List, Union, Optional
from .user import User
from pycordia import api


class Emoji:
    """Represents server specific emojis."""
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
        return f"<Emoji id={self.emoji_id} name='{self.name}'>"


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

    Operations:
        - x == y: Checks if two channels are the same.
        - str(x): Return username with discriminator
    """
    def __init__(self, data: dict):
        self.user: User = User(data.get("user", {}))
        self.nick: Union[str, None] = data.get("nick")
        # NOTE: Uncomment when Roles are properly implemented
        # self.roles: list = list(map(Role, data.get("roles", [])))
        self.roles: list = data.get("roles", [])
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
        return f"<PartialGuild id={self.id} name='{self.name}'>"


class RoleTags:
    def __init__(self, data: dict):
        self.bot_id = data.get("bot_id")
        self.integration_id = data.get("integration_id")
        self.premium_subscriber = data.get("premium_subscriber")

    def __repr__(self):
        return f"<RoleTags bot_id={self.bot_id}>"


class Role:
    """
    Model to represent a guild's role.

    Attributes:
        id (str): ID of role
        name (str): Name of role
        color (int): Role color
        colour (int): Role colour
        hoist (bool): Whether the role is hoisted
        icon_hash (str): The icon hash for the icon
        unicode_emoji (str): The role's unicode emoji if a default emoji
        position (int): Role position in the hierarchy
        permissions (str): Permissions granted to the role
        managed (bool): Whether the role is a managed role
        mentionable (bool): Whether users can mention the role
        tags (List[RoleTags]): The tags for this role

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

        self.tags: List[RoleTags] = [RoleTags(tag) for tag in data.get("tags", [])]
    

    def __eq__(self, other) -> bool:
        return self.role_id == other.role_id
    
    def __gt__(self, other) -> bool:
        """Check if the role is higher up than another"""
        return self.role_id > other.role_id

    def __lt__(self, other) -> bool:
        """Check if the role is lower than another"""
        return self.role_id < other.role_id

    def __repr__(self):
        return f"<Role id={self.role_id} name='{self.role_name}'>"


class GuildVerificationLevel(enum.Enum):
    none = 0
    low = 1
    medium = 2
    high = 3
    very_high = 4

class GuildNotificationLevel(enum.Enum):
    all_messages = 0
    only_mentions = 1

class GuildExplicitContentFilter(enum.Enum):
    disabled = 0
    members_without_roles = 1
    all_members = 2


class GuildNSFWLevel(enum.Enum):
    default = 0
    explicit = 1
    safe = 2
    age_restricted = 3

class GuildMFALevel(enum.Enum):
    none = 0
    elevated = 1

class GuildPremiumTier(enum.Enum):
    none = 0
    tier_1 = 1
    tier_2 = 2
    tier_3 = 3

class Guild:
    def __init__(self, data: dict) -> None:
        self.id: str = data["id"]
        self.name: str = data["name"]
        self.icon_hash: Optional[str] = data.get("icon")
        self.template_icon_hash: Optional[str] = data.get("icon_hash")
        self.splash_hash: Optional[str] = data.get("splash")
        self.discovery_splash_hash: Optional[str] = data.get("discovery_splash")
        self.is_bot_owner: Optional[str] = data.get("owner")
        self.owner_id: str = data["owner_id"]
        self.permissions: Optional[str] = data.get("permissions")
        self.afk_channel_id: Optional[str] = data.get("afk_channel_id")
        self.afk_timeout: int = data["afk_timeout"]
        self.has_widget_enabled: Optional[bool] = data.get("widget_enabled")
        self.widget_channel_id: Optional[str] = data.get("widget_channel_id")
        self.verification_level = GuildVerificationLevel(data["verification_level"])
        self.message_notifcations_level = GuildNotificationLevel(data["default_message_notifications"])
        self.explicit_content_filter = GuildExplicitContentFilter(data["explicit_content_filter"])
        self.roles: List[Role] = [Role(role) for role in data["roles"]]
        self.emojis: List[Emoji] = [Emoji(emoji) for emoji in data["emojis"]]
        self.features: List[str] = data["features"]
        self.mfa_level = GuildMFALevel(data["mfa_level"])
        self.application_id: Optional[str] = data.get("application_id")
        self.system_channel_id: Optional[str] = data.get("system_channel_id")
        self.system_channel_flags = data.get("system_channel_flags")
        self.rules_channel_id: Optional[str] = data.get("rules_channel_id")
        self.joined_at: Optional[str] = data.get("joined_at")
        self.large: Optional[bool] = data.get("large")
        self.unavailable: Optional[bool] = data.get("unavailable")
        self.member_count: int = data.get("member_count", -1)
        self.voice_states = data.get("voice_states")
        self.members: List[Member] = [Member(mem) for mem in data.get("members", [])]
        self.channels = data.get("channels")
        self.threads = data.get("threads")
        self.presences = data.get("presences")
        self.max_presences: Optional[int] = data.get("max_presences")
        self.max_members: Optional[int] = data.get("max_members")
        self.vanity_url_code: Optional[str] = data.get("vanity_url_code")
        self.description: Optional[str] = data.get("description")
        self.banner_hash: Optional[str] = data.get("banner")
        self.premium_tier = GuildPremiumTier(data["premium_tier"])
        self.premium_subscription_count: Optional[int] = data.get("premium_subscription_count")
        self.preferred_locale: str = data["preferred_locale"]
        self.public_updates_channel_id: Optional[str] = data.get("public_updates_channel_id")
        self.max_video_channel_users: Optional[int] = data.get("max_video_channel_users")
        self.approximate_member_count: Optional[int] = data.get("approximate_member_count")
        self.approximate_presence_count: Optional[int] = data.get("approximate_presence_count")
        self.welcome_screen = data.get("welcome_screen")
        self.nsfw_level = GuildNSFWLevel(data["nsfw_level"])
        self.stage_instances = data.get("stage_instances")
        self.stickers = data.get("stickers")

    @classmethod
    async def from_id(cls, guild_id: str, *, with_counts: bool = False) -> Guild:
        """Get a guild from an ID
        
        Args:
            guild_id (str): A guild ID
            with_counts (bool): Whether or not to add approximate member and presence counts
        
        Returns: `Guild`
        """
        rs = await api.request("GET", f"guilds/{guild_id}{'?with_counts=true'*with_counts}")
        return Guild(rs)
