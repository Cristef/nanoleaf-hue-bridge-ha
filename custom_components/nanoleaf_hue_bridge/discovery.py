"""Validate DNS-SD metadata without transmitting an API token."""
import ipaddress
import uuid

def discovered_bridge(info):
    identity=str(uuid.UUID(info.properties['id']))
    if info.properties.get('api')!='1':raise ValueError('Unsupported API')
    candidates=[getattr(info,'ip_address',None),getattr(info,'host',None),*getattr(info,'ip_addresses',[])]
    host=None
    for candidate in candidates:
        try:address=ipaddress.IPv4Address(str(candidate))
        except ValueError:continue
        if address.is_private and not address.is_loopback and not address.is_multicast and not address.is_unspecified and not address.is_link_local:
            host=address;break
    port=info.port
    if host is None or type(port) is not int or not 1<=port<=65535:raise ValueError('Unsupported address')
    return identity,f'http://{host}:{port}'
