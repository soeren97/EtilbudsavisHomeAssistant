"""Functions to be used throughout the repocetory."""

import json
from typing import Any


def load_config(path: str) -> Any:
    """Load the config file.

    Args:
        path (str): Path to config file.

    Returns:
        dict[str, str]: API key and secret.
    """
    with open(path, "r") as file:
        return json.load(file)
