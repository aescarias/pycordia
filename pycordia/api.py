import pycordia
import aiohttp

async def request(method: str, endpoint: str, *, json_data={}):
    client = pycordia.models.active_client
    if not client:
        raise Exception("No initialized client found.")
    
    async with aiohttp.ClientSession(headers={
        "Authorization": f"Bot {client.ws.bot_token}",
        "Accept": "application/json"
    }) as session:
        kws = { "json": json_data } if json_data else {}

        async with session.request(method, 
            f"{pycordia.api_url}/{endpoint}", **kws
        ) as resp:
            rs = await resp.json()
            
            if not resp.ok:
                raise pycordia.errors.QueryError(rs.get("code"), rs.get("message"))
            
            return rs