"""Tests for the store_in_cache_as_text function in the cache module."""

import os

from query_and_cache.cache import store_in_cache_as_text


def test_sicat_can_store_text_in_cache():
    """Test that the store_in_cache_as_text function can store text in a cache file."""
    file_path = os.path.join(".", "cache", "test", "html", "test_file.txt")
    data = "This is a test string."
    result = store_in_cache_as_text(file_path, data)
    with open(file_path, "r", encoding="utf-8") as textfile:
        stored_data = textfile.read()
    assert stored_data == data
    assert result is True


def test_sicat_false_with_invalid_input():
    """Test that store_in_cache_as_text returns False with invalid input."""
    file_path = os.path.join(".", "cache", "test", "test_file.txt")
    data = {"key": "value"}
    result = store_in_cache_as_text(file_path, data)
    assert result is False


def test_sicat_false_with_empty_path():
    """Test that store_in_cache_as_text returns False with an empty path."""
    file_path = os.path.join("")
    data = "This is a test string."
    result = store_in_cache_as_text(file_path, data)
    assert result is False
