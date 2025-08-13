# NextBus HACS Integration

![GitHub Release](https://img.shields.io/github/v/release/andrew867/nextbus-hacs?style=flat-square)
![License](https://img.shields.io/github/license/andrew867/nextbus-hacs?style=flat-square)

Custom [Home Assistant](https://www.home-assistant.io/) integration for fetching [NextBus](https://www.nextbus.com/) arrival predictions.  This repository mirrors the upstream [`nextbus` integration](https://github.com/home-assistant/core/tree/2025.8.0/homeassistant/components/nextbus) so it can be developed and fixed outside of Home Assistant core.

---

## Features

- Fetches live predictions from the NextBus public API
- Simple configuration via the Home Assistant UI
- Optional Lovelace card for displaying upcoming departures
- Fully tested with `pytest`

## Installation

### Via [HACS](https://hacs.xyz/)
1. Make sure HACS is installed and working in your Home Assistant instance.
2. In HACS, add this repository as a **Custom Repository** (integration category).
3. Install the **NextBus** integration from the list.
4. Restart Home Assistant.

### Manual
1. Copy the `custom_components/nextbus` folder to `<config>/custom_components/nextbus` in your Home Assistant configuration directory.
2. (Optional) Copy `next-bus-card.js` into `<config>/www` and add it as a resource to your dashboard.
3. Restart Home Assistant.

## Configuration

1. Navigate to **Settings → Devices & services** in Home Assistant.
2. Click **Add Integration** and search for **NextBus**.
3. Enter the agency and stop information when prompted.
4. Save to create the entity.

### Lovelace Card
After copying `next-bus-card.js` into your dashboard resources, create a card using the `next-bus-card` type:

```yaml
type: custom:next-bus-card
entity: sensor.my_bus_stop
```

## Debugging

Enable debug logging either during configuration or through `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.nextbus: debug
```

Logs can then be viewed via **Settings → System → Logs** or the Home Assistant log file.

## Development

### Requirements
- Python 3.11+
- `requests`, `pytest`, `flake8`, `black`

### Setup

```bash
./setup.sh
source .venv/bin/activate
```

### Running Tests

```bash
pytest
```

### Code Style

Format code with `black` and ensure linting passes with `flake8` before committing.

## Contributing

Issues and pull requests are welcome. If proposing a new feature, please open an issue first to discuss your idea.

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
