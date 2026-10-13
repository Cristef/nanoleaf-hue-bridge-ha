from homeassistant.components.switch import SwitchEntity
from .entity import BridgeEntity
from .const import DOMAIN
async def async_setup_entry(hass,entry,async_add_entities):async_add_entities([SyncSwitch(hass.data[DOMAIN][entry.entry_id])])
class SyncSwitch(BridgeEntity,SwitchEntity):
    _attr_icon='mdi:sync'
    def __init__(self,coordinator):super().__init__(coordinator,'sync','Synchronization')
    @property
    def is_on(self):return self.coordinator.data['enabled']
    @property
    def available(self):return super().available and self.coordinator.data['reachable']
    async def async_turn_on(self,**kwargs):await self.coordinator.command('sync',True)
    async def async_turn_off(self,**kwargs):await self.coordinator.command('sync',False)
