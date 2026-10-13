"""Local bridge API. Never log tokens or arbitrary server response bodies."""
import asyncio
from urllib.parse import urlsplit
import aiohttp
class InvalidAuth(Exception):pass
class CannotConnect(Exception):pass
class CommandError(Exception):pass

def validate_url(value):
    parts=urlsplit(value)
    if parts.scheme!='http' or not parts.hostname or parts.username or parts.password or parts.query or parts.fragment or parts.path not in ('','/'):
        raise ValueError('Use http://HOST[:PORT] without credentials or a path')
    if parts.port is not None and not 1<=parts.port<=65535:raise ValueError('Invalid port')
    return value.rstrip('/')

class BridgeAPI:
    def __init__(self,session,url,token):
        self.session=session;self.url=validate_url(url);self.token=token
    async def request(self,method,path,payload=None):
        try:
            async with asyncio.timeout(10):
                async with self.session.request(method,self.url+'/api/integration/v1/'+path,json=payload,
                    headers={'Authorization':'Bearer '+self.token},allow_redirects=False) as response:
                    if response.status in (401,403):raise InvalidAuth()
                    if response.status in (400,409):raise CommandError()
                    if response.status!=200:raise CannotConnect()
                    data=await response.json()
                    if not isinstance(data,dict) or data.get('apiVersion')!=1 or not isinstance(data.get('id'),str):raise CannotConnect()
                    return data
        except (aiohttp.ClientError,TimeoutError,ValueError) as error:raise CannotConnect() from error
    async def state(self):return await self.request('GET','state')
    async def command(self,command,value):return await self.request('POST','command',{'command':command,'value':value})
