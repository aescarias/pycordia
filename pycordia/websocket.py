# Pycordia v0.1.0 - The Discord bot framework
# Developed by Angel Carias and it's contributors. 2021.

# websocket.py
#   Handles communication with the Discord Gateway API


import asyncio
import json
import platform
from pycordia.errors import GatewayError

import aiohttp
from aiohttp.client_ws import ClientWebSocketResponse
from aiohttp.http_websocket import WSMsgType

import pycordia


class DiscordWebSocket:
    """A WebSockets client for the Discord Gateway API"""

    opcodes = {
        "DISPATCH": 0,
        "HEARTBEAT": 1,
        "IDENTIFY": 2,
        "PRESENCE_UPDATE": 3,
        "VOICE_STATE_UPDATE": 4,
        "RESUME": 6,
        "RECONNECT": 7,
        "REQUEST_GUILD_MEMBERS": 8,
        "INVALID_SESION": 9,
        "HELLO": 10,
        "HEARTBEAT_ACK": 11,
    }

    def __init__(self, client, bot_token, intents):
        self.bot_token = bot_token
        """A valid Discord bot token"""

        self.heartbeat_interval = None
        """The interval to wait before calling the gateway again, in milliseconds"""
        self.sequence = None
        self.gateway_url = f"{pycordia.ws_url}/?v=9&encoding=json"
        self.client = client

        self.session_id = None
        self.intents = intents

    def get_identify(self):
        return {
            "op": self.opcodes["IDENTIFY"],
            "d": {
                "token": self.bot_token,
                "properties": {
                    "$os": platform.system(),
                    "$browser": "pycordia",
                    "$device": "pycordia",
                },
                "compress": False,
                "large_threshold": 250,
                "intents": self.intents,
            },
        }

    async def __keep_alive(self, sock: ClientWebSocketResponse):
        """Keeps the connection alive by sending periodic heartbeats to the Discord gateway"""
        while True:
            if self.heartbeat_interval:
                await asyncio.sleep(self.heartbeat_interval / 1000)

                # Send heartbeat
                await sock.send_str(
                    json.dumps({"op": self.opcodes["HEARTBEAT"], "d": self.sequence})
                )

    async def __listen_socket(self, sock: ClientWebSocketResponse):
        """Start listening for websocket data"""
        while True:
            data = await sock.receive()

            if data.type == WSMsgType.CLOSE:
                code, msg = data.data, data.extra
                await sock.close(code=1001)
                raise GatewayError(code, msg)
            elif data.type == WSMsgType.TEXT:
                js = data.json()
                event_data = js["d"]

                self.sequence = js.get("s")

                if js["op"] == self.opcodes["HELLO"]:
                    self.heartbeat_interval = event_data["heartbeat_interval"]
                    ident = self.get_identify()
                    await sock.send_json(ident)
                elif js["op"] == self.opcodes["DISPATCH"]:
                    if js["t"] == "READY":
                        self.session_id = event_data["session_id"]

                    await self.client.call_event_handler(js["t"], event_data)

    async def listen(self):
        async with aiohttp.ClientSession() as session:
            sock = await session.ws_connect(self.gateway_url)

            await asyncio.gather(
                asyncio.create_task(self.__listen_socket(sock)),
                asyncio.create_task(self.__keep_alive(sock)),
            )
