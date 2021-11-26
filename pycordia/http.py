import pycordia
import aiohttp
import json

from typing import Dict, List, Any


class HTTPClient:
    def __init__(self, bot_token: str, *, boundary: str = "boundary") -> None:
        self.bot_token = bot_token

        self.boundary = boundary

        self.session = None

    async def login(self):
        """Setup an authenticated session"""
        self.session = aiohttp.ClientSession(headers={
            "Authorization": f"Bot {self.bot_token}",
            "Accept": "application/json"
        })

    async def create_multipart(self, data, files: List['pycordia.models.File']) -> bytes:
        multipart = (f'--{self.boundary}\n' \
                      'Content-Disposition: form-data; name="payload_json"\n' \
                      'Content-Type: application/json\n\n' \
                     f'{json.dumps(data, indent=4)}\n').encode("utf-8")

        for i, fl in enumerate(files):
            multipart += (f'--{self.boundary}\n' \
                          f'Content-Disposition: form-data; name="files[{i}]"; filename="{fl.filename}"\n' \
                           'Content-Type: application/octet-stream\n\n').encode("utf-8") + fl.fp.read() + b"\n"
        multipart += f"--{self.boundary}--".encode("utf-8")

        return multipart

    async def request(
        self, method: str, endpoint: str, *,
        payload_json={}, 
        params: Dict[str, Any] = {},
        files: List['pycordia.models.File'] = None
    ) -> aiohttp.ClientResponse:
        """Perform a request to the Discord API"""

        if not self.session:
            raise pycordia.errors.ClientSetupError("No HTTP client session found.")

        param_list = []
        if params:
            for name, value in params.items():
                if value is None:
                    continue

                param_list.append(f"{name}={value}")

            if param_list:
                endpoint = f"{endpoint}?{'&'.join(param_list)}"

        if files:
            multipart = await self.create_multipart(payload_json, files)
            content_type = f'multipart/form-data; boundary="{self.boundary}"'

            kws = { "data": multipart }
        else:
            multipart = ""
            content_type = "application/json"
            kws = { "json": payload_json } if payload_json else {}

        async with self.session.request(
            method, f"{pycordia.api_url}/{endpoint}", 
            **kws, headers={ "Content-Type": content_type }
        ) as resp:
            rs = await resp.json()

            if not resp.ok:
                raise pycordia.errors.determine_error(resp.status, rs)
            
            return resp

    

# async def request(
#     method: str, endpoint: str, *, 
#     json_data={}, 
#     files: List['pycordia.models.File'] = None
# ):
#     client = pycordia.models.active_client
#     boundary = "boundary"
#     if not client:
#         raise pycordia.errors.ClientSetupError("No initialized client found.")

    
#     if files:
#         multipart = (f'--{boundary}\n' \
#                       'Content-Disposition: form-data; name="payload_json"\n' \
#                       'Content-Type: application/json\n\n' \
#                      f'{json.dumps(json_data, indent=4)}\n').encode("utf-8")

#         for i, fl in enumerate(files):
#             multipart += (f'--{boundary}\n' \
#                           f'Content-Disposition: form-data; name="files[{i}]"; filename="{fl.filename}"\n' \
#                            'Content-Type: application/octet-stream\n\n').encode("utf-8") + fl.fp.read() + b"\n"
#         multipart += f"--{boundary}--".encode("utf-8")
#         content_type = f'multipart/form-data; boundary="{boundary}"'
#     else:
#         multipart = ""
#         content_type = "application/json"
    
#     async with aiohttp.ClientSession(headers={
#         "Authorization": f"Bot {client.ws.bot_token}",
#         "Accept": "application/json",
#         "Content-Type": content_type
#     }) as session:
#         if files:
#             kws = { "data": multipart }
#         else:
#             kws = { "json": json_data } if json_data else {}
        
#         async with session.request(method, 
#             f"{pycordia.api_url}/{endpoint}", **kws
#         ) as resp:
#             rs = await resp.json()
            
#             if not resp.ok:
#                 raise pycordia.errors.QueryError(rs.get("code"), rs.get("message"))
            
#             return rs
