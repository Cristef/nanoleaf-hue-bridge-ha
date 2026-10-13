"""One shared local state poll for every bridge entity."""
from datetime import timedelta
from homeassistant.exceptions import ConfigEntryAuthFailed, HomeAssistantError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import logging
from .api import InvalidAuth, CannotConnect, CommandError
_LOGGER=logging.getLogger(__name__)
class BridgeCoordinator(DataUpdateCoordinator):
    def __init__(self,hass,entry,api):
        super().__init__(hass,_LOGGER,name="Nanoleaf Hue Bridge",config_entry=entry,update_interval=timedelta(seconds=5))
        self.api=api
    async def _async_update_data(self):
        try:return await self.api.state()
        except InvalidAuth as error:raise ConfigEntryAuthFailed('Automation token was revoked or is invalid') from error
        except CannotConnect as error:raise UpdateFailed('Bridge unavailable') from error
    async def command(self,name,value):
        try:self.async_set_updated_data(await self.api.command(name,value))
        except InvalidAuth as error:raise ConfigEntryAuthFailed('Automation token was revoked or is invalid') from error
        except (CannotConnect,CommandError) as error:raise HomeAssistantError('Bridge command failed; check connectivity and settings') from error
