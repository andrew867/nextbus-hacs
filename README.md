# NextBus HACS Integration

Custom [Home Assistant](https://www.home-assistant.io/) integration for fetching NextBus arrival predictions.

This project packages the core [`nextbus` integration](https://github.com/home-assistant/core/tree/2025.8.0/homeassistant/components/nextbus) as a [HACS](https://hacs.xyz/) custom component so it can be easily modified and fixed outside of Home Assistant core.

## Installation

1. Ensure [HACS](https://hacs.xyz/docs/setup/download) is installed.
2. Add this repository as a custom integration repository in HACS.
3. Install the **NextBus integration** from HACS.
4. Restart Home Assistant.

## Configuration

Use the Home Assistant UI to configure the integration via **Settings → Devices & services → Add integration** and search for "NextBus".

When adding the integration you can optionally enable **debug logging**. This will increase the verbosity of the integration's logs which can be helpful when troubleshooting.

This repository also includes a basic Lovelace card. After installing the integration copy the resource `/hacsfiles/next-bus-card.js` into your dashboard resources and use the `next-bus-card` type in your views to display upcoming departures.

## License

Distributed under the MIT License. See `LICENSE` for more information.
