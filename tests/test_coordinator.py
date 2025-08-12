import sys
import types
from pathlib import Path
import asyncio
import pytest

# Stub Home Assistant modules
ha_core = types.ModuleType("core")

class DummyHass:
    async def async_add_executor_job(self, func, *args):
        return func(*args)

ha_core.HomeAssistant = DummyHass
sys.modules["homeassistant.core"] = ha_core

ha_helpers = types.ModuleType("helpers")
update_coordinator = types.ModuleType("update_coordinator")

class DataUpdateCoordinator:
    def __init__(self, hass, logger, *, name, update_interval, config_entry=None):
        self.hass = hass
        self.logger = logger
        self.name = name
        self.update_interval = update_interval
        self.config_entry = config_entry

    def __class_getitem__(cls, item):
        return cls

class UpdateFailed(Exception):
    pass

update_coordinator.DataUpdateCoordinator = DataUpdateCoordinator
update_coordinator.UpdateFailed = UpdateFailed
ha_helpers.update_coordinator = update_coordinator
sys.modules["homeassistant.helpers"] = ha_helpers
sys.modules["homeassistant.helpers.update_coordinator"] = update_coordinator

# Ensure custom component can be imported
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from custom_components.nextbus.coordinator import NextBusDataUpdateCoordinator
from custom_components.nextbus.util import RouteStop


class DummyClient:
    rate_limit_percent = 0
    rate_limit_reset = None

    def predictions_for_stop(self, stop_id):
        return [
            {"route": {"id": "312", "title": "312"}, "stop": {"id": "14669", "name": "Stop"}, "values": []},
            {
                "route": {"id": "512", "title": "512"},
                "stop": {"id": "14669", "name": "Stop"},
                "values": [{"timestamp": 1, "seconds": 60, "minutes": 1}],
            },
        ]


def test_predictions_returned_when_stop_id_differs():
    hass = DummyHass()
    coordinator = NextBusDataUpdateCoordinator(hass, "ttc")
    coordinator.client = DummyClient()
    coordinator.add_stop_route("14934", "512")

    async def mock_resolve(route_id, stop_id):
        return stop_id

    coordinator._async_resolve_api_stop_id = mock_resolve

    data = asyncio.run(coordinator._async_update_data())
    result = data[RouteStop("512", "14934")]
    assert result["values"][0]["minutes"] == 1
