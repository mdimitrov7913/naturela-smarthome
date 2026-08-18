# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Martin Dimitrov

from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN
from .api import NaturelaDataUpdateCoordinator

STATE_MAP = {
    0: "off",
    1: "heating",
    2: "smart",
    3: "study",
    4: "timers",
}
# Reverse map for setting state
NAME_TO_STATE = {v: k for k, v in STATE_MAP.items()}

async def async_setup_entry(
        hass: HomeAssistant,
        entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
):
    """Set up Naturela select entities."""
    coordinator: NaturelaDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([NaturelaStateSelect(coordinator, entry)])

class NaturelaStateSelect(CoordinatorEntity, SelectEntity):
    """Dropdown for Naturela Boiler State."""

    _attr_translation_key = "boiler_mode"
    _attr_options = list(STATE_MAP.values())
    _attr_icon = "mdi:water-boiler"
    
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
        self._attr_unique_id = f"{device_id}_state"
        self._attr_name = f"Flat Water Heater {device_id} State"

    @property
    def current_option(self) -> str:
        """Return the current selected option."""
        state_code = self.coordinator.data.get("State")
        return STATE_MAP.get(state_code)

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        state_code = NAME_TO_STATE.get(option)
        if state_code is not None:
            await self.coordinator.client.set_state(state_code)
            # Refresh data to confirm update
            await self.coordinator.async_request_refresh()
