import asyncio
import json
import platform
import zlib
from pycordia.errors import GatewayError

import aiohttp
from aiohttp.client_ws import ClientWebSocketResponse
from aiohttp.http_websocket import WSMsgType

import pycordia

ZLIB_SUFFIX = b"\x00\x00\xff\xff"


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

        self.sock = None

        self.heartbeat_interval = None
        """The interval to wait before calling the gateway again, in milliseconds"""
        self.sequence = None
        self.gateway_url = f"{pycordia.ws_url}/?v=9&encoding=json&compress=zlib-stream"
        self.client = client

        self.session_id = None
        self.intents = intents
        """The provided intents as an integer"""


    def get_identify(self):
        """Returns an Opcode 2 (Identify) response"""
        return {
            "op": self.opcodes["IDENTIFY"],
            "d": {
                "token": self.bot_token,
                "properties": {
                    "$os": platform.system(),
                    "$browser": "pycordia",
                    "$device": "pycordia",
                },
                "compress": True,
                "large_threshold": 250,
                "intents": self.intents,
            },
        }

    async def __keep_alive(self, sock: ClientWebSocketResponse):
        """Keeps the connection alive by sending periodic heartbeats to the Discord gateway"""
        while True:
            if self.heartbeat_interval:
                # Sleep for an interval in seconds
                await asyncio.sleep(self.heartbeat_interval / 1000)

                # Send heartbeat
                await sock.send_str(
                    json.dumps({ "op": self.opcodes["HEARTBEAT"], "d": self.sequence })
                )

    async def __listen_socket(self, sock: ClientWebSocketResponse):
        """Start listening for data from the gateway"""
        self.sock = sock
        inflator = zlib.decompressobj()

        while True:
            data = await sock.receive()
            payload = data.data

            # --- Handle close --- #
            if data.type == WSMsgType.CLOSE:
                code, msg = data.data, data.extra
                await sock.close()
                #  A non-100(0|1) code indicates an error
                if code not in (1000, 1001):
                    raise GatewayError(code, msg)
            # --- Handle binary response --- #
            elif data.type == WSMsgType.BINARY:
                # Decompress the binary into readable JSON data
                buffer = bytearray()
                buffer.extend(data.data)
                # We have to account for both payload and transport
                # compression
                if buffer[-4:] == ZLIB_SUFFIX:
                    payload = inflator.decompress(buffer)
                else:
                    payload = zlib.decompress(buffer)

            if data.type in (WSMsgType.BINARY, WSMsgType.TEXT):
                js = json.loads(payload)
                event_data = js["d"]

                self.sequence = js.get("s")

                # Send identify
                if js["op"] == self.opcodes["HELLO"]:
                    self.heartbeat_interval = event_data["heartbeat_interval"]
                    ident = self.get_identify()
                    await sock.send_json(ident)
                # Call event handlers
                elif js["op"] == self.opcodes["DISPATCH"]:
                    if js["t"] == "READY":
                        self.session_id = event_data["session_id"]

                    await self.client.call_event_handler(js["t"], event_data)

    async def listen(self):
        """Manage a separate connection for both heartbeats and websocket events"""
        async with aiohttp.ClientSession() as session:
            sock = await session.ws_connect(self.gateway_url)

            await asyncio.gather(
                asyncio.create_task(self.__listen_socket(sock)),
                asyncio.create_task(self.__keep_alive(sock)),
            )