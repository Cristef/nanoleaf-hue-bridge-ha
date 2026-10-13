from homeassistant.components.number import NumberEntity, NumberMode
from .entity import BridgeEntity
from .const import DOMAIN
async def async_setup_entry(hass,entry,async_add_entities):async_add_entities([BrightnessNumber(hass.data[DOMAIN][entry.entry_id])])
class BrightnessNumber(BridgeEntity,NumberEntity):
    _attr_native_min_value=0;_attr_native_max_value=100;_attr_native_step=1
    _attr_native_unit_of_measurement='%';_attr_mode=NumberMode.SLIDER;_attr_icon='mdi:brightness-6'
    def __init__(self,coordinator):super().__init__(coordinator,'brightness','Global brightness')
    @property
    def native_value(self):return self.coordinator.data['brightness']
    async def async_set_native_value(self,value):await self.coordinator.command('brightness',int(value))
