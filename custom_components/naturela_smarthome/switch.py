# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Martin Dimitrov

from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN
from .api import NaturelaDataUpdateCoordinator

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Naturela switch entities."""
    coordinator: NaturelaDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([NaturelaHeaterBoostSwitch(coordinator, entry)])

class NaturelaHeaterBoostSwitch(CoordinatorEntity, SwitchEntity):
    """Switch for Naturela Heater Boost."""

    _attr_translation_key = "heater_boost"
    
    def __init__(self, coordinator: NaturelaDataUpdateCoordinator, entry: ConfigEntry):
        super().__init__(coordinator)
        self._entry = entry
        device_id = entry.data["device_id"]
        
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device_id)},
            name=f"Naturela Flat Water Heater {device_id}",
            manufacturer="Naturela",
            model="Flat Water Heater",
        )
        self._attr_name = f"Flat Water Heater {device_id} Heater Boost"
        self._attr_unique_id = f"{device_id}_heater_boost"
        self._attr_icon = "mdi:lightning-bolt"

    @property
    def is_on(self) -> bool:
        """Return True if the heater boost is on."""
        return self.coordinator.data.get("HasBoost")

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the heater boost on."""
        await self.coordinator.client.set_heater(True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the heater boost off. The API doesn't support this."""
