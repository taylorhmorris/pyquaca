"""Test APIRequester class."""

# Test can create APIRequester
from query_and_cache.api_requester import APIRequester


def test_api_requester_creation():
    """Test if the APIRequester class can be created with a URL."""
    url = "https://example.com/{search_string}"
    requester = APIRequester(url)
    assert requester.base_url == url
    assert requester.logger.name == "Requester.API"


def test_api_requester_creation_with_api_key():
    """Test if the APIRequester class can be created with an API key."""
    url = "https://example.com/{search_string}?api_key={api_key}"
    api_key = "test_api_key"
    requester = APIRequester(url, api_key)
    assert requester.base_url == url
    assert requester.api_key == api_key
    assert requester.logger.name == "Requester.API"

    url = requester.format_url("test")
    assert url == "https://example.com/test?api_key=test_api_key"
