import platform
import pycordia
import aiohttp
import json

from typing import Dict, List, Any, Optional


class HTTPClient:
    """The HTTP client used to manage a Discord HTTP connection
    
    Attributes:
        bot_token (str): The bot token used to connect
        boundary (str): The boundary used in multipart when sending files, \
            'boundary' by default.

        session (Optional[aiohttp.ClientSession]): An active HTTP session if any        
    """
    def __init__(self, bot_token: str, *, boundary: str = "boundary") -> None:
        self.bot_token = bot_token

        self.boundary = boundary

        self.session: Optional[aiohttp.ClientSession] = None

    async def login(self):
        """Setup an authenticated session"""

        # Assume reauthenticate
        if self.session:
            await self.session.close()     
        
        self.session = aiohttp.ClientSession(headers={
            "Authorization": f"Bot {self.bot_token}",
            "Accept": "application/json",
            "User-Agent": f"pycordia @ v{pycordia.__version__} on {platform.platform()}"
        })

    async def create_multipart(self, data: Any, files: List['pycordia.models.File']) -> bytes:
        """Create the multipart used when sending attachments through Discord
        
        Arguments:
            data (Any): Any valid JSON object, provided as `payload_json`
            files (List[pycordia.models.File]): The files to be sent in the message

        Returns:
            A bytes object containing the constructed multipart string
        """
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
        payload_json=None, 
        params: Dict[str, Any] = None,
        files: List['pycordia.models.File'] = None
    ) -> aiohttp.ClientResponse:
        """Perform a request to the Discord API and return its response

        Arguments:
            method (str): Any valid HTTP verb or method (GET, POST, ...)
            endpoint (str): A valid endpoint URI
        
        Keyword Arguments:
            payload_json (Any, optional): Any JSON-like object which is \
                provided to Discord in the request
            
            params (Dict[str, Any], optional): A mapping of URL query parameters
            files (List[pycordia.models.File], optional): \
                A list of files to provide in the request.

        Returns:
            An `aiohttp.ClientResponse` object once a response is received

        Raises:
            `pycordia.errors.HTTPError`: If the HTTP status code is above 400. 
            `pycordia.errors.ClientSetupError`: If no active session is found
        """
        if not payload_json:
            payload_json = {}
        if not params:
            params = {}

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
            # 204 No Content
            if resp.status == 204:
                # NOTE: Makeshift solution, might want to improve
                async def json(**kwargs):
                    return {}
                resp.json = json
                
                return resp

            rs = await resp.json()

            if not resp.ok:
                raise pycordia.errors.determine_error(resp.status, rs)
            
            return resp
