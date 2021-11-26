from __future__ import annotations
from pycordia import utils


class Embed:
    """
    A Discord embed.

    Attributes:
        title (str): Title of the embed
        embed_type (str): An embed type (either 'rich', 'image', 'video', 'gifv', 'article', or 'link')
        description (str): Embed description
        url (str): URL provided in embed
        timestamp (str): An ISO8601-compliant timestamp string
        color (int): The color for the embed, better represented as a hexadecimal value.
        colour (int): Embed colour
        fields (list): Embed fields
    """

    def __init__(self, data: dict):
        self.title: str = data.get("title", "")
        self.embed_type: str = data.get("type", "rich")

        self.description: str = data.get("description", "")
        self.url: str = data.get("url", "")
        self.timestamp: str = data.get("timestamp", "")

        self.color: int = data.get("color", "")

        self.colour: int = self.color
        self.fields: list = []

        # Privates
        self.__thumbnail = {}
        self.__image = {}
        self.__video = {}
        self.__footer = {}
        self.__author = {}
        self.__provider = {}

    @classmethod
    def create(
        cls, *, title: str = None, description: str = None,
       url: str = None, color: int = None
    ) -> Embed:
        """
        Create a new Embed object

        Args:
            title (str): (Optional) Title of the embed
            description (str): (Optional) Embed description
            url (str): (Optional) URL provided in Embed
            color (int): (Optional) Color of embed
        """

        return Embed({
            "title": title,
            "description": description,
            "url": url,
            "color": color
        })

    def add_field(self, name: str, value: str, inline: bool = True):
        """
        Add a field object to the embed fields
        
        Args:
            name (str): The name of the embed field
            value (str): The contents/value of the field
            inline (bool): Indicates whether the field is placed either inline or in a new row. \
                True by default
        """

        self.fields.append({
            "name": name,
            "value": value,
            "inline": inline
        })
        return self

    def __make_image(self, url, proxy_url, height, width):
        return {
            "url": url,
            "proxy_url": proxy_url,
            "height": height,
            "width": width
        }

    @property
    def thumbnail(self):
        """Embed thumbnail"""
        return self.__thumbnail

    def set_thumbnail(self, url: str, *, proxy_url: str = None, height: int = None, width: int = None):
        """
        Add a thumbnail to an embed object.

        Args:
            url (str): The URL for the thumbnail
            proxy_url (str): An alternative URL for the thumbnail
            height (int): The height of the thumbnail
            width (int): The width of the thumbnail
        """

        self.__thumbnail = self.__make_image(url, proxy_url, height, width)
        return self

    @property
    def image(self):
        """Embed image"""
        return self.__image

    def set_image(self, url, *, proxy_url: str = None, height: int = None, width: int = None):
        """
        Set embed image.

        Args:
            url (str): The URL for the image
            proxy_url (str): An alternative URL for the image
            height (int): The height of the image
            width (int): The width of the image
        """

        self.__image = self.__make_image(url, proxy_url, height, width)
        return self

    @property
    def video(self):
        """Embed video"""
        return self.__video

    def set_video(self, url, *, proxy_url: str = None, height: int = None, width: int = None):
        """
        Set embed video.

        Args:
            url (str): The URL for the video
            proxy_url (str): An alternative URL for the video
            height (int): The height of the video
            width (int): The width of the video
        """
        self.__video = self.__make_image(url, proxy_url, height, width)
        return self

    ##: Footer
    @property
    def footer(self):
        """Embed footer"""
        return self.__footer

    def set_footer(self, *, text: str, icon_url: str, proxy_url: str = None):
        """
        Set embed footer.

        Args:
            text (str): The text for the footer
            icon_url (str): An URL for the footer
            proxy_url (str): An alternative URL for the footer
        """

        self.__footer = {
            "text": text,
            "icon_url": icon_url,
            "proxy_icon_url": proxy_url
        }
        return self

    ##: Author
    @property
    def author(self):
        """Author of embed"""
        return self.__author

    def set_author(self, *, name: str, url: str, icon_url: str, proxy_url: str = None):
        """
        Set the author of an embed.

        Args:
            name (str): The name of the author
            url (str): An URL related to the author
            icon_url (str): An icon URL for the author
            proxy_url (str): A proxy URL for the author
        """

        self.__author = {
            "name": name,
            "url": url,
            "icon_url": icon_url,
            "proxy_icon_url": proxy_url
        }
        return self

    @property
    def provider(self):
        """Embed Provider"""
        return self.__provider

    def set_provider(self, *, name: str = None, url: str = None):
        """
        Set the provider of the embed.

        Args:
            name (str): The name of the provider
            url (str): The URL of the provider
        """
        self.__provider = {
            "name": name,
            "url": url
        }
        return self

    def to_dict(self):
        """Convert object into a dictionary"""
        return utils.obj_to_dict(
            self, 
            alias={"embed_type": "type"},
            ignore_fields=["colour"]
        )

    def __repr__(self):
        return f"<Embed title='{self.title}' description='{self.description}'>"
