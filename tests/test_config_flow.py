import sys
import types
from pathlib import Path


package = types.ModuleType("nextbus")
package.__path__ = [
    str(Path(__file__).resolve().parents[1] / "custom_components" / "nextbus")
]
sys.modules["nextbus"] = package

ha_config_entries = types.ModuleType("config_entries")


class DummyConfigFlow:
    def __init_subclass__(cls, **kwargs):
        pass


ha_config_entries.ConfigFlow = DummyConfigFlow
ha_config_entries.ConfigFlowResult = object
ha_config_entries.ConfigEntry = object
sys.modules["homeassistant.config_entries"] = ha_config_entries

ha_const = types.ModuleType("const")
ha_const.CONF_STOP = "stop"
ha_const.Platform = types.SimpleNamespace(SENSOR="sensor")
sys.modules["homeassistant.const"] = ha_const

ha_selector = types.ModuleType("selector")


class Dummy:
    pass


ha_selector.SelectOptionDict = Dummy
ha_selector.SelectSelector = Dummy
ha_selector.SelectSelectorConfig = Dummy
ha_selector.SelectSelectorMode = Dummy
sys.modules["homeassistant.helpers.selector"] = ha_selector

ha_core = types.ModuleType("core")
ha_core.HomeAssistant = object
sys.modules["homeassistant.core"] = ha_core

ha_exceptions = types.ModuleType("exceptions")
ha_exceptions.ConfigEntryNotReady = type("ConfigEntryNotReady", (Exception,), {})
sys.modules["homeassistant.exceptions"] = ha_exceptions

requests = types.ModuleType("requests")


class DummySession:
    def get(self, *args, **kwargs):
        raise RuntimeError


requests.Session = DummySession
requests.HTTPError = Exception
requests.RequestException = Exception
sys.modules["requests"] = requests

vol = types.ModuleType("voluptuous")
vol.Schema = type("Schema", (), {})
vol.Required = lambda x: x
vol.Optional = lambda x, default=None: x
sys.modules["voluptuous"] = vol

from nextbus.config_flow import _get_stop_tags  # noqa: E402


class DummyClient:
    def route_details(self, route_tag, agency_tag):
        return {
            "stops": [
                {"id": "t1", "stopId": "s1", "name": "Main St"},
                {"id": "t2", "stopId": "s2", "name": "Main St"},
                {"id": "t3", "stopId": "s3", "name": "Third St"},
            ],
            "directions": [
                {
                    "name": "North",
                    "useForUi": True,
                    "stops": [{"id": "t1"}, {"id": "t2"}],
                },
                {
                    "name": "South",
                    "useForUi": True,
                    "stops": [{"id": "t3"}],
                },
            ],
        }


def test_get_stop_tags_handles_dict_stop_entries():
    tags = _get_stop_tags(DummyClient(), "agency", "route")
    assert tags == {
        "s1": "Main St (North)",
        "s2": "Main St (North)",
        "s3": "Third St",
    }
