from homeassistant.components.select import SelectEntity
from .entity import BridgeEntity
from .const import DOMAIN
async def async_setup_entry(hass,entry,async_add_entities):async_add_entities([ProfileSelect(hass.data[DOMAIN][entry.entry_id])])
class ProfileSelect(BridgeEntity,SelectEntity):
    _attr_icon='mdi:palette'
    def __init__(self,coordinator):super().__init__(coordinator,'profile','Profile')
    @property
    def options(self):return self.coordinator.data['profiles']
    @property
    def current_option(self):return self.coordinator.data['profile']
    async def async_select_option(self,option):await self.coordinator.command('profile',option)
