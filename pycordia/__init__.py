"""
Pycordia - The Discord bot framework
------------------------------------

Developed by Angel Carias and its contributors. 2021.

A wrapper around the Discord HTTP API and WebSockets
"""

from .client import Intents, Client
from . import websocket, errors, events, models, api

__version__ = "0.2.1"

cdn_url = "https://cdn.discordapp.com"
ws_url = "wss://gateway.discord.gg"
api_url = "https://discord.com/api/v9"
