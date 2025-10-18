"""Functions to be used throughout the repocetory."""

from __future__ import annotations

import json
import logging
from typing import Any

from httpx import AsyncClient, HTTPStatusError, RequestError

from .const import BASE_URL

_LOGGER = logging.getLogger(__name__)


def load_config(path: str) -> Any:
    """Load the config file.

    Args:
        path (str): Path to config file.

    Returns:
        dict[str, str]: API key and secret.
    """
    with open(path, "r") as file:
        return json.load(file)


async def validate_credentials(api_key: str, api_secret: str) -> bool:
    """
    Validate API credentials by making a lightweight test request.

    Args:
        api_key: The API key provided by the user.
        api_secret: The API secret provided by the user.

    Returns:
        True if credentials are valid, False otherwise.
    """
    headers = {"X-API-Key": api_key, "X-API-Secret": api_secret}
    params: dict[str, Any] = {
        "query": "mælk",
        "r_lat": "55.695497",
        "r_lng": "12.550145",
        "r_radius": "1000",
        "r_locale": "da_DK",
        "limit": "1",
    }

    async with AsyncClient(headers=headers, timeout=10) as client:
        try:
            response = await client.get(BASE_URL, params=params)
            response.raise_for_status()

            if response.status_code == 401:
                _LOGGER.warning("Invalid API credentials.")
                return False

            return True

        except HTTPStatusError as e:
            _LOGGER.error("HTTP error during credential validation: %s", e)
            return False
        except RequestError as e:
            _LOGGER.error("Connection error during credential validation: %s", e)
            return False
        except Exception as e:
            _LOGGER.exception("Unexpected error during credential validation: %s", e)
            return False
