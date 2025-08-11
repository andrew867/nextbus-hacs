import importlib.util
from pathlib import Path


def load_client():
    spec = importlib.util.spec_from_file_location(
        "nextbus_client",
        Path(__file__).resolve().parents[1] / "custom_components" / "nextbus" / "nextbus_client.py",
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_predictions_for_stop_parses_sample():
    nb = load_client()
    client = nb.NextBusClient(agency_id="ttc")

    sample = {
        "copyright": "All data copyright Toronto Transit Commission 2025.",
        "predictions": {
            "routeTag": "512",
            "stopTag": "14668",
            "routeTitle": "512-St. Clair",
            "agencyTitle": "Toronto Transit Commission",
            "stopTitle": "St Clair Ave West At Laughton Ave East Side",
            "direction": {
                "prediction": [
                    {
                        "seconds": "206",
                        "tripTag": "48968989",
                        "minutes": "3",
                        "isDeparture": "false",
                        "block": "512_1_10",
                        "dirTag": "512_0_512",
                        "branch": "512",
                        "epochTime": "1754882347123",
                        "vehicle": "4479",
                    },
                    {
                        "affectedByLayover": "true",
                        "seconds": "815",
                        "tripTag": "48968988",
                        "minutes": "13",
                        "isDeparture": "false",
                        "block": "512_2_20",
                        "dirTag": "512_0_512",
                        "branch": "512",
                        "epochTime": "1754882956176",
                        "vehicle": "4449",
                    },
                    {
                        "affectedByLayover": "true",
                        "seconds": "1579",
                        "tripTag": "48968987",
                        "minutes": "26",
                        "isDeparture": "false",
                        "block": "512_3_30",
                        "dirTag": "512_0_512",
                        "branch": "512",
                        "epochTime": "1754883719798",
                        "vehicle": "4440",
                    },
                    {
                        "affectedByLayover": "true",
                        "seconds": "2015",
                        "tripTag": "48968986",
                        "minutes": "33",
                        "isDeparture": "false",
                        "block": "512_6_60",
                        "dirTag": "512_0_512",
                        "branch": "512",
                        "epochTime": "1754884156176",
                        "vehicle": "4644",
                    },
                    {
                        "affectedByLayover": "true",
                        "seconds": "2615",
                        "tripTag": "48968985",
                        "minutes": "43",
                        "isDeparture": "false",
                        "block": "512_7_70",
                        "dirTag": "512_0_512",
                        "branch": "512",
                        "epochTime": "1754884756176",
                        "vehicle": "4652",
                    },
                ],
                "title": "East - 512 St Clair towards St Clair Station",
            },
        },
    }

    client._get = lambda params: sample
    result = client.predictions_for_stop("14933")

    assert len(result) == 1
    parsed = result[0]
    assert parsed["route"] == {"id": "512", "title": "512-St. Clair"}
    assert parsed["stop"] == {
        "id": "14668",
        "name": "St Clair Ave West At Laughton Ave East Side",
    }
    assert [v["minutes"] for v in parsed["values"]] == [3, 13, 26, 33, 43]
