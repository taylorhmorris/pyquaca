"""Test the Requester class"""

from unittest import mock

from pyquaca.requester import Requester


# Test Requester can be created
def test_requester_creation():
    """Test if the Requester class can be created with a URL."""
    url = "https://example.com/{search_string}"
    requester = Requester(url)
    assert requester.base_url == url
    assert requester.logger.name == "Requester"


# Test Requester can make a request
def test_requester_request():
    """Test if the Requester class can make a request."""
    url = "https://example.com/{search_string}"
    requester = Requester(url)
    query_string = "test"
    with mock.patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "test response"
        response = requester.request(query_string)
        assert response is not None
        assert response.status_code == 200


# Test Requester.request handles non-200 status codes
def test_requester_request_non_200():
    """Test if the Requester class handles non-200 status codes."""
    url = "https://example.com/{search_string}"
    requester = Requester(url)
    query_string = "test"
    with mock.patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 404
        response = requester.request(query_string)
        assert response is None
