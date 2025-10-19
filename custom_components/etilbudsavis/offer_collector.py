"""Collect and process offers asynchronously from eTilbudsavis API."""

from __future__ import annotations

import logging
from typing import Any

import aiohttp
from httpx import AsyncClient

from .const import BASE_URL

_LOGGER = logging.getLogger(__name__)


class OfferCollector:
    """Class to collect and process offers from the eTilbudsavis API."""

    def __init__(self, api_key: str, api_secret: str) -> None:
        """Initialize class.

        Args:
            api_key: API key for authentication.
            api_secret: API secret for authentication.
            session: Optional existing aiohttp session.
        """
        self._api_key = api_key
        self._api_secret = api_secret
        self._session: AsyncClient
        self.unit: str
        self.query: str
        self.response: list[dict[str, Any]] = []

    async def _get_session(self) -> AsyncClient:
        """Ensure a valid aiohttp session exists."""
        headers = {"X-API-Key": self._api_key, "X-API-Secret": self._api_secret}
        self._session = AsyncClient(headers=headers)

    def set_query(self, query: str) -> None:
        """Set the search query."""
        self.query = query

    def set_conditions(self, unit: str) -> None:
        """Set filter conditions (currently only measurement unit)."""
        self.unit = unit

    async def async_get_catalog_offers(self) -> None:
        """Fetch offers from the API."""
        if not self.query:
            _LOGGER.warning("Please set a query before fetching offers.")
            return

        endpoint = (
            f"{BASE_URL}?query={self.query}"
            "&r_lat=55.695497&r_lng=12.550145&r_radius=20000"
            "&r_locale=da_DK&limit=24&offset=0"
        )

        try:
            await self._get_session()
            response = await self._session.get(endpoint)
            response.raise_for_status()
            self.response = response.json()
        except aiohttp.ClientResponseError as e:
            _LOGGER.error("API responded with error %s: %s", e.status, e.message)
        except aiohttp.ClientError as e:
            _LOGGER.error("Error connecting to API: %s", e)
        except Exception as e:
            _LOGGER.exception("Unexpected error fetching offers: %s", e)

    def _check_conditions(self, offer: dict[str, Any]) -> bool:
        """Check the conditions to filter out irrelevant offers."""
        if not self.query or not self.unit:
            return False

        try:
            condition1 = self.query.lower() in offer.get("heading", "").lower()
            unit_info = offer.get("quantity", {}).get("unit", {}).get("symbol", "")
            condition2 = unit_info == self.unit
            return condition1 and condition2
        except Exception as e:
            _LOGGER.warning("Error checking conditions for offer: %s", e)
            return False

    def clean_offers(self) -> None:
        """Filter out offers that don't match conditions."""
        self.response = [
            offer for offer in self.response if self._check_conditions(offer)
        ]

    def find_best_offer(self) -> tuple[float, str]:
        """Find the cheapest offer."""
        if not self.response:
            raise ValueError("No offers available to process.")

        prices = [
            offer["pricing"]["price"] / offer["quantity"]["size"]["to"]
            for offer in self.response
            if "pricing" in offer and "quantity" in offer
        ]
        shops = [offer["branding"]["name"] for offer in self.response]

        min_price = min(prices)
        index = prices.index(min_price)
        shop = shops[index]

        if self.unit in ["g", "ml"]:
            min_price *= 1000

        return min_price, shop

    async def async_find_best_offers(
        self, items: list[list[str]]
    ) -> list[tuple[float, str]]:
        """Find the best offers for a list of items."""
        results: list[tuple[float, str]] = []
        for query, unit in items:
            self.set_query(query)
            self.set_conditions(unit)
            await self.async_get_catalog_offers()
            self.clean_offers()
            if self.response:
                price, shop = self.find_best_offer()
                results.append((price, shop))
        return results

    async def async_close(self) -> None:
        """Close the aiohttp session if created internally."""
        await self._session.aclose()
