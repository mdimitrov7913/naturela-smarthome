# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Martin Dimitrov

from homeassistant import config_entries
from homeassistant import exceptions
from homeassistant.core import callback
from homeassistant.config_entries import ConfigEntry, OptionsFlow
from homeassistant.helpers.selector import TextSelector, TextSelectorConfig
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers import config_validation as cv
import voluptuous as vol

from .api import NaturelaApiClient
from .const import DOMAIN

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            device_id = user_input.get("device_id", "")
            if len(device_id) != 4:
                errors["device_id"] = "invalid_length"
            else:
                client = NaturelaApiClient(
                    device_id=user_input["device_id"],
                    ath_cookie=user_input["ath_cookie"],
                    real_device_id="", # Not needed for confirmation
                )
                device_info = await client.get_device_info()
                await client.close()
                if not device_info:
                    errors["base"] = "cannot_connect"
                elif device_info.get("deviceType") != 7:
                    errors["base"] = "unsupported_device"
                else:
                    await self.async_set_unique_id(user_input["device_id"])
                    self._abort_if_unique_id_configured()
                    return self.async_create_entry(
                        title=device_info.get("name") or "Naturela Flat Water Heater " + user_input["device_id"],
                        data={
                            "device_id": user_input["device_id"],
                            "ath_cookie": user_input["ath_cookie"],
                            "real_device_id": device_info["realDeviceId"]
                        }
                    )

        data_schema = vol.Schema({
            vol.Required("device_id"): str,
            vol.Required("ath_cookie"): TextSelector(
                TextSelectorConfig(type="password")
            ),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(data_schema, user_input),
            errors=errors
        )