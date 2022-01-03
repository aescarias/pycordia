import pycordia

from .embed import Embed
from .message import (
    Message, Attachment, Application, 
    File, Interaction, MessageReference, 
    Reaction, MessageActivity
)
from .guild import (
    Guild, Emoji, Role, Member, PartialGuild
)
from .channel import (
    Channel, ChannelMention
)
from .user import (
    Connection, User
)
from .webhook import Webhook

active_client: 'pycordia.client.Client | None' = None

def fetch_client():
    """Helper function to fetch the currently active client
    
    Raises:
        A ClientSetupError if no client was found
    """
    if active_client:
        return active_client
    raise pycordia.errors.ClientSetupError