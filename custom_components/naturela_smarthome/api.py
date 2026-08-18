# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Martin Dimitrov

import asyncio
import async_timeout
import json
import logging
from datetime import timedelta
from typing import Any, Dict

import aiohttp
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

BASE_URL = "https://iot.naturela-bg.com/api"

class NaturelaApiError(HomeAssistantError):
    """General API error."""

class NaturelaApiAuthError(HomeAssistantError):
    """Authentication / cookie error."""

class NaturelaApiClient:
    """Client for Naturela Flat Boiler API."""

    def __init__(self, device_id: str, ath_cookie: str, real_device_id: str):
        self.device_id = device_id              # 4-digit
        self.real_device_id = real_device_id    # 12-char
        self.ath_cookie = ath_cookie

        self._session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def _request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        session = await self._get_session()
        url = f"{BASE_URL}/{path.lstrip('/')}"

        headers = {
            "Cookie": f".AspNetCore.cookieath={self.ath_cookie}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        try:
            async with session.request(method, url, headers=headers, **kwargs) as resp:
                text = await resp.text()

                if resp.status == 401:
                    raise NaturelaApiAuthError("Invalid or expired ath cookie")

                if resp.status >= 400:
                    raise NaturelaApiError(f"API error {resp.status}: {text}")

                data = json.loads(text)

                # Some responses are double-encoded as a JSON string
                if isinstance(data, str):
                    try:
                        data = json.loads(data)
                    except json.JSONDecodeError:
                        # If it's just a regular string, keep it as is
                        pass

                return data

        except asyncio.TimeoutError as err:
            raise NaturelaApiError("Timeout contacting Naturela API") from err

        except aiohttp.ClientError as err:
            raise NaturelaApiError(f"Network error: {err}") from err

    # -------------------------------------------------------------------------
    # Public API methods
    # -------------------------------------------------------------------------

    async def get_device_info(self) -> Dict[str, Any]:
        """POST /device/getmydevice"""
        data = await self._request(
            "POST",
            "device/getmydevice",
            json={"deviceId": int(self.device_id)},
        )
        if isinstance(data, list):
            if not data:
                return {}
            data = data[0]
        return data

    async def get_device_data(self) -> Dict[str, Any]:
        """GET /flatboiler/{deviceId}"""
        data = await self._request(
            "GET",
            f"flatboiler/{self.device_id}",
        )

        _LOGGER.debug("Device data response: %s", data)

        if isinstance(data, list):
            if not data:
                raise NaturelaApiError("Naturela API returned an empty list")
            data = data[0]

        if not isinstance(data, dict):
             raise NaturelaApiError(f"Unexpected API response type: {type(data)}")

        if "objectJson" not in data:
            raise NaturelaApiError("DeviceWrapper missing objectJson")

        try:
            return json.loads(data["objectJson"])
        except json.JSONDecodeError:
            raise NaturelaApiError("Failed to parse objectJson inner JSON")

    async def set_state(self, state: int) -> None:
        """POST /flatboiler/setState"""
        _LOGGER.debug("Setting state to %s for device %s", state, self.real_device_id)
        await self._request(
            "POST",
            "flatboiler/setState",
            json={"deviceId": self.real_device_id, "state": state},
        )

    async def set_heater(self, heater: bool) -> None:
        """POST /flatboiler/setHeater"""
        _LOGGER.debug("Setting heater to %s for device %s", heater, self.real_device_id)
        await self._request(
            "POST",
            "flatboiler/setHeater",
            json={"deviceId": self.real_device_id, "heater": heater},
        )

    async def close(self):
        """Close aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()


class NaturelaDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, client: NaturelaApiClient):
        """Initialize."""
        self.client = client
        super().__init__(
            hass,
            _LOGGER,
            name="Naturela Data Update Coordinator",
            update_interval=timedelta(seconds=30),
        )

    async def _async_update_data(self):
        """Update data via API."""
        try:
            return await self.client.get_device_data()
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
