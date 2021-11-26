import asyncio
import json
import platform
from re import S
import zlib
import datetime

from pycordia.errors import GatewayError

import aiohttp
from aiohttp.client_ws import ClientWebSocketResponse
from aiohttp.http_websocket import WSMsgType

import pycordia

ZLIB_SUFFIX = b"\x00\x00\xff\xff"


class DiscordWebSocket:
    """A WebSockets client for the Discord Gateway API

    Attributes
        client: A related client
        bot_token (str): The bot_token used for the session
        intents (int): The intents used for the session

        gateway_url (str): The gateway URL used to communicate with Discord
        sock: A WebSocket session
        sequence: A sequence value, provided by Discord
        session_id: The ID for this session, provided by Discord

        heartbeat_interval: Interval between each heartbeat, in milliseconds
        last_heartbeat: The last recorded heartbeat sent to Discord
        latency: The time between the current time and the last heartbeat time, in milliseconds
    """

    opcodes = {
        "DISPATCH": 0,
        "HEARTBEAT": 1,
        "IDENTIFY": 2,
        "PRESENCE_UPDATE": 3,
        "VOICE_STATE_UPDATE": 4,
        "RESUME": 6,
        "RECONNECT": 7,
        "REQUEST_GUILD_MEMBERS": 8,
        "INVALID_SESSION": 9,
        "HELLO": 10,
        "HEARTBEAT_ACK": 11,
    }

    def __init__(self, client, bot_token, intents):
        self.client = client
        self.bot_token = bot_token
        self.intents = intents

        self.gateway_url = f"{pycordia.ws_url}/?v=9&encoding=json&compress=zlib-stream"

        self.sock = None
        self.sequence = None
        self.session_id = None

        self.heartbeat_interval = None
        self.last_heartbeat = None
        self.latency = None

        self.session = None 

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

    async def __keep_alive(self):
        """Keeps the connection alive by sending periodic heartbeats to the Discord gateway"""
        
        
        while self.sock:
            if self.heartbeat_interval:
                # Sleep for an interval in seconds
                await asyncio.sleep(self.heartbeat_interval / 1000)

                # Send heartbeat
                await self.__send_heartbeat(self.sock)

    async def __send_heartbeat(self, sock: ClientWebSocketResponse):
        """Sends a heartbeat to the provided websocket"""
        if not sock.closed:
            await sock.send_str(
                json.dumps({ "op": self.opcodes["HEARTBEAT"], "d": self.sequence })
            )
            self.last_heartbeat = datetime.datetime.now()

    async def __listen_socket(self):
        """Start listening for data from the gateway"""
        inflator = zlib.decompressobj()

        while self.sock:
            data = await self.sock.receive()
            payload = data.data

            # --- Handle close
            if data.type == WSMsgType.CLOSE:
                code, msg = data.data, data.extra
                
                await self.sock.close()
                #  A non-100(0|1) code indicates an error
                if code not in (1000, 1001):
                    raise GatewayError(code, msg)
        
            # --- Handle binary response
            elif data.type == WSMsgType.BINARY:
                #  Decompress the binary into readable JSON data
                buffer = bytearray()
                buffer.extend(data.data)
                #  We have to account for both payload and transport
                #  compression
                if buffer[-4:] == ZLIB_SUFFIX:
                    payload = inflator.decompress(buffer)
                else:
                    payload = zlib.decompress(buffer)


            if data.type in (WSMsgType.BINARY, WSMsgType.TEXT):
                payload_json = json.loads(payload)

                event_data = payload_json["d"]
                self.sequence = payload_json.get("s")

                # Send identify and set heartbeat
                if payload_json["op"] == self.opcodes["HELLO"]:
                    self.heartbeat_interval = event_data["heartbeat_interval"]

                    ident = self.get_identify()
                    await self.sock.send_json(ident)

                # Call event handlers
                elif payload_json["op"] == self.opcodes["DISPATCH"]:
                    if payload_json["t"] == "READY":
                        self.session_id = event_data["session_id"]

                    await self.client.call_event_handler(payload_json["t"], event_data)

                # Send heartbeat on request
                # elif payload_json["op"] == self.opcodes["HEARTBEAT"]:
                #     heartbeat.cancel()

                #     await self.__send_heartbeat(self.sock)  

                #     heartbeat = asyncio.create_task(self.__keep_alive())
                #     await asyncio.gather(heartbeat)

                # Maintain latency
                elif payload_json["op"] == self.opcodes["HEARTBEAT_ACK"]:
                    if self.last_heartbeat is not None:
                        self.latency = (
                            datetime.datetime.now() - self.last_heartbeat
                        ).total_seconds() * 1000

                # Reconnect
                elif payload_json["op"] == self.opcodes["RECONNECT"]:
                    await self.sock.close()
                    await self.start()

    async def start(self):
        """Start a WebSocket for connecting to Discord"""

        async with aiohttp.ClientSession() as session:
            self.sock = await session.ws_connect(self.gateway_url)

            await asyncio.gather(
                self.__listen_socket(),
                self.__keep_alive()
            )