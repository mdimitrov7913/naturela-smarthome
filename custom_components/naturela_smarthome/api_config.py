# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Martin Dimitrov

import async_timeout
import aiohttp
import logging

_LOGGER = logging.getLogger(__name__)

API_URL = "https://iot.naturela-bg.com/api"

class NaturelaApiClient:
    def __init__(self, session: aiohttp.ClientSession):
        self._session = session

    async def async_confirm_connection(self, device_id: str, ath_cookie: str):
        """Validate device ID + cookie and return device info."""
        payload = {"deviceId": device_id}

        headers = {
            "Content-Type": "application/json",
            "Cookie": f".AspNetCore.cookieath={ath_cookie}"
        }

        try:
            with async_timeout.timeout(10):
                response = await self._session.post(API_URL + "/device/getmydevice", json=payload, headers=headers)

                if response.status != 200:
                    _LOGGER.error("Naturela API error: HTTP %s", response.status)
                    return None

                data = await response.json(content_type=None)

                if isinstance(data, list):
                    if not data:
                        _LOGGER.error("Naturela API returned an empty list")
                        return None
                    data = data[0]

                # Validate expected fields
                if not isinstance(data, dict) or "deviceType" not in data or "realDeviceId" not in data:
                    _LOGGER.error("Naturela API returned unexpected data structure: %s", data)
                    return None

                return data

        except Exception as err:
            _LOGGER.error("Naturela API connection error: %s", err)
            return None
