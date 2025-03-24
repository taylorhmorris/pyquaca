"""Cache class for caching query results."""

import logging
import os
from pathlib import Path
from typing import Any


class Cache:
    """Cache class for caching query results."""

    def __init__(self, cache_dir: str, ext: str = "") -> None:
        self.cache_dir = cache_dir
        self.ext = ext
        # Create the cache directory if it does not exist
        Path(self.cache_dir).mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger("Cache")

    def retrieve(self, key: str) -> None | str:
        """
        Retrieve data from the cache.

        Args:
            key (str): The cache key to lookup.

        Returns:
            the data string if it is found in the cache, None otherwise.
        """
        full_path = os.path.join(self.cache_dir, key + self.ext)
        try:
            with open(full_path, "r", encoding="utf-8") as cache_file:
                return cache_file.read()
        except (FileNotFoundError, PermissionError, IOError) as e:
            self.logger.error("Could not read from cache %s", e)
        return None

    def store(self, key: str, value: Any) -> bool:
        """
        Store data in the cache.

        Args:
            key (str): The key string.
            value (str): The data to store.

        Returns:
            True if the data is successfully stored, False otherwise.
        """
        if not key or len(key) < 1:
            self.logger.error("Invalid key")
            return False
        full_path = os.path.join(self.cache_dir, key + self.ext)
        try:
            with open(full_path, "w", encoding="utf-8") as cache_file:
                cache_file.write(value)
            return True
        except (PermissionError, IOError) as e:
            self.logger.error("Could not write to cache %s", e)
        return False
