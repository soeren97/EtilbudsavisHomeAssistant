"""Collect and process offers."""

from typing import Any, Optional

import requests  # type:ignore
from EtilbudsavisHomeAssistant.utils import load_config
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.typing import ConfigType


class OfferColloector:
    """Class to collect and process offers."""

    def __init__(self) -> None:
        """Initialize class."""
        self.query: Optional[str] = None
        self.unit: Optional[str] = None
        self.response: Optional[list[dict[Any, Any]]]

        config = load_config("config.json")
        self.api_key = config["key"]
        self.api_secret = config["secret"]

    def set_query(self, query: str) -> None:
        """Set the search query.

        Args:
            query (str): Search string.
        """
        self.query = query

    def set_conditions(self, unit: str) -> None:
        """Set conditions to be met.

        Currently only unit of meassurement.

        Args:
            unit (str): Unit of meassurement.
        """
        self.unit = unit

    def get_catalog_offers(self) -> None:
        """Call the Etilbudsavis API endpoint using API key and secret."""
        if self.query:
            endpoint = (
                "https://etilbudsavis.dk/api/squid/v2/offers/"
                f"search?query={self.query}&r_lat="
                "55.695497&r_lng=12.550145&r_radius=20000"
                "&r_locale=da_DK&limit=24&offset=0"
            )
            headers = {"X-API-Key": self.api_key, "X-API-Secret": self.api_secret}

            try:
                response = requests.get(endpoint, headers=headers)
                response.raise_for_status()  # Raise an exception for bad status codes
                self.response = response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")

        else:
            print("Please select query")

    def check_conditions(self, offer: dict[Any, Any]) -> bool:
        """Check the conditions to filter out irrelivant offers.

        Args:
            offer (dict[Any]): Offer.

        Returns:
            bool: Is the offer relevant.
        """
        condition1 = self.query in offer["heading"]
        condition2 = offer["quantity"]["unit"]["symbol"] == self.unit
        return condition1 and condition2

    def clean_offers(self) -> None:
        """Remove non relevant offers."""
        self.response = [
            offer
            for offer in self.response  # type: ignore
            if self.check_conditions(offer)
        ]

    def find_best_offer(self) -> tuple[float, str]:
        """Find the cheapest offer.

        Returns:
            tuple[float, str]: Price and store of the cheapest item.
        """
        prices = [
            offer["pricing"]["price"] / offer["quantity"]["size"]["to"]
            for offer in self.response  # type:ignore
        ]
        shops = [offer["branding"]["name"] for offer in self.response]  # type:ignore

        min_price = min(prices)
        index = prices.index(min_price)
        shop = shops[index]

        if self.unit in ["g", "ml"]:
            min_price *= 1000

        return min_price, shop

    def find_best_offers(self, items: list[list[str]]) -> list[tuple[float, str]]:
        """Search for the best offers.

        Args:
            items (list[list[str]]): List of items and thier units.

        Returns:
            list[tuple[float, str]]: List of prices and locations of offers.
        """
        results = []
        for query, unit in items:
            self.set_query(query)
            self.set_conditions(unit)
            self.get_catalog_offers()
            self.clean_offers()
            price, shop = self.find_best_offer()
            results.append((price, shop))
        return results


def handle_offer_search(hass: HomeAssistant, call: ServiceCall) -> None:
    """Fetch offers using the offercolector class from the homeass config file.

    Args:
        hass (HomeAssistant): Home assistant object.
        call (ServiceCall): Call to the home assistant config (maybe).
    """
    items = call.data.get("items", [])
    collector = OfferColloector()
    offers = collector.find_best_offers(items)
    for price, shop in offers:
        hass.states.set(f"etilbudsavis.{shop}", price)


def setup_service(hass: HomeAssistant) -> bool:
    """Set up the application in home assistant.

    Args:
        hass (HomeAssistant): Home assistant object.

    Returns:
        bool: Status.
    """
    hass.services.register("etilbudsavis", "find_best_offers", handle_offer_search)
    return True


if __name__ == "__main__":
    pass
