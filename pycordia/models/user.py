from typing import Optional
from pycordia import api, utils
from datetime import datetime
import pycordia


class User:
    """
    A Discord User

    Attributes:
        id (str): ID of the user
        username (str): A username
        discriminator (str): A user's discriminator; a `#` followed by 4 numbers
        avatar_hash (str): User's avatar hash
        bot (bool): Whether the user is a bot or not
        system (bool): Whether the user is an official Discord System User
        mfa_enabled (bool): Whether the user has 2FA enabled
        banner_hash (str): User's banner hash
        accent_color (int): User's banner color, better represented as hexadecimal
        locale (str): User's chosen language
        verified (bool): Whether the user's email has been verified. Can only be accessed from the email scope, in OAuth2 applications
        email (str): User's email. Can only be accessed from the email scope, in OAuth2 applications
        flags (int): Flags on user's account
        premium_type (int): Nitro subscription type: 0 - None, 1 - Nitro Classic, 2 - Nitro
        public_flags (int): Public flags on a user's account

    Operations:
        - str(x): Returns the username + discriminator
        - repr(x): Returns a representation of the object
        - x == y: Checks if two users are the same (check by ID)
    """
    def __init__(self, data):
        self.id: str = data["id"]
        self.username: str = data["username"]
        self.discriminator: str = data["discriminator"]
        self.avatar_hash: str = data["avatar"]
        self.bot: Optional[bool] = data.get("bot")
        self.system: Optional[bool] = data.get("system")
        self.mfa_enabled: Optional[bool] = data.get("mfa_enabled")
        self.banner_hash: Optional[str] = data.get("banner")
        self.accent_color: Optional[int] = data.get("accent_color")
        self.locale: Optional[str] = data.get("locale")
        self.verified: Optional[bool] = data.get("verified")
        self.email: Optional[str] = data.get("email")
        self.flags: Optional[int] = data.get("flags")
        self.premium_type: Optional[int] = data.get("premium_type")
        self.public_flags: Optional[int] = data.get("public_flags")

    def __str__(self):
        return f"{self.username}#{self.discriminator}"

    def __repr__(self):
        return f"<User id={self.id} username='{self.username}' bot={self.bot}>"    

    @property
    def mention(self) -> str:
        """The mention for this user"""
        return f"<@!{self.id}>"

    @property
    def avatar_url(self) -> Optional[str]:
        """The avatar URL for this user"""
        if self.avatar_hash:
            return f"{pycordia.cdn_url}/avatars/{self.id}/{utils.add_ext(self.avatar_hash)}"

    @property
    def banner_url(self) -> Optional[str]:
        """The banner URL for this user"""
        if self.banner_hash:
            return f"{pycordia.cdn_url}/banners/{self.id}/{utils.add_ext(self.banner_hash)}"

    @property
    def created_on(self) -> datetime:
        """The date and time the user was created on"""
        return utils.snowflake_to_date(int(self.id))

    @classmethod
    async def from_id(cls, user_id: str, use_cache: bool = True):
        """
        Get a User object, given a user ID

        Args:
            user_id (str): ID of the user to fetch
            use_cache (bool): Whether to check in cache first, or not

        Returns: A `pycordia.models.user.User` object
        """
        client = pycordia.models.active_client
        if not client:
            raise Exception("No initialized client found")

        # Check if its present in the cache first
        user = client.user_cache.get(user_id)
        if user and use_cache:
            return user

        # Otherwise, fetch directly from the API
        rs = await api.request("GET", f"users/{user_id}")
        user = User(rs)

        # Add to cache
        if len(client.user_cache.keys()) >= client.cache_size:
            first_user = list(client.user_cache.keys())[0]
            del client.user_cache[first_user]
        
        client.user_cache[user.id] = user

        return user

    def __eq__(self, other: 'User'):
        return self.id == other.id
