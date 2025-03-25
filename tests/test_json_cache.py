"""Tests for the JSONCache class."""

import os
from unittest import mock

from pyquaca.cache import Cache
from pyquaca.json_cache import JSONCache


def test_json_cache_can_instantiate() -> None:
    """Test that the JSONCache class can be instantiated."""

    with mock.patch("pyquaca.cache.Path") as mock_path:
        cache = JSONCache("testcache")
        assert mock_path.called
    assert isinstance(cache, JSONCache)
    assert isinstance(cache, Cache)
    assert cache.file_extension == ".json"


@mock.patch(
    "builtins.open", new_callable=mock.mock_open, read_data='{"keystr": "valuestr"}'
)
def test_json_cache_retrieve(mock_file) -> None:
    """Test the JSONCache.retrieve method."""

    with mock.patch("pyquaca.cache.Path"):
        cache = JSONCache("testcache")
    assert cache.retrieve("test") == {"keystr": "valuestr"}
    cache_path = os.path.join("testcache", "test" + cache.file_extension)
    mock_file.assert_called_once_with(cache_path, "r", encoding="utf-8")


# Test JSONCache.retrieve returns None when file not found
@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_json_cache_retrieve_file_not_found(mock_file) -> None:
    """Test the JSONCache.retrieve method when file not found."""

    with mock.patch("pyquaca.cache.Path"):
        cache = JSONCache("testcache")
    mock_file.side_effect = FileNotFoundError
    assert cache.retrieve("test") is None
    cache_path = os.path.join("testcache", "test" + cache.file_extension)
    mock_file.assert_called_once_with(cache_path, "r", encoding="utf-8")


# Test JSONCache.retrieve returns None when permission error
@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_json_cache_retrieve_permission_error(mock_file) -> None:
    """Test the JSONCache.retrieve method when permission error."""

    with mock.patch("pyquaca.cache.Path"):
        cache = JSONCache("testcache")
    mock_file.side_effect = PermissionError
    assert cache.retrieve("test") is None
    cache_path = os.path.join("testcache", "test")
    mock_file.assert_called_once_with(
        cache_path + cache.file_extension, "r", encoding="utf-8"
    )


# Test JSONCache.retrieve returns None when IO error
@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_json_cache_retrieve_io_error(mock_file) -> None:
    """Test the JSONCache.retrieve method when IO error."""

    with mock.patch("pyquaca.cache.Path"):
        cache = JSONCache("testcache")
    mock_file.side_effect = IOError
    assert cache.retrieve("test") is None
    cache_path = os.path.join("testcache", "test")
    mock_file.assert_called_once_with(
        cache_path + cache.file_extension, "r", encoding="utf-8"
    )


# Test JSONCache.retrieve returns None when key is empty
def test_json_cache_retrieve_empty_key() -> None:
    """Test the JSONCache.retrieve method when key is empty."""

    with mock.patch("pyquaca.cache.Path"):
        cache = JSONCache("testcache")
    assert cache.retrieve("") is None


# Test JSONCache.store returns True when successful
@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_json_cache_store(mock_file) -> None:
    """Test the JSONCache.store method."""

    with mock.patch("pyquaca.cache.Path"):
        cache = JSONCache("testcache")
    sample_data = {"keystr": "valuestr"}
    assert cache.store("test", sample_data)
    cache_path = os.path.join("testcache", "test" + cache.file_extension)
    mock_file.assert_called_once_with(cache_path, "w", encoding="utf-8")
    handle = mock_file()
    handle.write.assert_called_once_with('{"keystr": "valuestr"}')


# Test JSONCache.store returns False when permission error
@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_json_cache_store_permission_error(mock_file) -> None:
    """Test the JSONCache.store method when permission error."""

    with mock.patch("pyquaca.cache.Path"):
        cache = JSONCache("testcache")
    mock_file.side_effect = PermissionError
    assert not cache.store("test", "dummy test text")
    cache_path = os.path.join("testcache", "test")
    mock_file.assert_called_once_with(
        cache_path + cache.file_extension, "w", encoding="utf-8"
    )


# Test JSONCache.store returns False when IO error
@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_json_cache_store_io_error(mock_file) -> None:
    """Test the JSONCache.store method when IO error."""

    with mock.patch("pyquaca.cache.Path"):
        cache = JSONCache("testcache")
    mock_file.side_effect = IOError
    assert not cache.store("test", {"key": "value"})
    cache_path = os.path.join("testcache", "test")
    mock_file.assert_called_once_with(
        cache_path + cache.file_extension, "w", encoding="utf-8"
    )


# Test JSONCache.store returns False when key is empty
def test_json_cache_store_empty_key() -> None:
    """Test the JSONCache.store method when key is empty."""

    with mock.patch("pyquaca.cache.Path"):
        cache = JSONCache("testcache")
    assert not cache.store("", "dummy test text")


# Test JSONCache.store returns False when value is empty
def test_json_cache_store_empty_value() -> None:
    """Test the JSONCache.store method when value is empty."""

    with mock.patch("pyquaca.cache.Path"):
        cache = JSONCache("testcache")
    assert not cache.store("test", "")


# Test JSONCache.store returns False when value is invalid
@mock.patch("pyquaca.json_cache.json.dumps", side_effect=TypeError)
@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_json_cache_store_invalid_value(mock_file, mock_dump) -> None:
    """Test the JSONCache.store method when value is invalid."""

    with mock.patch("pyquaca.cache.Path"):
        cache = JSONCache("testcache")
    assert not cache.store("test", {"key": "value"})
    assert mock_dump.called
    assert mock_file.called is False
