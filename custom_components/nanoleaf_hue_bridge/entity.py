from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from .const import DOMAIN
class BridgeEntity(CoordinatorEntity):
    _attr_has_entity_name=True
    def __init__(self,coordinator,key,name):
        super().__init__(coordinator)
        self._attr_unique_id=coordinator.data['id']+'_'+key
        self._attr_name=name
        self._attr_device_info=DeviceInfo(identifiers={(DOMAIN,coordinator.data['id'])},name='Nanoleaf Hue Bridge',manufacturer='Cristef',model='Virtual Sync+ bridge',sw_version=coordinator.data['version'],configuration_url=coordinator.api.url)
