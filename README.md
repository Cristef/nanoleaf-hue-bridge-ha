# Nanoleaf Hue Bridge for Home Assistant

Experimental custom integration for the standalone [Nanoleaf Hue Bridge](https://github.com/Cristef/nanoleaf-hue-bridge). It controls the Debian bridge; it does not run Sync+ or Hue Entertainment inside Home Assistant.

## Requirements

- Home Assistant 2025.12 or newer.
- A bridge deployment with automation API v1 (introduced after bridge 4.1.0; **4.1.0 alone is not compatible**).
- Local network access from Home Assistant to the bridge on HTTP port 80 or 8080. VLAN routing/firewall rules must permit it.
- A dedicated automation token created in the bridge portal. No HomeKit code, Hue credentials or portal password is needed.

## Install with HACS

Add `https://github.com/Cristef/nanoleaf-hue-bridge-ha` as a **custom repository**, category **Integration**. Download, restart Home Assistant, then go to Settings → Devices & services → Add integration → Nanoleaf Hue Bridge.

This is not included in the default HACS catalogue.

For manual installation, copy `custom_components/nanoleaf_hue_bridge` to `/config/custom_components/nanoleaf_hue_bridge` and restart Home Assistant.

## Connect

In the bridge portal, open Setup → Home Assistant integration → Create token. Copy the token when displayed: it is never shown again. In Home Assistant enter the bridge URL (for example `http://nanoleaf-hue.local` or `http://BRIDGE_IP:8080`) and that token. On routed VLANs use the IP if mDNS does not resolve. No automatic discovery is implemented in 0.1.0.

## Entities

- **Synchronization** switch: enables/disables the virtual receiver. Enabled without incoming frames is normal.
- **Stream status**: Off, Waiting, Streaming, Error or Unavailable.
- **Profile** selector: applies an existing saved portal profile. It is unknown when current settings no longer match any saved profile; matching duplicates resolve to the first saved profile.
- **Global brightness** slider: 0–100%, preserving individual light brightness.
- **Sync+ frames arriving** binary sensor: recent frames, not proof of device connectivity.

State is polled once every five seconds for all entities. Commands update the shared state immediately. Stopping streaming releases Hue Entertainment; it does not restore a previous scene or turn the bulbs off. This integration does not duplicate your Hue lights or alter source placement/pairing.

Revoke tokens in the portal. Home Assistant will request reauthentication. Use Reconfigure to update the bridge address or token. Tokens are stored in Home Assistant's configuration: protect its backups. HTTP is unencrypted and intended only for a trusted LAN; do not forward these ports to the Internet. Tokens cannot administer accounts, pair devices, install updates or modify mappings.

## Validation status

Initial experimental version. Automated contract/security tests are provided; validation on a real Home Assistant OS deployment is still pending. Do not interpret a GitHub release as verified compatibility with every Home Assistant version.

## License

PolyForm Noncommercial 1.0.0. Commercial use is not granted. This is a community project, unaffiliated with Nanoleaf, Philips Hue or Home Assistant.
