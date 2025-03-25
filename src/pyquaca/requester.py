"""Requester class to handle requests to a given URL."""

import logging

import requests


class Requester:
    """Requester class to handle requests to a given URL."""

    def __init__(self, url: str):
        self.base_url = url
        self.logger = logging.getLogger("Requester")

    def request(self, query_string: str) -> str | requests.Response | None:
        """Make a request with the given query_string"""
        self.logger.info("Requesting with query_string: %s", query_string)
        url = self.format_url(query_string)
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            self.logger.error("Request to %s failed (%s)", url, response.status_code)
            return None
        self.logger.debug("Received response from %s", url)
        return response

    def format_url(self, query_string: str) -> str:
        """Format the URL with the given query_string"""
        return self.base_url.format(search_string=query_string)
