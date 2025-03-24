"""Cache module for storing and retrieving data from cache"""

import json
import logging
import os
from pathlib import Path
from typing import Any

import requests


def store_in_cache_as_text(file_path: str, data: str) -> bool:
    """
    Write data to cache file

    Args:
        file_path (str): The path to the cache file.
        data (str): The data to store in the cache file.

    Returns:
        True if the data was successfully stored in the cache file, otherwise False
    """
    logger = logging.getLogger("Cache")
    if not file_path or len(file_path) == 0:
        logger.error("File path is empty")
        return False
    cache_folder = os.path.dirname(file_path)
    Path(cache_folder).mkdir(parents=True, exist_ok=True)
    logger.debug("Updating '%s' in cache", file_path)
    try:
        with open(file_path, "w", encoding="utf-8") as textfile:
            textfile.write(data)
    except TypeError as e:
        logging.error("Could not serialize data")
        logging.error("%s", e)
        return False
    return True


def retrieve_from_cache_as_text(file_path: str) -> str | bool:
    """
    Retrieve data from cache as str

    Args:
        file_path (str): The path to the cache file.

    Returns:
        The data from the cache file if it exists, otherwise False.
    """
    logger = logging.getLogger("Cache")
    try:
        with open(file_path, "r", encoding="utf-8") as textfile:
            data = textfile.read()
        return data
    except FileNotFoundError:
        logger.debug("File Not Found")
    return False


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
    return store_in_cache_as_text(file_path, json_data)


def retrieve_from_cache(file_path: str) -> Any | bool:
    """
    Retrieve query data from cache.

    Args:
        file_path (str): The path to the cache file.

    Returns:
        The data from the cache file if it exists, otherwise False.
    """
    logger = logging.getLogger("Cache")
    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        logger.debug("File Not Found")
    return False


def retrieve_or_request(url: str, path: str) -> str | bool:
    """Retrieve from cache or request."""
    cached = retrieve_from_cache_as_text(path)
    if cached is not False:
        return cached
    webpage = requests.get(url, timeout=5)
    store_in_cache_as_text(path, webpage.text)
    return webpage.text
