"""Configure a bridge and reauthenticate a revoked token from the UI."""
import voluptuous as vol
import ipaddress
import uuid
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers import selector
from .api import BridgeAPI, InvalidAuth, CannotConnect, validate_url
from .const import DOMAIN,CONF_URL,CONF_TOKEN
class ConfigFlow(config_entries.ConfigFlow,domain=DOMAIN):
    VERSION=1
    async def async_step_zeroconf(self,discovery_info):
        try:
            identity=str(uuid.UUID(discovery_info.properties['id']))
            if discovery_info.properties.get('api')!='1':raise ValueError()
            host=ipaddress.IPv4Address(str(getattr(discovery_info,'ip_address',None) or discovery_info.host))
            port=discovery_info.port
            if not host.is_private or host.is_loopback or host.is_multicast or host.is_unspecified or type(port) is not int or not 1<=port<=65535:raise ValueError()
        except (KeyError,ValueError,TypeError,AttributeError):return self.async_abort(reason='invalid_discovery')
        await self.async_set_unique_id(identity)
        # Discovery never redirects an already-configured client or its token.
        self._abort_if_unique_id_configured()
        self._discovered_url=f'http://{host}:{port}'
        self._discovered_id=identity
        return await self.async_step_zeroconf_confirm()
    async def async_step_zeroconf_confirm(self,user_input=None):
        errors={}
        if user_input:
            try:
                data=await BridgeAPI(async_get_clientsession(self.hass),self._discovered_url,user_input[CONF_TOKEN]).state()
                if data['id']!=self._discovered_id:errors['base']='wrong_bridge'
                else:return self.async_create_entry(title=data['name'],data={CONF_URL:self._discovered_url,CONF_TOKEN:user_input[CONF_TOKEN]})
            except InvalidAuth:errors['base']='invalid_auth'
            except CannotConnect:errors['base']='cannot_connect'
        return self.async_show_form(step_id='zeroconf_confirm',description_placeholders={'url':self._discovered_url},data_schema=vol.Schema({vol.Required(CONF_TOKEN):selector.TextSelector(selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD))}),errors=errors)

    async def async_step_user(self,user_input=None):
        errors={}
        if user_input is not None:
            try:
                url=validate_url(user_input[CONF_URL]);data=await BridgeAPI(async_get_clientsession(self.hass),url,user_input[CONF_TOKEN]).state()
                await self.async_set_unique_id(data['id']);self._abort_if_unique_id_configured()
                return self.async_create_entry(title=data['name'],data={CONF_URL:url,CONF_TOKEN:user_input[CONF_TOKEN]})
            except InvalidAuth:errors['base']='invalid_auth'
            except CannotConnect:errors['base']='cannot_connect'
            except ValueError:errors['base']='invalid_url'
        return self.async_show_form(step_id='user',data_schema=vol.Schema({vol.Required(CONF_URL,default='http://nanoleaf-hue.local'):str,vol.Required(CONF_TOKEN):selector.TextSelector(selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD))}),errors=errors)
    async def async_step_reauth(self,entry_data):return await self.async_step_reauth_confirm()
    async def async_step_reauth_confirm(self,user_input=None):
        entry=self._get_reauth_entry();errors={}
        if user_input:
            try:
                data=await BridgeAPI(async_get_clientsession(self.hass),entry.data[CONF_URL],user_input[CONF_TOKEN]).state()
                if data['id']!=entry.unique_id:errors['base']='wrong_bridge'
                else:return self.async_update_reload_and_abort(entry,data_updates={CONF_TOKEN:user_input[CONF_TOKEN]})
            except InvalidAuth:errors['base']='invalid_auth'
            except CannotConnect:errors['base']='cannot_connect'
        return self.async_show_form(step_id='reauth_confirm',data_schema=vol.Schema({vol.Required(CONF_TOKEN):selector.TextSelector(selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD))}),errors=errors)
    async def async_step_reconfigure(self,user_input=None):
        entry=self._get_reconfigure_entry();errors={}
        if user_input:
            try:
                url=validate_url(user_input[CONF_URL]);data=await BridgeAPI(async_get_clientsession(self.hass),url,user_input[CONF_TOKEN]).state()
                if data['id']!=entry.unique_id:errors['base']='wrong_bridge'
                else:return self.async_update_reload_and_abort(entry,data_updates={CONF_URL:url,CONF_TOKEN:user_input[CONF_TOKEN]})
            except InvalidAuth:errors['base']='invalid_auth'
            except CannotConnect:errors['base']='cannot_connect'
            except ValueError:errors['base']='invalid_url'
        return self.async_show_form(step_id='reconfigure',data_schema=vol.Schema({vol.Required(CONF_URL,default=entry.data[CONF_URL]):str,vol.Required(CONF_TOKEN):selector.TextSelector(selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD))}),errors=errors)
