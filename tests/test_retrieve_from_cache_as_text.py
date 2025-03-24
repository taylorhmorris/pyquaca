"""Tests for the retrieve_from_cache_as_text function."""

import os
from unittest.mock import mock_open, patch

from query_and_cache.cache import retrieve_from_cache_as_text


@patch("builtins.open", new_callable=mock_open, read_data="dummy test text")
def test_rfcat_can_retrieve_text_from_cache(mock_file):
    """Test that retrieve_from_cache_as_text can retrieve text from cache."""
    file_path = os.path.join(".", "cache", "test", "html", "test_file.txt")
    data = "dummy test text"
    result = retrieve_from_cache_as_text(file_path)
    assert result == data
    mock_file.assert_called_once_with(file_path, "r", encoding="utf-8")


def test_rfcat_false_with_empty_path() -> None:
    """Test that retrieve_from_cache_as_text returns False with empty path."""
    file_path = os.path.join("")
    result = retrieve_from_cache_as_text(file_path)
    assert result is False


@patch("builtins.open", new_callable=mock_open)
def test_rfcat_false_with_file_not_found(mock_file):
    """Test that retrieve_from_cache_as_text returns False with file not found."""
    mock_file.return_value.__enter__.side_effect = FileNotFoundError
    file_path = os.path.join(".", "cache", "test", "html", "test_file.txt")
    result = retrieve_from_cache_as_text(file_path)
    assert result is False
    mock_file.assert_called_once_with(file_path, "r", encoding="utf-8")
