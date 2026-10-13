from homeassistant.components.binary_sensor import BinarySensorEntity
from .entity import BridgeEntity
from .const import DOMAIN
async def async_setup_entry(hass,entry,async_add_entities):async_add_entities([FramesSensor(hass.data[DOMAIN][entry.entry_id])])
class FramesSensor(BridgeEntity,BinarySensorEntity):
    _attr_icon='mdi:motion-play-outline'
    def __init__(self,coordinator):super().__init__(coordinator,'frames','Sync+ frames arriving')
    @property
    def is_on(self):return self.coordinator.data['syncFramesFresh']
