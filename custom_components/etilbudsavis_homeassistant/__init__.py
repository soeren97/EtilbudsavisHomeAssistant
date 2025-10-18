"""Initialize the eTilbudsavis (Local Offers) integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .offer_collector import OfferCollector

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Legacy setup, required by HA but unused."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """
    Set up the integration from a config entry.

    This method:
      - Initializes the OfferCollector with stored credentials.
      - Registers the HA service for searching offers.
      - Stores references in hass.data for later cleanup.
    """
    _LOGGER.debug("Setting up eTilbudsavis integration...")

    api_key: str = entry.data.get("api_key")
    api_secret: str = entry.data.get("api_secret")

    # Create and store the OfferCollector instance
    collector = OfferCollector(api_key, api_secret)
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN]["collector"] = collector
    hass.data[DOMAIN]["entry_id"] = entry.entry_id

    # Register service
    async def handle_find_best_offers(call: ServiceCall) -> None:
        """Handle service call to search offers.

        Expected call.data:
          - items: list of [query, unit] pairs, e.g. [["mælk", "l"], ["smør", "g"]]
        """
        items: list[list[str]] = call.data.get("items", [])
        _LOGGER.debug(
            "Received find_best_offers service call with %s items", len(items)
        )

        try:
            offers = await collector.async_find_best_offers(items)
            for price, shop in offers:
                # Use a stable entity id
                hass.states.async_set(f"etilbudsavis.{shop}", price)
            _LOGGER.debug(
                "Service call completed successfully with %s offers.", len(offers)
            )
        except (
            Exception
        ) as exc:  # broad except to prevent service crash from unexpected errors
            _LOGGER.exception("Error while handling find_best_offers service: %s", exc)

    # Register the service (coroutine handler)
    hass.services.async_register(DOMAIN, "find_best_offers", handle_find_best_offers)

    _LOGGER.info("eTilbudsavis integration successfully initialized.")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """
    Handle unloading of the integration.

    This method:
      - Closes the HTTPX client session.
      - Unregisters the custom service.
      - Cleans up hass.data references.
    """
    _LOGGER.debug("Unloading eTilbudsavis integration...")

    collector: OfferCollector | None = hass.data.get(DOMAIN, {}).get("collector")
    if collector:
        await collector.async_close()
        _LOGGER.debug("Closed HTTP session for OfferCollector.")

    # Unregister the service
    hass.services.async_remove(DOMAIN, "find_best_offers")

    # Remove stored data
    hass.data.pop(DOMAIN, None)

    _LOGGER.info("eTilbudsavis integration unloaded successfully.")
    return True
