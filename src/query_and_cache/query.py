"""Query Class to be extended for use with specific sites"""

import logging
from typing import Any, NotRequired, Optional, TypedDict

import requests

from query_and_cache.cacheclass import Cache
from query_and_cache.parser import Parser


class QueryConfig(TypedDict):
    """Configuration for Query Class"""

    auth: NotRequired[str]
    check_cache: NotRequired[bool]
    api_key: NotRequired[str]
    cache_path: NotRequired[str]
    parser: NotRequired[Parser]
    cache: NotRequired[Cache]


class Query:  # pylint: disable=too-few-public-methods
    """Query Class to be extended for use with specific sites"""

    def __init__(self, url: str, config: Optional[QueryConfig] = None):
        if config is None:
            config = {}
        self.url = url
        self.auth = config.get("auth", None)
        self.check_cache = config.get("check_cache", True)
        self.api_key = config.get("api_key", None)
        cache_path = config.get("cache_path", "cache")
        self.parser = config.get("parser", None)
        self.cache = config.get("cache", Cache(cache_path))
        service_name = self.__class__.__name__.lstrip("Query").lower()
        if len(service_name) == 0:
            service_name = "query"
        self.logger = logging.getLogger(f"{service_name}")
        self.logger.setLevel(logging.DEBUG)

    def query(self, query_string: str) -> Any:
        """Query the site with query_string"""
        query_string = query_string.lower()
        if self.check_cache and self.cache:
            cached: Any | None = self.cache.retrieve(query_string)
            if cached is not None:
                self.logger.info("Search string (%s) found in cache", query_string)
                return cached
            self.logger.info("Search string (%s) not found in cache", query_string)
        else:
            self.logger.info("Skipping Cache as requested")
        url = self.url.format(search_string=query_string, api_key=self.api_key)
        self.logger.debug("querying %s", url)
        result = requests.get(url, timeout=5)
        if result.status_code != 200:
            self.logger.error("Query of %s failed (%s)", url, result.status_code)
            return None
        if self.parser:
            self.logger.debug("Parsing data")
            result = self.parser.parse(result)
        else:
            self.logger.debug("No parser found, returning raw data")
        if self.check_cache and self.cache:
            self.cache.store(query_string, result)
        return result
