import importlib.util,unittest
from pathlib import Path
from types import SimpleNamespace
spec=importlib.util.spec_from_file_location('discovery',Path(__file__).parents[1]/'custom_components/nanoleaf_hue_bridge/discovery.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class DiscoveryTests(unittest.TestCase):
 def test_selects_private_ipv4_and_validates_identity(self):
  identity='11111111-1111-4111-8111-111111111111'
  info=SimpleNamespace(properties={'id':identity,'api':'1'},ip_address='fd00::1',host='fd00::1',ip_addresses=['fd00::1','10.23.45.20'],port=8080)
  self.assertEqual(module.discovered_bridge(info),(identity,'http://10.23.45.20:8080'))
 def test_rejects_public_address_unknown_api_and_invalid_port(self):
  for host,version,port in [('8.8.8.8','1',8080),('10.0.0.1','2',8080),('10.0.0.1','1',True)]:
   info=SimpleNamespace(properties={'id':'11111111-1111-4111-8111-111111111111','api':version},host=host,port=port)
   with self.assertRaises(ValueError):module.discovered_bridge(info)
