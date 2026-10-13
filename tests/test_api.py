import asyncio,importlib.util,json,unittest
from pathlib import Path
from aiohttp import web,ClientSession
spec=importlib.util.spec_from_file_location('bridge_api',Path(__file__).parents[1]/'custom_components/nanoleaf_hue_bridge/api.py')
api=importlib.util.module_from_spec(spec);spec.loader.exec_module(api)
class APITests(unittest.IsolatedAsyncioTestCase):
 async def asyncSetUp(self):
  self.status=200;self.headers=[]
  async def handler(request):
   self.headers.append(request.headers.get('Authorization'))
   if self.status!=200:return web.json_response({'secret':'never displayed'},status=self.status)
   return web.json_response({'apiVersion':1,'id':'stable-id','name':'Bridge'})
  app=web.Application();app.router.add_route('*','/{path:.*}',handler);self.runner=web.AppRunner(app);await self.runner.setup();self.site=web.TCPSite(self.runner,'127.0.0.1',0);await self.site.start()
  port=self.site._server.sockets[0].getsockname()[1];self.session=ClientSession();self.client=api.BridgeAPI(self.session,f'http://127.0.0.1:{port}','test-token')
 async def asyncTearDown(self):await self.session.close();await self.runner.cleanup()
 async def test_state_and_command_use_bearer(self):
  self.assertEqual((await self.client.state())['id'],'stable-id');await self.client.command('sync',True);self.assertEqual(self.headers,['Bearer test-token']*2)
 async def test_revoked_auth_and_busy(self):
  self.status=401
  with self.assertRaises(api.InvalidAuth):await self.client.state()
  self.status=409
  with self.assertRaises(api.CommandError):await self.client.command('brightness',50)
  self.status=503
  with self.assertRaises(api.CannotConnect):await self.client.state()
 def test_reject_credentials_paths_https(self):
  for url in ('https://host','http://user:pass@host','http://host/private','http://host?token=x'):
   with self.assertRaises(ValueError):api.validate_url(url)
