"""Query Class to be extended for use with specific sites"""

import logging
import os
from typing import Any, NotRequired, Optional, TypedDict

from bs4 import BeautifulSoup

from query_and_cache.parser import Parser

from .cache import retrieve_from_cache, retrieve_or_request, store_in_cache


class QueryConfig(TypedDict):
    """Configuration for Query Class"""

    auth: NotRequired[str]
    check_cache: NotRequired[bool]
    api_key: NotRequired[str]
    cache_path: NotRequired[str]
    parser: NotRequired[Parser]


class Query:
    """Query Class to be extended for use with specific sites"""

    def __init__(self, url: str, config: Optional[QueryConfig] = None):
        if config is None:
            config = {}
        self.url = url
        self.auth = config.get("auth", None)
        self.check_cache = config.get("check_cache", True)
        self.api_key = config.get("api_key", None)
        self.cache_path = config.get("cache_path", "cache")
        self.parser = config.get("parser", None)
        self.service_name = self.__class__.__name__.lstrip("Query").lower()
        if len(self.service_name) == 0:
            self.service_name = "query"
        self.logger = logging.getLogger(f"{self.service_name}")
        self.logger.setLevel(logging.DEBUG)

    def get_full_cache_path(self, filename: str) -> str:
        """Get the full path to the cache file"""
        return os.path.join(self.cache_path, self.service_name, filename)

    def retrieve_cache(self, search_string: str) -> bool | Any:
        """Retrieve query data from cache"""
        if len("".join(e for e in search_string if e.isalnum())) < 1:
            self.logger.debug("Invalid search string")
            return False
        cache_file_path = self.get_full_cache_path(f"{search_string}.json")
        return retrieve_from_cache(cache_file_path)

    def store_in_cache(self, search_string: str, data: Any) -> bool:
        """Store query data in cache"""
        if len("".join(e for e in search_string if e.isalnum())) < 1:
            return False
        try:
            word = data["word"]
            if not word or len("".join(e for e in word if e.isalnum())) < 1:
                return False
        except KeyError as e:
            word = search_string
            self.logger.warning("%s", e)
        cache_file_path = self.get_full_cache_path(f"{word}.json")
        return store_in_cache(cache_file_path, data)

    def query(self, search_string: str) -> Any:
        """Query the site with search_string"""
        search_string = search_string.lower()
        if self.check_cache:
            cached: bool | Any = self.retrieve_cache(search_string)
            if cached is not False and cached is not True and cached is not None:
                self.logger.info("Search string (%s) found in cache", search_string)
                return cached
            self.logger.info("Search string (%s) not found in cache", search_string)
        else:
            self.logger.info("Skipping Cache as requested")
        url = self.url.format(search_string=search_string, api_key=self.api_key)
        self.logger.debug("querying %s", url)
        webpage = retrieve_or_request(
            url, self.get_full_cache_path(f"{search_string}.html")
        )
        if webpage is False or webpage is True or webpage is None:
            self.logger.error("Error retrieving webpage")
            return False
        soup = BeautifulSoup(webpage, features="html.parser")

        if self.parser:
            self.logger.debug("Parsing data")
            results = self.parser.parse(soup)
        else:
            self.logger.debug("No parser found, returning raw data")
            results = soup

        if "word" not in results or results["word"] is None:
            results["word"] = search_string
        try:
            self.store_in_cache(search_string, results)
        except KeyError as e:
            self.logger.error("Error storing in cache: results does not have %s key", e)
        self.logger.debug("Returning query results")
        return results
