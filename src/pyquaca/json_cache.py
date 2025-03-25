"""This module provides a JSONCache class to work with JSON data."""

import json
from typing import Any

from pyquaca.cache import Cache


class JSONCache(Cache):
    """Cache class for storing and retrieving objects as JSON data."""

    def __init__(self, cache_dir: str, file_extension: str = ".json") -> None:
        super().__init__(cache_dir, file_extension)
        self.logger = self.logger.getChild("JSONCache")

    def retrieve(self, key: str) -> None | Any:
        data = super().retrieve(key)
        if data:
            return json.loads(data)
        return None

    def store(self, key: str, value: Any) -> bool:
        if not key or len(key) < 1:
            self.logger.error("Invalid key")
            return False
        if not value:
            self.logger.error("Invalid value")
            return False
        try:
            serialized_data = json.dumps(value)
        except TypeError as e:
            self.logger.error("Could not serialize data: %s", e)
            return False
        return super().store(key, serialized_data)
