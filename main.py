"""Main loop."""

from EtilbudsavisHomeAssistant.OfferCollector import OfferColloector


def main(items: list[list[str]]) -> None:
    """Search for the best offers.

    Args:
        items (list[list[str]]): List of items and thier units.
    """
    collector = OfferColloector()

    for query, unit in items:
        collector.set_query(query)
        collector.set_conditions(unit)
        collector.get_catalog_offers()
        collector.clean_offers()
        price, shop = collector.find_best_offer()
        print(price, shop)


if __name__ == "__main__":
    queries = [["æg", "pcs"], ["fløde", "ml"]]
    main(queries)
