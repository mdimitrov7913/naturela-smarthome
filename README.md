
# Naturela Smarthome - Home Assistant Custom Integration

> [!CAUTION]
> **Not official Naturela software!**
>
> This integration is independently developed through reverse engineering
> of the official Naturela Smarthome WEB App and API. It is not affiliated
> with, authorized by, or endorsed by Naturela.

> [!WARNING]
> **Limited device support**
>
> Currently, the integration is compatible only with **Flat water heater /
> Flat boiler**, specifically `deviceType: 7`.

> [!IMPORTANT]
> **Privacy**
>
> This integration does not send your data to any third-party service.
> Communication is performed directly between Home Assistant and the
> official Naturela Smarthome API.

---

## Installation

### HACS (Recommended)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=mdimitrov7913&repository=naturela-smarthome&category=device)

### HACS – Custom repository
1. Open HACS in Home Assistant.
2. Click on **Integrations**.
3. Click the three dots in the top-right corner and select **Custom repositories**.
4. Paste the URL of this repository: `https://github.com/mdimitrov7913/naturela-smarthome`
5. Select **Integration** as the type and click **Add**.
6. Find "Naturela Smarthome" in the HACS store and click **Download**.
7. Restart Home Assistant.

### Manual
1. Copy the contents of the `custom_components` directory into your Home Assistant `custom_components` directory.
2. Restart Home Assistant.

## Configuration

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=naturela_smarthome)

1. In Home Assistant, go to **Settings** > **Devices & Services**.
2. Click **Add Integration**.
3. Search for **Naturela Smarthome** and select it.
4. Follow the configuration steps below.

### Please configure via Home Assistant UI (Config flow). Configuration via YAML is not supported!

### For configuration you will need:
#### 1. `Device ID`
- A four-digit number identifying your device.
- It can be found in the [WEB App](https://iot.naturela-bg.com/) URL, when you are on the device page
- Example:
> https://iot.naturela-bg.com/#/device/flatboiler/0000
>
> `Device ID`: `0000`

#### 2. `Ath cookie`
- Two Naturela Smarthome responds with two cookies upon login. The required cookie is called `.AspNetCore.cookieath`, here refered to as `Ath cookie`.
- The cookie can be retrieved from the [WEB App](https://iot.naturela-bg.com/) using your browser's Developer tools

### Just paste the `Device ID` and the `Ath cookie` values' into the integration Config flow.

## Reasons for configuration failure

### 1. `Device ID must be exactly 4 characters!`
#### The `Device ID` length you pasted is not correct!
> [!WARNING]
> Actually, at this point reverse-engineering did not show `Device IDs` with different lengths, but it may be possible. If so please [open a new issue](https://github.com/mdimitrov7913/naturela-smarthome/issues)!
#### Fix:
- Make sure the `Device ID` is exactly 4 digits!
### 2. `Couldn't authenticate with the provided data!`
#### Upon verification of the `Device ID` and the `Ath cookie` values, authentication failed!
#### Fix:
- Make sure the `Device ID` and the `Ath cookie` values are correct!
### 3. `This device type is not supported!`
#### Your device is currently not supported by the integration!
> [!WARNING]
> Currently, only device type 7 (Flat water heater / Flat boiler) is supported!
#### Fix:
- This error cannot be fixed. The specified device is just not supported!

## Reauthentication

#### The `Ath cookie` has an expiration date, after which reauthentication is required.
#### There is currently no built-in reauthentication option.
#### To reauthenticate, log in to the [WEB App](https://iot.naturela-bg.com/) and follow the Configuration instructions from this document

## Open an Issue

> [!CAUTION]
> When opening an issue, DO NOT include your `Device ID` and `Ath cookie` values!
>
> They provide full access to your Naturela Smarthome account!

### [Open an Issue](https://github.com/mdimitrov7913/naturela-smarthome/issues)

## License

This project is licensed under the GNU General Public License v3.0 or later.
See the [LICENSE](LICENSE) file for details.

© 2026 Martin Dimitrov. All rights reserved.