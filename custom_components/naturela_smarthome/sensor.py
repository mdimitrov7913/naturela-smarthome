# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Martin Dimitrov

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import UnitOfTemperature
from homeassistant.const import UnitOfEnergy
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)

from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN
from .api import NaturelaDataUpdateCoordinator


async def async_setup_entry(
        hass: HomeAssistant,
        entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
):
    """Set up Naturela sensors."""

    coordinator: NaturelaDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    entities = [
        NaturelaFtTemperatureSensor(coordinator, entry),
        NaturelaStlTemperatureSensor(coordinator, entry),
        NaturelaSetTemperatureSensor(coordinator, entry),
        NaturelaEnergyDSensor(coordinator, entry),
        NaturelaEnergyNSensor(coordinator, entry),
    ]

    async_add_entities(entities)


class NaturelaBaseSensor(CoordinatorEntity, SensorEntity):
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

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.handle_data(self.coordinator.data)

    def handle_data(self, data: dict):
        """Override in subclasses to return the specific value."""
        raise NotImplementedError

class NaturelaFtTemperatureSensor(NaturelaBaseSensor):
    """Current water temperature (FT_Temp)."""

    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:thermometer"

    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)

        device_id = entry.data["device_id"]

        self._attr_name = f"Flat Water Heater {device_id} FT Temperature"
        self._attr_unique_id = f"{device_id}_ft_temp"

    def handle_data(self, data: dict):
        return data.get("FT_Temp")
class NaturelaStlTemperatureSensor(NaturelaBaseSensor):
    """Current water temperature (STL_Temp)."""

    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:thermometer"

    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)

        device_id = entry.data["device_id"]

        self._attr_name = f"Flat Water Heater {device_id} STL Temperature"
        self._attr_unique_id = f"{device_id}_stl_temp"

    def handle_data(self, data: dict):
        return data.get("STL_Temp")

class NaturelaSetTemperatureSensor(NaturelaBaseSensor):
    """Set water temperature (SetTemp)."""

    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:thermometer-plus"

    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)

        device_id = entry.data["device_id"]

        self._attr_name = f"Flat Water Heater {device_id} Set Temperature"
        self._attr_unique_id = f"{device_id}_set_temp"

    def handle_data(self, data: dict):
        return data.get("SetTemp")

class NaturelaEnergyDSensor(NaturelaBaseSensor):
    """Day energy consumption (EnergyD)."""

    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:lightning-bolt"

    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)

        device_id = entry.data["device_id"]

        self._attr_name = f"Flat Water Heater {device_id} Consumed Energy Day"
        self._attr_unique_id = f"{device_id}_energy_day"

    def handle_data(self, data: dict):
        return data.get("EnergyD")
class NaturelaEnergyNSensor(NaturelaBaseSensor):
    """Night energy consumption (EnergyN)."""

    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:lightning-bolt"

    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)

        device_id = entry.data["device_id"]

        self._attr_name = f"Flat Water Heater {device_id} Consumed Energy Night"
        self._attr_unique_id = f"{device_id}_energy_night"

    def handle_data(self, data: dict):
        return data.get("EnergyN")