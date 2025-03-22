"""
Unit tests for the cache functions in the query_and_cache.cache module.
"""

import os
import shutil
import unittest

import requests
from bs4 import BeautifulSoup

from query_and_cache.cache import retrieve_or_request


class Test(unittest.TestCase):
    """Test case for the retrieve_or_request function."""

    def tearDown(self) -> None:
        """Remove the test cache directory after each test."""
        path = os.path.join(".", "cache", "test", "html")
        shutil.rmtree(path)
        return super().tearDown()

    def test_retrieve_or_request(self):
        """Test the retrieve_or_request function with a sample URL."""
        url = "https://example.com/"
        filepath = os.path.join(".", "cache", "test", "html", "test_file_html.html")
        text_response = retrieve_or_request(url, filepath)
        manual_request = requests.get(url, timeout=5)
        self.assertEqual(text_response, manual_request.text)
        soup = BeautifulSoup(text_response, features="html.parser")
        self.assertEqual(soup.title.text, "Example Domain")


if __name__ == "__main__":
    unittest.main()
