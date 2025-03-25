"""Tests for the Cacher class."""

import os
from unittest import mock

from hypothesis import given
from hypothesis import strategies as st

from pyquaca.cache import Cache


def test_cacher_can_instantiate() -> None:
    """Test that the Cache class can be instantiated."""

    with mock.patch("query_and_cache.cache.Path") as mock_path:
        cacher = Cache("testcache")
        assert mock_path.called
    assert isinstance(cacher, Cache)


@mock.patch("builtins.open", new_callable=mock.mock_open, read_data="dummy test text")
def test_cache_retrieve(mock_file) -> None:
    """Test the Cache.retrieve method."""

    with mock.patch("query_and_cache.cache.Path"):
        cacher = Cache("testcache")
    assert cacher.retrieve("test") == "dummy test text"
    cache_path = os.path.join("testcache", "test")
    mock_file.assert_called_once_with(cache_path, "r", encoding="utf-8")


# Test Cache.retrieve returns None when file not found
@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_cache_retrieve_file_not_found(mock_file) -> None:
    """Test the Cache.retrieve method when file not found."""

    with mock.patch("query_and_cache.cache.Path"):
        cacher = Cache("testcache")
    mock_file.side_effect = FileNotFoundError
    assert cacher.retrieve("test") is None
    cache_path = os.path.join("testcache", "test")
    mock_file.assert_called_once_with(cache_path, "r", encoding="utf-8")


# Test Cache.retrieve returns None when permission error
@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_cache_retrieve_permission_error(mock_file) -> None:
    """Test the Cache.retrieve method when permission error."""

    with mock.patch("query_and_cache.cache.Path"):
        cacher = Cache("testcache")
    mock_file.side_effect = PermissionError
    assert cacher.retrieve("test") is None
    cache_path = os.path.join("testcache", "test")
    mock_file.assert_called_once_with(cache_path, "r", encoding="utf-8")


# Test Cache.retrieve returns None when IO error
@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_cache_retrieve_io_error(mock_file) -> None:
    """Test the Cache.retrieve method when IO error."""

    with mock.patch("query_and_cache.cache.Path"):
        cacher = Cache("testcache")
    mock_file.side_effect = IOError
    assert cacher.retrieve("test") is None
    cache_path = os.path.join("testcache", "test")
    mock_file.assert_called_once_with(cache_path, "r", encoding="utf-8")


# Test Cache.retrieve returns None when key is empty
def test_cache_retrieve_empty_key() -> None:
    """Test the Cache.retrieve method when key is empty."""

    with mock.patch("query_and_cache.cache.Path"):
        cacher = Cache("testcache")
    assert cacher.retrieve("") is None


# Test Cache.store returns True when successful
@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_cache_store(mock_file) -> None:
    """Test the Cache.store method."""

    with mock.patch("query_and_cache.cache.Path"):
        cacher = Cache("testcache")
    assert cacher.store("test", "dummy test text")
    cache_path = os.path.join("testcache", "test")
    mock_file.assert_called_once_with(cache_path, "w", encoding="utf-8")
    handle = mock_file()
    handle.write.assert_called_once_with("dummy test text")


# Test Cache.store returns False when permission error
@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_cache_store_permission_error(mock_file) -> None:
    """Test the Cache.store method when permission error."""

    with mock.patch("query_and_cache.cache.Path"):
        cacher = Cache("testcache")
    mock_file.side_effect = PermissionError
    assert not cacher.store("test", "dummy test text")
    cache_path = os.path.join("testcache", "test")
    mock_file.assert_called_once_with(cache_path, "w", encoding="utf-8")


# Test Cache.store returns False when IO error
@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_cache_store_io_error(mock_file) -> None:
    """Test the Cache.store method when IO error."""

    with mock.patch("query_and_cache.cache.Path"):
        cacher = Cache("testcache")
    mock_file.side_effect = IOError
    assert not cacher.store("test", "dummy test text")
    cache_path = os.path.join("testcache", "test")
    mock_file.assert_called_once_with(cache_path, "w", encoding="utf-8")


# Test Cache.store returns False when key is empty
def test_cache_store_empty_key() -> None:
    """Test the Cache.store method when key is empty."""

    with mock.patch("query_and_cache.cache.Path"):
        cacher = Cache("testcache")
    assert not cacher.store("", "dummy test text")


# Test Cache.store can store any text
@given(st.text())
def test_cache_store_hypo(s: str) -> None:
    """Test the Cache.store method with Hypothesis."""

    with mock.patch("query_and_cache.cache.Path"):
        cacher = Cache("testcache")
    with mock.patch("builtins.open", new_callable=mock.mock_open) as mock_file:
        assert cacher.store("test", s)
        cache_path = os.path.join("testcache", "test")
        mock_file.assert_called_once_with(cache_path, "w", encoding="utf-8")
        handle = mock_file()
        handle.write.assert_called_once_with(s)


# Test Cache.retrieve can retrieve any text
@given(st.text())
def test_cache_retrieve_hypo(s: str) -> None:
    """Test the Cache.retrieve method with Hypothesis."""

    with mock.patch("query_and_cache.cache.Path"):
        cacher = Cache("testcache")
    with mock.patch(
        "builtins.open", new_callable=mock.mock_open, read_data=s
    ) as mock_file:
        assert cacher.retrieve("test") == s
        cache_path = os.path.join("testcache", "test")
        mock_file.assert_called_once_with(cache_path, "r", encoding="utf-8")


# Test Cache.store returns False when value is empty
def test_cache_store_empty_value() -> None:
    """Test the Cache.store method when value is empty."""

    with mock.patch("query_and_cache.cache.Path"):
        cacher = Cache("testcache")
    assert not cacher.store("test", "")


# Test Cache.store returns False when value is invalid
def test_cache_store_invalid_value() -> None:
    """Test the Cache.store method when value is invalid."""

    with mock.patch("query_and_cache.cache.Path"):
        cacher = Cache("testcache")
    assert not cacher.store("test", {"key": "value"})
