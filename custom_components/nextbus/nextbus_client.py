"""Client for UmoIQ NextBus publicJSONFeed API."""
from __future__ import annotations

"""Client for UmoIQ NextBus publicJSONFeed API."""
from typing import Any, cast

from datetime import datetime

import requests
from requests import RequestException


class NextBusError(Exception):
    """Base class for NextBus errors."""


class NextBusHTTPError(NextBusError):
    """HTTP error from NextBus API."""

    def __init__(self, message: str, response: requests.Response | None = None) -> None:
        super().__init__(message)
        self.response = response


class NextBusFormatError(NextBusError):
    """Raised when the API returns invalid data."""


class NextBusClient:
    """Minimal client for the UmoIQ NextBus JSON feed."""

    BASE_URL = "https://webservices.umoiq.com/service/publicJSONFeed"
    DEFAULT_TIMEOUT = 10

    def __init__(self, agency_id: str | None = None, *, timeout: int = DEFAULT_TIMEOUT) -> None:
        self.agency_id = agency_id
        self._session = requests.Session()
        self._timeout = timeout
        self._rate_limit: int = 0
        self._rate_limit_remaining: int = 0
        self._rate_limit_reset: datetime | None = None

    def _get(self, params: dict[str, Any]) -> dict[str, Any]:
        try:
            response = self._session.get(
                self.BASE_URL, params=params, timeout=self._timeout
            )
            response.raise_for_status()

            self._rate_limit = int(response.headers.get("X-RateLimit-Limit", 0))
            self._rate_limit_remaining = int(
                response.headers.get("X-RateLimit-Remaining", 0)
            )
            reset_time = response.headers.get("X-RateLimit-Reset")
            self._rate_limit_reset = (
                datetime.fromtimestamp(int(reset_time)) if reset_time else None
            )

            return cast(dict[str, Any], response.json())
        except requests.HTTPError as exc:  # pragma: no cover - network
            raise NextBusHTTPError("Error from the NextBus API", exc.response) from exc
        except RequestException as exc:  # pragma: no cover - network
            raise NextBusHTTPError("Error communicating with NextBus API") from exc
        except ValueError as exc:  # pragma: no cover - invalid JSON
            raise NextBusFormatError("Failed to parse JSON from request") from exc

    def agencies(self) -> list[dict[str, str]]:
        data = self._get({"command": "agencyList"})
        agencies = []
        for agency in data.get("agency", []):
            agencies.append({"id": agency.get("tag", ""), "name": agency.get("title", "")})
        return agencies

    def routes(self, agency_id: str | None = None) -> list[dict[str, str]]:
        agency_id = agency_id or self.agency_id
        data = self._get({"command": "routeList", "a": agency_id})
        routes = []
        for route in data.get("route", []):
            routes.append({"id": route.get("tag", ""), "title": route.get("title", "")})
        return routes

    def route_details(self, route_id: str, agency_id: str | None = None) -> dict[str, Any]:
        agency_id = agency_id or self.agency_id
        data = self._get({"command": "routeConfig", "a": agency_id, "r": route_id}).get("route", {})
        stops = [
            {
                "id": stop.get("tag"),
                "name": stop.get("title"),
                "tag": stop.get("tag"),
                "code": stop.get("stopId"),
                "stopId": stop.get("stopId"),
            }
            for stop in data.get("stop", [])
        ]
        directions: list[dict[str, Any]] = []
        dir_data = data.get("direction")
        if isinstance(dir_data, list):
            dir_list = dir_data
        elif dir_data:
            dir_list = [dir_data]
        else:
            dir_list = []
        for direction in dir_list:
            directions.append(
                {
                    "name": direction.get("title"),
                    "useForUi": direction.get("useForUI") in (True, "true", "True"),
                    "stops": direction.get("stop", []),
                }
            )
        return {"stops": stops, "directions": directions}

    def predictions_for_stop(self, stop_id: str, agency_id: str | None = None) -> list[dict[str, Any]]:
        agency_id = agency_id or self.agency_id
        data = self._get({"command": "predictions", "a": agency_id, "stopId": stop_id})
        predictions_raw = data.get("predictions")
        if not predictions_raw:
            return []
        if isinstance(predictions_raw, list):
            prediction_items = predictions_raw
        else:
            prediction_items = [predictions_raw]
        results: list[dict[str, Any]] = []
        for item in prediction_items:
            route_tag = item.get("routeTag")
            stop_tag = item.get("stopTag", stop_id)
            route_title = item.get("routeTitle", "")
            stop_title = item.get("stopTitle", "")
            values: list[dict[str, int]] = []
            directions = item.get("direction")
            if isinstance(directions, list):
                dir_list2 = directions
            elif directions:
                dir_list2 = [directions]
            else:
                dir_list2 = []
            for direction in dir_list2:
                preds = direction.get("prediction")
                if isinstance(preds, list):
                    pred_list = preds
                elif preds:
                    pred_list = [preds]
                else:
                    pred_list = []
                for pred in pred_list:
                    try:
                        values.append(
                            {
                                "timestamp": int(pred.get("epochTime")),
                                "seconds": int(pred.get("seconds")),
                                "minutes": int(pred.get("minutes")),
                            }
                        )
                    except (TypeError, ValueError):
                        continue
            results.append(
                {
                    "route": {"id": route_tag, "title": route_title},
                    "stop": {"id": stop_tag, "name": stop_title},
                    "values": values,
                }
            )
        return results

    @property
    def rate_limit(self) -> int:
        return self._rate_limit

    @property
    def rate_limit_remaining(self) -> int:
        return self._rate_limit_remaining

    @property
    def rate_limit_reset(self) -> datetime | None:
        return self._rate_limit_reset

    @property
    def rate_limit_percent(self) -> float:
        if self._rate_limit == 0:
            return 0.0
        return self._rate_limit_remaining / self._rate_limit * 100
