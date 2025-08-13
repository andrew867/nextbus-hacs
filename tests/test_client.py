import importlib.util
from pathlib import Path

import pytest
import requests

spec = importlib.util.spec_from_file_location(
    "nextbus_client",
    Path(__file__).resolve().parents[1]
    / "custom_components"
    / "nextbus"
    / "nextbus_client.py",
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
NextBusClient = module.NextBusClient
NextBusHTTPError = module.NextBusHTTPError


def test_get_handles_request_exception(monkeypatch):
    client = NextBusClient()

    def raise_exc(*args, **kwargs):
        raise requests.RequestException

    client._session.get = raise_exc

    with pytest.raises(NextBusHTTPError):
        client._get({"command": "agencyList"})
