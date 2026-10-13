import importlib,sys,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock
sys.path.insert(0,str(Path(__file__).parents[1]))
try:
 from custom_components.nanoleaf_hue_bridge.switch import SyncSwitch
 from custom_components.nanoleaf_hue_bridge.number import BrightnessNumber
 from custom_components.nanoleaf_hue_bridge.select import ProfileSelect
 from custom_components.nanoleaf_hue_bridge.sensor import StatusSensor
 from custom_components.nanoleaf_hue_bridge.binary_sensor import FramesSensor
 AVAILABLE=True
except ModuleNotFoundError:AVAILABLE=False
@unittest.skipUnless(AVAILABLE,'Home Assistant runtime is installed in the runtime CI job')
class EntityTests(unittest.IsolatedAsyncioTestCase):
 async def test_entities_and_commands(self):
  c=SimpleNamespace(data={'id':'stable','version':'test','enabled':True,'reachable':True,'brightness':70,'profiles':['Cinema'],'profile':'Cinema','status':'streaming','syncFramesFresh':True},api=SimpleNamespace(url='http://host'),last_update_success=True,command=AsyncMock())
  switch=SyncSwitch(c);number=BrightnessNumber(c);select=ProfileSelect(c);status=StatusSensor(c);frames=FramesSensor(c)
  self.assertTrue(switch.is_on);self.assertTrue(switch.available);self.assertEqual(number.native_value,70);self.assertEqual(select.current_option,'Cinema');self.assertEqual(status.native_value,'streaming');self.assertTrue(frames.is_on)
  await switch.async_turn_off();c.command.assert_awaited_with('sync',False)
  await number.async_set_native_value(55);c.command.assert_awaited_with('brightness',55)
  await select.async_select_option('Cinema');c.command.assert_awaited_with('profile','Cinema')
  c.data['reachable']=False;self.assertFalse(switch.available)
 async def test_modules_import_and_reauthentication_steps_exist(self):
  module=importlib.import_module('custom_components.nanoleaf_hue_bridge.config_flow')
  self.assertTrue(hasattr(module.ConfigFlow,'async_step_reauth_confirm'));self.assertTrue(hasattr(module.ConfigFlow,'async_step_reconfigure'))

@unittest.skipUnless(AVAILABLE,'Home Assistant runtime required')
class DiagnosticsTests(unittest.IsolatedAsyncioTestCase):
 async def test_allowlisted_diagnostics_remove_token_url_and_names(self):
  module=importlib.import_module('custom_components.nanoleaf_hue_bridge.diagnostics')
  result=module.safe_diagnostics({'apiVersion':1,'version':'test','status':'off','token':'secret','id':'private','url':'http://private','profiles':['private room'],'profile':'private room','diagnostics':{'lightCount':2,'token':'secret','hueFrames':8}})
  self.assertNotIn('secret',str(result));self.assertNotIn('private',str(result));self.assertEqual(result['stream']['lightCount'],2)
 async def test_invalid_discovery_rejected_without_authentication(self):
  module=importlib.import_module('custom_components.nanoleaf_hue_bridge.config_flow');flow=module.ConfigFlow()
  result=await flow.async_step_zeroconf(SimpleNamespace(properties={'id':'not-a-uuid','api':'1'},host='10.0.0.1',port=8080))
  self.assertEqual(result['reason'],'invalid_discovery')
