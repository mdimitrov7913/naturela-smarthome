# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Martin Dimitrov

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .api import NaturelaApiClient, NaturelaDataUpdateCoordinator
from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict):
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    # Create API client
    client = NaturelaApiClient(
        device_id=entry.data["device_id"],
        ath_cookie=entry.data["ath_cookie"],
        real_device_id=entry.data["real_device_id"],
    )

    coordinator = NaturelaDataUpdateCoordinator(hass, client)

    await coordinator.async_config_entry_first_refresh()

    # Store client and coordinator in hass.data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "coordinator": coordinator,
    }

    # Load platforms
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor", "select", "switch"])

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor", "select", "switch"])
    
    if unload_ok:
        data = hass.data[DOMAIN].pop(entry.entry_id)
        await data["client"].close()

    return unload_ok
