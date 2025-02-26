"""Test the number websocket API."""
from pytest_unordered import unordered

from homeassistant.components.number.const import DOMAIN
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component


async def test_device_class_units(hass: HomeAssistant, hass_ws_client) -> None:
    """Test we can get supported units."""
    assert await async_setup_component(hass, DOMAIN, {})

    client = await hass_ws_client(hass)

    # Device class with units which number allows customizing & converting
    await client.send_json(
        {
            "id": 1,
            "type": "number/device_class_convertible_units",
            "device_class": "temperature",
        }
    )
    msg = await client.receive_json()
    assert msg["success"]
    assert msg["result"] == {"units": unordered(["°F", "°C", "K"])}

    # Device class with units which number doesn't allow customizing & converting
    await client.send_json(
        {
            "id": 2,
            "type": "number/device_class_convertible_units",
            "device_class": "energy",
        }
    )
    msg = await client.receive_json()
    assert msg["success"]
    assert msg["result"] == {"units": []}

    # Unknown device class
    await client.send_json(
        {
            "id": 3,
            "type": "number/device_class_convertible_units",
            "device_class": "kebabsås",
        }
    )
    msg = await client.receive_json()
    assert msg["success"]
    assert msg["result"] == {"units": unordered([])}
