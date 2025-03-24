"""Query Class to be extended for use with specific sites"""

import logging
from typing import Any, NotRequired, Optional, TypedDict

from query_and_cache.cache import Cache
from query_and_cache.parser import Parser
from query_and_cache.requester import Requester


class QueryConfig(TypedDict):
    """Configuration for Query Class"""

    auth: NotRequired[str]
    check_cache: NotRequired[bool]
    api_key: NotRequired[str]
    cache_path: NotRequired[str]
    parser: NotRequired[Parser]
    cache: NotRequired[Cache]
    requester: NotRequired[Requester]


class Query:  # pylint: disable=too-few-public-methods
    """Query Class to be extended for use with specific sites"""

    def __init__(self, url: str, config: Optional[QueryConfig] = None):
        if config is None:
            config = {}
        self.auth = config.get("auth", None)
        self.check_cache = config.get("check_cache", True)
        self.api_key = config.get("api_key", None)
        cache_path = config.get("cache_path", "cache")
        self.parser = config.get("parser", None)
        self.cache = config.get("cache", Cache(cache_path))
        self.requester = config.get("requester", Requester(url))
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
        response = self.requester.request(query_string)
        if self.parser:
            self.logger.debug("Parsing data")
            response = self.parser.parse(response)
        else:
            self.logger.debug("No parser found, returning raw data")
        if self.check_cache and self.cache:
            self.cache.store(query_string, response)
        return response
