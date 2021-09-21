import aiohttp
import pycordia


class User:
    """
    Model to mirror a Discord User

    Attributes:
        user_id (str): ID of the user
        username (str): Username
        discriminator (str): User's discriminator - a # followed by 4 numbers
        avatar_hash (str): User's avatar hash
        bot (bool): Whether the user is a bot or not
        system (bool): Whether the user is an official Discord System User
        mfa_enabled (bool): Whether the user has 2FA enabled
        banner (str): User's banner hash
        accent_color (int): User's banner color, in hex, encoded as an int
        locale (str): User's chosen language
        verified (bool): Whether the user's email has been verified. Can only be accessed from the email scope, in OAuth2 applications
        email (str): User's email. Can only be accessed from the email scope, in OAuth2 applications
        flags (int): Flags on user's account
        premium_type (int): Nitro subscription type: 0 - None, 1 - Classic, 2 - Nitro
        public_flags (int): Public flags on a user's account

    ---

    Operations:
        - str(x): Returns the username + discriminator
        - x == y: Checks if two users are the same
    """
    def __init__(self, json):
        self.user_id: str = json.get("id")
        self.username: str = json.get("username")
        self.discriminator: str = json.get("discriminator")
        self.avatar_hash: str = json.get("avatar")
        self.bot: bool = json.get("bot")
        self.system: bool = json.get("system")
        self.mfa_enabled: bool = json.get("mfa_enabled")
        self.banner: str = json.get("banner")
        self.accent_color: int = json.get("accent_color")
        self.locale: str = json.get("locale")
        self.verified: bool = json.get("verified")
        self.email: str = json.get("email")
        self.flags: int = json.get("flags")
        self.premium_type: int = json.get("premium_type")
        self.public_flags: int = json.get("public_flags")

    def __repr__(self):
        return f"{self.username}#{self.discriminator}"

    @property
    def mention(self) -> str:
        """Mention a user"""
        return f"<@!{self.user_id}>"

    @property
    def avatar_url(self) -> str:
        """Get the avatar url of a user"""
        return f"{pycordia.cdn_url}/avatars/{self.user_id}/{self.avatar_hash}.png"

    @classmethod
    async def user_from_id(cls, client, user_id: str, use_cache: bool = True):
        """
        Get user info, given the user id

        Args:
            client (Client): `pycordia.client.Client` object to use while fetching
            user_id (str): ID of the user to fetch
            use_cache (bool): Whether to check in cache first, or not

        Returns: A `pycordia.models.user.User` object if the user is found, else None

        """

        # Check if its present in the cache first -
        user = client.user_cache.get(user_id, None)
        if user and use_cache:
            return user

        # Else, fetch it from the discord api
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{pycordia.api_url}/users/{user_id}",
                headers={
                    "Authorization": f"Bot {client._Client__bot_token}"
                }
            ) as resp:

                if not resp.ok:
                    return None

                json = await resp.json()
                user = User(json)

                if len(client.user_cache.keys()) >= client.cache_size:
                    first_user = list(client.user_cache.keys())[0]
                    del client.user_cache[first_user]

                client.user_cache[user.user_id] = user

                return user

    def __eq__(self, other):
        return self.user_id == other.user_id
