"""Setup components for home assistant."""

from typing import Any

from EtilbudsavisHomeAssistant.OfferCollector import setup_service
from homeassistant.core import HomeAssistant


def setup(hass: HomeAssistant) -> bool:
    """Set up the Etilbudsavis component."""
    return setup_service(hass)  # type: ignore
