import aiohttp
import pycordia


class User:
    """Model used for users"""
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
    def mention(self):
        return f"<@!{self.user_id}>"

    @property
    def avatar_url(self):
        return f"{pycordia.cdn_url}/avatars/{self.user_id}/{self.avatar_hash}.png"

    @classmethod
    async def user_from_id(cls, client, user_id: str, use_cache: bool = True):
        """Get user info, given the user id"""

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
                    return

                json = await resp.json()
                user = User(json)

                if len(client.user_cache.keys()) < 1000:
                    client.user_cache[user.user_id] = user

                return user
