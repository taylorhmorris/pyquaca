"""Tests for the store_in_cache function in the cache module."""

import json
import os
from unittest.mock import patch

from query_and_cache.cache import store_in_cache


def test_sic_can_store_text_in_cache():
    """Test that the store_in_cache function can store an object in a cache file."""
    file_path = os.path.join(".", "cache", "test", "json", "test_file.txt")
    data = {"msg": "This is a test string."}
    result = store_in_cache(file_path, data)
    with open(file_path, "r", encoding="utf-8") as textfile:
        stored_data = textfile.read()
    assert json.loads(stored_data) == data
    assert result is True


def test_sic_false_with_invalid_input():
    """Test that the store_in_cache function returns False with invalid input."""
    file_path = os.path.join(".", "cache", "test", "test_file.txt")
    data = None
    result = store_in_cache(file_path, data)
    assert result is False


def test_sic_false_with_empty_path():
    """Test that the store_in_cache function returns False with an empty path."""
    file_path = ""
    data = {"msg": "This is a test string."}
    result = store_in_cache(file_path, data)
    assert result is False


# Test store in cache returns False on TypeError
@patch("query_and_cache.cache.json.dumps", side_effect=TypeError)
def test_sic_false_with_type_error(mock_json):
    """Test that store_in_cache_as_text returns False on TypeError."""
    file_path = os.path.join(".", "cache", "test", "html", "test_file.txt")
    data = {"key": "value"}
    result = store_in_cache(file_path, data)
    assert result is False
    mock_json.assert_called_once_with(data)
