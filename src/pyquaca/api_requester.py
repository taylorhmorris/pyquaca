"""APIRequester class to handle requests to a given API endpoint."""

from pyquaca.requester import Requester


class APIRequester(Requester):
    """APIRequester class to handle requests to a given API endpoint."""

    def __init__(self, url: str, api_key: str | None = None):
        super().__init__(url)
        self.logger = self.logger.getChild("API")
        self.api_key = api_key

    def format_url(self, query_string: str) -> str:
        """Format the URL with the given query_string and API key if provided."""
        return self.base_url.format(search_string=query_string, api_key=self.api_key)
