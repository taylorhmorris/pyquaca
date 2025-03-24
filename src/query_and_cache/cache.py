"""Cache module for storing and retrieving data from cache"""

import json
import logging
from typing import Any

from query_and_cache.cacheclass import Cache


def store_in_cache(file_path: str, data: Any) -> bool:
    """
    Write data object to cache file

    Args:
        file_path (str): The path to the cache file.
        data: The data to store in the cache file.

    Returns:
        True if the data was successfully stored in the cache file, otherwise False
    """
    if not data:
        logging.error("Data is empty")
        return False
    try:
        json_data = json.dumps(data)
    except TypeError as e:
        logging.error("Could not serialize data")
        logging.error("%s", e)
        return False
    cache = Cache("")
    return cache.store(file_path, json_data)


def retrieve_from_cache(file_path: str) -> Any | bool:
    """
    Retrieve query data from cache.

    Args:
        file_path (str): The path to the cache file.

    Returns:
        The data from the cache file if it exists, otherwise False.
    """
    cache = Cache("")
    text = cache.retrieve(file_path)
    if text:
        return json.loads(text)
    return False
