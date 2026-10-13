from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from .entity import BridgeEntity
from .const import DOMAIN
async def async_setup_entry(hass,entry,async_add_entities):async_add_entities([StatusSensor(hass.data[DOMAIN][entry.entry_id])])
class StatusSensor(BridgeEntity,SensorEntity):
    _attr_device_class=SensorDeviceClass.ENUM
    _attr_options=['off','waiting','streaming','error','unavailable'];_attr_icon='mdi:information-outline'
    def __init__(self,coordinator):super().__init__(coordinator,'status','Stream status')
    @property
    def native_value(self):return self.coordinator.data['status']
