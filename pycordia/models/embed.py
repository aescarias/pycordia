class Embed:
    """An embed object"""

    def __init__(self, data: dict):
        self.title: str = data.get("title", "")
        self.embed_type: str = data.get("type", "rich")
        """An embed type (either 'rich', 'image', 'video', 'gifv', 'article', or 'link')"""

        self.description: str = data.get("description", "")
        self.url: str = data.get("url", "")
        self.timestamp: str = data.get("timestamp", "")
        """An ISO8601-compliant timestamp string"""

        self.color: int = data.get("color", "")
        """The color for the embed, better represented as a hexadecimal value."""

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
    def create(cls, *, title: str = None, description: str = None, 
        url: str = None, color: int = None
    ):
        """Create an Embed object"""
        return Embed({
            "title": title,
            "description": description,
            "url": url,
            "color": color
        })

    def add_field(self, name: str, value: str, inline: bool = True):
        """Add a field object to the embed fields
        
        Arguments:
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

    def __make_image(self, url, proxy_url, height, width):
        return {
            "url": url,
            "proxy_url": proxy_url,
            "height": height,
            "width": width  
        }

    ##: Thumbnail
    @property
    def thumbnail(self):
        return self.__thumbnail

    def set_thumbnail(self, url: str, *, proxy_url: str = None, height: int = None, width: int = None):
        """Arguments:
            url (str): The URL for the thumbnail
            proxy_url (str): An alternative URL for the thumbnail
            height (int): The height of the thumbnail
            width (int): The width of the thumbnail
        """
        self.__thumbnail = self.__make_image(url, proxy_url, height, width)
    
    ##: Image
    @property
    def image(self):
        return self.__image

    def set_image(self, url, *, proxy_url: str = None, height: int = None, width: int = None):
        """Arguments:
            url (str): The URL for the image
            proxy_url (str): An alternative URL for the image
            height (int): The height of the image
            width (int): The width of the image
        """
        self.__image = self.__make_image(url, proxy_url, height, width)

    ##: Video
    @property
    def video(self):
        return self.__video

    def set_video(self, url, *, proxy_url: str = None, height: int = None, width: int = None):
        """Arguments:
            url (str): The URL for the video
            proxy_url (str): An alternative URL for the video
            height (int): The height of the video
            width (int): The width of the video
        """
        self.__video = self.__make_image(url, proxy_url, height, width)

    ##: Footer
    @property
    def footer(self):
        return self.__footer

    def set_footer(self, *, text: str, icon_url: str, proxy_url: str = None):
        """Arguments:
            text (str): The text for the footer
            icon_url (str): An URL for the footer
            proxy_url (str): An alternative URL for the footer
        """
        self.__footer = {
            "text": text,
            "icon_url": icon_url,
            "proxy_icon_url": proxy_url
        }

    ##: Author
    @property
    def author(self):
        """The author of the embed"""
        return self.__author

    def set_author(self, *, name: str, url: str, icon_url: str, proxy_url: str = None):
        """Arguments
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

    ##: Provider
    @property
    def provider(self):
        return self.__provider

    def set_provider(self, *, name: str = None, url: str = None):
        """Arguments
            name (str): The name of the provider
            url (str): The URL of the provider
        """
        self.__provider = {
            "name": name,
            "url": url
        }

    def to_dict(self):
        """Convert data to a valid dictionary"""
        return {
            "title": self.title,
            "type": self.embed_type,
            "description": self.description,
            "url": self.url,
            "timestamp": self.timestamp,
            "color": self.color,
            "fields": self.fields,
            "thumbnail": self.thumbnail,
            "image": self.image,
            "video": self.video,
            "footer": self.footer,
            "author": self.author,
            "provider": self.provider
        }

    def __repr__(self):
        return f"<pycordia.models.Embed - title='{self.title}' description={self.description}>"

