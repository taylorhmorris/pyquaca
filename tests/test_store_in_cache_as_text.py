"""Tests for the store_in_cache_as_text function in the cache module."""

import os
from unittest.mock import mock_open, patch

import hypothesis.strategies as st
from hypothesis import given

from query_and_cache.cache import store_in_cache_as_text


def test_sicat_can_store_text_in_cache() -> None:
    """Test that the store_in_cache_as_text function can store text in a cache file."""
    file_path = os.path.join(".", "cache", "test", "html", "test_file.txt")
    data = "This is a test string."
    with patch("builtins.open", new_callable=mock_open) as mock_file:
        result = store_in_cache_as_text(file_path, data)
        mock_file.assert_called_once_with(file_path, "w", encoding="utf-8")
        handle = mock_file()
        handle.write.assert_called_once_with(data)
        assert result is True


def test_sicat_false_with_invalid_input() -> None:
    """Test that store_in_cache_as_text returns False with invalid input."""
    file_path = os.path.join(".", "cache", "test", "test_file.txt")
    data = {"key": "value"}
    result = store_in_cache_as_text(file_path, data)
    assert result is False


def test_sicat_false_with_empty_path() -> None:
    """Test that store_in_cache_as_text returns False with an empty path."""
    file_path = os.path.join("")
    data = "This is a test string."
    result = store_in_cache_as_text(file_path, data)
    assert result is False


@given(st.text())
def test_hypo_can_store_text(s: str) -> None:
    """Test that store_in_cache_as_text can store text in a cache file."""
    with patch("builtins.open", new_callable=mock_open) as mock_file:
        file_path = os.path.join(".", "cache", "unused", "test_file.txt")
        result = store_in_cache_as_text(file_path, s)
        mock_file.assert_called_once_with(file_path, "w", encoding="utf-8")
        handle = mock_file()
        handle.write.assert_called_once_with(s)
        assert result is True
