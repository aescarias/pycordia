"""
### PyCordia - The Discord bot framework

Developed by Angel Carias and it's contributors. 2021.

A wrapper around the Discord HTTP API and WebSockets
"""

from .client import Intents, Client
from . import websocket, errors, events, models