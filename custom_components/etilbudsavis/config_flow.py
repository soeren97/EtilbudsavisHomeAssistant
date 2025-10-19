"""Config flow for the Local Store Offers integration."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN
from .utils import validate_credentials


class LocalOffersAPIValidator:
    """Single-responsibility class for validating API credentials."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the validator with a Home Assistant instance."""
        self._hass = hass


@config_entries.HANDLERS.register(DOMAIN)
class LocalOffersConfigFlow(config_entries.ConfigFlow):
    """Handle the configuration flow for Local Store Offers."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, str] | None = None
    ) -> FlowResult:
        """Prompt for and validate API credentials."""
        errors: dict[str, str] = {}

        if user_input is not None:
            api_key = user_input.get("api_key", "")
            api_secret = user_input.get("api_secret", "")

            if await validate_credentials(api_key, api_secret):
                await self.async_set_unique_id(DOMAIN)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title="eTilbudsavis", data=user_input)
            else:
                errors["base"] = "Authentication failed"

        data_schema = vol.Schema(
            {
                vol.Required("api_key"): str,
                vol.Required("api_secret"): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )
