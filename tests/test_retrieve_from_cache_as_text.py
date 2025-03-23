"""Tests for the retrieve_from_cache_as_text function."""

import os

from query_and_cache.cache import retrieve_from_cache_as_text, store_in_cache_as_text


def test_rfcat_can_retrieve_text_from_cache():
    """Test that retrieve_from_cache_as_text can retrieve text from cache."""
    file_path = os.path.join(".", "cache", "test", "html", "test_file.txt")
    data = "This is a test string."
    store_in_cache_as_text(file_path, data)
    result = retrieve_from_cache_as_text(file_path)
    assert result == data


def test_rfcat_false_with_empty_path():
    """Test that retrieve_from_cache_as_text returns False with empty path."""
    file_path = os.path.join("")
    result = retrieve_from_cache_as_text(file_path)
    assert result is False
