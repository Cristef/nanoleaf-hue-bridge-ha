"""Allowlisted diagnostics: no tokens, addresses, identifiers or profile names."""
from .const import DOMAIN

def safe_diagnostics(data):
    result={key:data.get(key) for key in ('apiVersion','version','enabled','reachable','status','syncFramesFresh','brightness','frameAge')}
    extra=data.get('diagnostics',{})
    result['stream']={key:extra.get(key) for key in ('lightCount','panelCount','hueFrames','apiPaired')}
    result['profileCount']=len(data.get('profiles',[]))
    return result

async def async_get_config_entry_diagnostics(hass,entry):
    coordinator=hass.data[DOMAIN][entry.entry_id]
    return {'integration':'nanoleaf_hue_bridge','state':safe_diagnostics(coordinator.data),
        'pollingSeconds':5,'lastUpdateSucceeded':coordinator.last_update_success}
