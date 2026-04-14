from unittest.mock import patch
import pytest
from homeassistant import config_entries, data_entry_flow
from homeassistant.core import HomeAssistant
from custom_components.thames_water.const import DOMAIN
import custom_components.thames_water

async def test_form(recorder_mock, hass: HomeAssistant, mock_thames_water_client):
    """Test we get the form and handle success."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == data_entry_flow.FlowResultType.FORM
    assert result["errors"] == {}

    with patch(
        "custom_components.thames_water.async_setup_entry",
        return_value=True,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "username": "test@example.com",
                "password": "test-password",
                "account_number": "123456789",
                "meter_id": "987654321",
                "liter_cost": "0.0016",
                "fetch_hours": "15,23"
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] == data_entry_flow.FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Thames Water"
    assert result2["data"] == {
        "username": "test@example.com",
        "password": "test-password",
        "account_number": "123456789",
        "meter_id": "987654321",
        "liter_cost": "0.0016",
        "fetch_hours": "15,23"
    }

async def test_form_invalid_auth(recorder_mock, hass: HomeAssistant):
    """Test we handle invalid auth."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.thames_water.config_flow.ThamesWaterConfigFlow._validate_input",
        return_value={"base": "cannot_connect"},
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "username": "test@example.com",
                "password": "test-password",
                "account_number": "123456789",
                "meter_id": "987654321",
                "liter_cost": "0.0016",
                "fetch_hours": "15,23"
            },
        )

    assert result2["type"] == data_entry_flow.FlowResultType.FORM
    assert result2["errors"] == {"base": "cannot_connect"}
