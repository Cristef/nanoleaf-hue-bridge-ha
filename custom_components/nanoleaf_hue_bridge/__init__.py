"""Home Assistant control for the standalone Nanoleaf Hue Bridge."""
from homeassistant.const import Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .api import BridgeAPI
from .const import DOMAIN, CONF_URL, CONF_TOKEN
from .coordinator import BridgeCoordinator
PLATFORMS=[Platform.SWITCH,Platform.SENSOR,Platform.BINARY_SENSOR,Platform.SELECT,Platform.NUMBER]
async def async_setup_entry(hass,entry):
    coordinator=BridgeCoordinator(hass,entry,BridgeAPI(async_get_clientsession(hass),entry.data[CONF_URL],entry.data[CONF_TOKEN]))
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN,{})[entry.entry_id]=coordinator
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    await hass.config_entries.async_forward_entry_setups(entry,PLATFORMS)
    return True
async def async_unload_entry(hass,entry):
    unloaded=await hass.config_entries.async_unload_platforms(entry,PLATFORMS)
    if unloaded:hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded
async def async_reload_entry(hass,entry):await hass.config_entries.async_reload(entry.entry_id)
