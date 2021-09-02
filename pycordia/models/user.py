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
        return f"<@!{self.user_id}"

    @property
    def avatar_url(self):
        return f"https://cdn.discordapp.com/avatars/{self.user_id}/{self.avatar_hash}.png"
